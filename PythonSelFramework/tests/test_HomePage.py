import pytest

from utilities.BaseClass import BaseClass
from pageObjects.HomePage import HomePage


class TestHomePage(BaseClass):

    def test_formSubmission(self, getData):
        homePage = HomePage(self.driver)
        homePage.getName().send_keys(getData[0])
        homePage.getEmail().send_keys(getData[1])
        homePage.getExampleCheck1().click()
        self.selectOptionByText(homePage.getGender(), getData[2])
        homePage.clickSubmit()

        alertText = homePage.getSuccessAlertText()
        assert ("Success" in alertText)
        self.driver.refresh()

    @pytest.fixture(params=[("Rahul", "shetty", "Male"), ("Anshika", "shetty", "Female")])
    def getData(self, request):
        return request.param