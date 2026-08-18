import pytest


@pytest.fixture(scope="class")
def setup():
  print("I wll be executing first")
  yield
  print("I will excuted last")
