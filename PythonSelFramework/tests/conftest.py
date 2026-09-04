from selenium import webdriver

import pytest

def pytest_addoption(parser):
  parser.addoption(
    "--browser_name", action="store", default="chrome"
  )


@pytest.fixture(scope="class")
def setup(request):
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
