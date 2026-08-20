import pytest


@pytest.fixture(scope="class")
def setup():
  print("I will be executing first")
  yield
  print("I will excuted last")

@pytest.fixture()
def dataLoad():
  print("user profile data is being created")
  return ["Rahul", "Shetty", "rahulshetty.com"]

@pytest.fixture(params=["Chrome", "Firefox", "IE"])
def crossBrowser(request):
  return request.param