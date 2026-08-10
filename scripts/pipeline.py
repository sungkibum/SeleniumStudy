import json
import os
import subprocess
import sys
import time
import requests

# ==========================================
# 1. 환경 변수 및 설정 로드
# ==========================================
api_key = os.environ.get("GEMINI_API_KEY")
github_token = os.environ.get("GITHUB_TOKEN")
repo = os.environ.get("GITHUB_REPOSITORY")
event_name = os.environ.get("GITHUB_EVENT_NAME")
event_path = os.environ.get("GITHUB_EVENT_PATH")

if not api_key or not github_token or not repo:
    print("❌ 오류: 필수 환경 변수(GEMINI_API_KEY, GITHUB_TOKEN, GITHUB_REPOSITORY)가 없습니다.")
    sys.exit(1)

headers = {
    "Authorization": f"token {github_token}",
    "Accept": "application/vnd.github.v3+json",
}


# ==========================================
# 2. Gemini API 호출 함수 (Gemini 1.5 Flash 무료 모델)
# ==========================================
def call_gemini_api(prompt: str) -> str:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    req_headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    
    res = requests.post(url, headers=req_headers, json=payload)
    
    if res.status_code == 429:
        print("⚠️ Rate Limit 발생. 10초 대기 후 재시도...")
        time.sleep(10)
        res = requests.post(url, headers=req_headers, json=payload)

    if res.status_code != 200:
        raise Exception(f"Gemini API 호출 실패 ({res.status_code}): {res.text}")
    
    data = res.json()
    try:
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError):
        raise Exception(f"Gemini 응답 파싱 실패: {data}")


# ==========================================
# 3. [시나리오 1] Push 발생 ➔ 파이썬 코드 기반 퀴즈 Issue 생성
# ==========================================
def handle_push_event():
    print("🐍 파이썬 코드 변경 감지: 퀴즈 Issue 생성을 시작합니다.")
    
    try:
        diff_output = subprocess.check_output(
            ["git", "diff", "--name-only", "HEAD~1", "HEAD"]
        ).decode("utf-8")
        changed_files = [f.strip() for f in diff_output.splitlines() if f.strip().endswith(".py")]
    except Exception as e:
        print(f"⚠️ git diff 추출 실패: {e}")
        changed_files = []

    if not changed_files:
        print("ℹ️ 변경된 .py 파일이 없습니다. 종료합니다.")
        return

    code_context = ""
    for py_file in changed_files:
        if os.path.exists(py_file):
            with open(py_file, "r", encoding="utf-8") as f:
                code_context += f"\n--- 파일명: {py_file} ---\n" + f.read()

    prompt = f"""
    당신은 친절하고 전문적인 프로그래밍 튜터입니다.
    개발자가 작성/수정한 아래 파이썬 코드를 분석하여 이해도를 점검할 수 있는 퀴즈 1~2개를 작성해주세요.

    [제출된 코드]:
    {code_context}

    [작성 요구사항]:
    1. 첫 줄은 반드시 `# [Quiz] 주제` 형태로 작성해주세요.
    2. 문제의 출제 의도, 상세 문제 내용, 답안 작성 방식(예: '이 이슈의 댓글로 정답을 남겨주세요')을 명확히 제시하세요.
    """

    quiz_content = call_gemini_api(prompt)
    quiz_title = "[Quiz] 파이썬 코드 개념 점검 퀴즈"

    for line in quiz_content.strip().split("\n"):
        if "[Quiz]" in line:
            quiz_title = line.replace("#", "").strip()
            break

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
# 4. [시나리오 2] Issue 댓글 작성 ➔ AI 답안 채점 및 피드백 댓글 작성
# ==========================================
def handle_comment_event():
    print("📝 Issue 댓글 작성 감지: 답안 채점을 시작합니다.")

    if not os.path.exists(event_path):
        print("❌ 이벤트 페이로드 파일이 존재하지 않습니다.")
        return

    with open(event_path, "r", encoding="utf-8") as f:
        event_data = json.load(f)

    issue = event_data.get("issue", {})
    comment = event_data.get("comment", {})

    issue_number = issue.get("number")
    issue_body = issue.get("body")
    user_answer = comment.get("body")

    labels = [l.get("name") for l in issue.get("labels", [])]
    if "quiz" not in labels and "[Quiz]" not in issue.get("title", ""):
        print("ℹ️ 퀴즈 관련 Issue가 아니므로 채점을 건너뜁니다.")
        return

    grading_prompt = f"""
    당신은 엄격하지만 친절한 프로그래밍 채점관입니다.
    
    [퀴즈 문제]:
    {issue_body}

    [사용자가 댓글로 제출한 답안]:
    {user_answer}

    위 제출된 답안을 평가하여 점수(100점 만점)와 상세 피드백, 모범 답안을 친절하게 알려주세요.
    답안이 훌륭하다면 이슈를 닫아도 좋다는 안내 문구도 함께 적어주세요.
    """

    feedback_content = call_gemini_api(grading_prompt)

    comment_url = f"https://api.github.com/repos/{repo}/issues/{issue_number}/comments"
    res = requests.post(comment_url, headers=headers, json={"body": feedback_content})

    if res.status_code == 201:
        print(f"💬 Issue #{issue_number}번 이슈에 성공적으로 채점 피드백 코멘트를 달았습니다.")
    else:
        print(f"❌ 코멘트 작성 실패 ({res.status_code}): {res.text}")


# ==========================================
# 5. 메인 실행 흐름
# ==========================================
if __name__ == "__main__":
    print(f"🔍 감지된 이벤트: {event_name}")

    if event_name == "push":
        handle_push_event()
    elif event_name == "issue_comment":
        handle_comment_event()
    else:
        print(f"ℹ️ 처리 대상이 아닌 이벤트입니다: {event_name}")