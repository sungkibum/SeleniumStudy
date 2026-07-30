import json
import os
import re
import subprocess
import sys
import requests

# ==========================================
# 1. 환경 변수 및 설정 로드
# ==========================================
api_key = os.environ.get("GEMINI_API_KEY")
github_token = os.environ.get("GITHUB_TOKEN")
repo = os.environ.get("GITHUB_REPOSITORY")

# 필수 환경변수 누락 체크
if not api_key or not github_token or not repo:
    print("❌ 오류: 필수 환경 변수(GEMINI_API_KEY, GITHUB_TOKEN, GITHUB_REPOSITORY)가 설정되지 않았습니다.")
    sys.exit(1)

headers = {
    "Authorization": f"token {github_token}",
    "Accept": "application/vnd.github.v3+json",
}


# Gemini API 호출 헬퍼 함수 (SDK 패키지 버전 문제 우회 및 최신 모델 적용)
def call_gemini_api(prompt: str, model: str = "gemini-2.5-flash") -> str:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }
    res = requests.post(url, json=payload)
    if res.status_code != 200:
        # gemini-2.5-flash 실패 시 gemini-2.0-flash로 재시도
        if model == "gemini-2.5-flash":
            print("⚠️ gemini-2.5-flash 호출 실패, gemini-2.0-flash로 재시도합니다...")
            return call_gemini_api(prompt, model="gemini-2.0-flash")
        raise Exception(f"Gemini API 호출 실패 ({res.status_code}): {res.text}")
    
    data = res.json()
    return data["candidates"][0]["content"]["parts"][0]["text"]


# ==========================================
# 2. 최근 커밋에서 변경된 파일 감지
# ==========================================
def get_changed_files():
    """최근 커밋(git diff)에서 변경되거나 추가된 파일 목록을 가져옵니다."""
    try:
        diff_output = subprocess.check_output(
            ["git", "diff", "--name-only", "HEAD~1", "HEAD"]
        ).decode("utf-8")
        files = [f.strip() for f in diff_output.splitlines() if f.strip()]
        return files
    except Exception as e:
        print(f"⚠️ Git diff 추출 실패 (첫 커밋이거나 단일 커밋일 수 있음): {e}")
        return []


# ==========================================
# 3. 시나리오 A: Python(.py) 수정 ➔ 퀴즈 Issue 생성
# ==========================================
def handle_python_changes(changed_files):
    print("🐍 Python 파일 변경 감지: 퀴즈 Issue 생성을 시작합니다.")

    # studyLog.md 또는 challengeLog.md 내용 읽기 (없으면 py 파일 내용 사용)
    log_context = ""
    for log_file in ["challengeLog.md", "studyLog.md"]:
        if os.path.exists(log_file):
            with open(log_file, "r", encoding="utf-8") as f:
                log_context += f"\n--- {log_file} ---\n" + f.read()

    # 로그 파일이 없으면 변경된 .py 파일 자체를 읽음
    if not log_context:
        for py_file in [f for f in changed_files if f.endswith(".py")]:
            if os.path.exists(py_file):
                with open(py_file, "r", encoding="utf-8") as f:
                    log_context += f"\n--- {py_file} ---\n" + f.read()

    prompt = f"""
    당신은 친절한 프로그래밍 튜터입니다. 
    아래 작성된 학습 기록 및 코드를 바탕으로 개발자의 이해도를 점검할 수 있는 퀴즈 1~2개를 작성해주세요.

    [학습 내용]:
    {log_context}

    [작성 요구사항]:
    1. 첫 줄은 반드시 `# [Quiz] 주제` 형태로 작성해주세요.
    2. 문제의 출제 의도, 문제 설명, 작성해야 할 답안 가이드를 명확히 작성해주세요.
    """

    quiz_content = call_gemini_api(prompt)
    quiz_title = "[Quiz] 파이썬 학습 점검 퀴즈"

    # 제목 추출
    for line in quiz_content.strip().split("\n"):
        if "[Quiz]" in line:
            quiz_title = line.replace("#", "").strip()
            break

    # GitHub API를 사용해 Issue 등록
    issue_url = f"https://api.github.com/repos/{repo}/issues"
    payload = {
        "title": quiz_title,
        "body": quiz_content,
        "labels": ["quiz"],
    }

    res = requests.post(issue_url, headers=headers, json=payload)
    if res.status_code == 201:
        print(f"✅ 퀴즈 Issue가 성공적으로 생성되었습니다: {quiz_title}")
    else:
        print(f"❌ Issue 생성 실패 ({res.status_code}): {res.text}")


# ==========================================
# 4. 시나리오 B: Markdown(.md) 수정 ➔ 채점 및 조건부 Issue 종료
# ==========================================
def handle_markdown_changes(changed_files):
    print("📝 Markdown 파일 변경 감지: 열려있는 퀴즈 Issue 채점을 시작합니다.")

    issues_url = f"https://api.github.com/repos/{repo}/issues?state=open&labels=quiz"
    res = requests.get(issues_url, headers=headers)
    open_issues = res.json() if res.status_code == 200 else []

    if not open_issues:
        print("ℹ️ 채점할 'open' 상태의 퀴즈 Issue가 없습니다.")
        return

    target_issue = open_issues[0]
    issue_number = target_issue["number"]
    issue_body = target_issue["body"]

    user_answer = ""
    for md_file in [f for f in changed_files if f.endswith(".md")]:
        if os.path.exists(md_file):
            with open(md_file, "r", encoding="utf-8") as f:
                user_answer += f"\n--- {md_file} ---\n" + f.read()

    grading_prompt = f"""
    당신은 엄격하지만 친절한 프로그래밍 채점관입니다.
    
    [퀴즈 문제]:
    {issue_body}

    [제출된 답안]:
    {user_answer}

    위 답안을 평가하여 반드시 아래 JSON 형식으로만 응답해주세요. 다른 설명이나 텍스트는 덧붙이지 마세요.

    {{
      "score": 0부터 100 사이의 정수,
      "feedback": "상세한 피드백, 잘한 점, 부족한 점, 모범 답안 해설"
    }}
    """

    raw_text = call_gemini_api(grading_prompt)

    try:
        json_match = re.search(r"\{.*\}", raw_text, re.DOTALL)
        if json_match:
            result = json.loads(json_match.group(0))
        else:
            result = json.loads(raw_text)

        score = int(result.get("score", 0))
        feedback = result.get("feedback", "피드백을 불러올 수 없습니다.")
    except Exception as e:
        print(f"⚠️ JSON 파싱 실패: {e}\n원본 응답: {raw_text}")
        score = 0
        feedback = f"채점 처리 중 형식이 올바르지 않아 에러가 발생했습니다.\n\n{raw_text}"

    status_tag = "🎉 **통과 (Pass)**" if score >= 80 else "❌ **재도전 필요 (Fail)**"
    comment_body = (
        f"## 📝 퀴즈 채점 결과\n\n"
        f"- **점수:** {score}점 / 100점 ({status_tag})\n\n"
        f"### 💡 피드백 & 모범 답안\n{feedback}"
    )

    comment_url = f"https://api.github.com/repos/{repo}/issues/{issue_number}/comments"
    requests.post(comment_url, headers=headers, json={"body": comment_body})
    print(f"💬 Issue #{issue_number}번에 채점 코멘트를 작성했습니다. (점수: {score}점)")

    if score >= 80:
        close_url = f"https://api.github.com/repos/{repo}/issues/{issue_number}"
        requests.patch(close_url, headers=headers, json={"state": "closed"})
        print(f"🎯 80점 이상({score}점) 달성으로 Issue #{issue_number}번을 자동으로 Closed 처리합니다!")
    else:
        print(f"🔄 80점 미만({score}점)이므로 Issue #{issue_number}번을 Open 상태로 유지합니다. 재도전해 보세요!")


# ==========================================
# 5. 메인 실행 흐름 (Main Execution)
# ==========================================
if __name__ == "__main__":
    changed_files = get_changed_files()
    print(f"🔍 최근 커밋에서 변경된 파일: {changed_files}")

    has_py = any(f.endswith(".py") for f in changed_files)
    has_md = any(f.endswith(".md") for f in changed_files)

    if has_py:
        handle_python_changes(changed_files)
    elif has_md:
        handle_markdown_changes(changed_files)
    else:
        print("ℹ️ 처리할 .py 또는 .md 파일 변경 사항이 없습니다.")