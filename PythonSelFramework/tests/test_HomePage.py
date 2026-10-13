import pytest

from TestData.HomePageData import HomePageData
from utilities.BaseClass import BaseClass
from pageObjects.HomePage import HomePage


class TestHomePage(BaseClass):

    def test_formSubmission(self, getData):
        log = self.getLogger()
        homePage = HomePage(self.driver)
        log.info("first name is "+getData["firstname"])
        homePage.getName().send_keys(getData["firstname"])
        homePage.getEmail().send_keys(getData["lastname"])
        homePage.getExampleCheck1().click()
        self.selectOptionByText(homePage.getGender(), getData["gender"])
        homePage.clickSubmit()

        alertText = homePage.getSuccessAlertText()
        assert ("Success" in alertText)
        self.driver.refresh()

    @pytest.fixture(params=HomePageData.test_HomePage_data)
    def getData(self, request):
        return request.param