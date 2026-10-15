from selenium import webdriver

import pytest
driver = None

def pytest_addoption(parser):
  parser.addoption(
    "--browser_name", action="store", default="chrome"
  )


@pytest.fixture(scope="class")
def setup(request):
  global driver
  browser_name = request.config.getoption("browser_name")
  if browser_name == "chrome":
    driver = webdriver.Chrome()
  elif browser_name == "firefox":
    driver = webdriver.Firefox()
  elif browser_name == "edge":
    driver = webdriver.Edge()

  driver.get("https://rahulshettyacademy.com/angularpractice/")
  driver.maximize_window()
  request.cls.driver = driver
  yield
  driver.close()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    pytest_html = item.config.pluginmanager.getplugin("html")
    outcome = yield
    report = outcome.get_result()
    extras = getattr(report, "extras", [])          # extra → extras

    if report.when in ("call", "setup"):
        xfail = hasattr(report, "wasxfail")
        if (report.skipped and xfail) or (report.failed and not xfail):
            if driver is not None:                   # driver가 있을 때만
                screenshot = driver.get_screenshot_as_base64()
                extras.append(pytest_html.extras.png(screenshot, "Screenshot"))
        report.extras = extras

def _capture_screenshot(name):
  driver.get_screenshot_as_file(name)
