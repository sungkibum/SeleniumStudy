from selenium import webdriver

import pytest


@pytest.fixture(scope="class")
def setup():
  driver = webdriver.Chrome()
  driver.get("https://qaclickacademy.github.io/protocommerce/")
  driver.maximize_window()