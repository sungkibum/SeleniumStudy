import pytest


@pytest.fixture()
def setup():
  print("I wll be executing first")
  yield
  print("I will excuted last")


def test_fixtureDemo(setup):
  print("I will execute steps in fixtureDemo method")