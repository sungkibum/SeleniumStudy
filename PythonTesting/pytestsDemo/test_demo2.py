# Any pytest file sould start with test_ or end with _test
# pytest method names should start with test
# Any code should be wrapped in method only
# Method name should have sense
# -k stands for method names execution, -s logs in out put  -v stands for more info metadata
# you can run specific file with py.test <filename>

def test_firstProgram():
  msg = "Hello"
  assert msg == "Hi", "Test failed   because strings do not match"


def test_SecondGreetCreditCard():
  a = 4
  b = 6
  assert a+2 == 6, "Addition do not match"