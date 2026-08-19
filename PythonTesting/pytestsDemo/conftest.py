import pytest


@pytest.fixture(scope="class")
def setup():
  print("I wll be executing first")
  yield
  print("I will excuted last")

@pytest.fixture()
def dataLoad():
  print("user profile data is being created")
  return ["Rahul", "Shetty", "rahulshetty.com"]
