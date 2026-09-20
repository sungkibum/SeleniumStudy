from selenium.webdriver.support.select import Select

from utilities.BaseClass import BaseClass
from pageObjects.HomePage import HomePage


class TestHomePage(BaseClass):

    def test_formSubmission(self):
        homePage = HomePage(self.driver)
        homePage.getName().send_keys("Rahul")
        homePage.getEmail().send_keys("shetty")
        homePage.getExampleCheck1().click()
        sel = Select(homePage.getGender())
        sel.select_by_visible_text("Male")
        homePage.clickSubmit()

        alertText = homePage.getSuccessAlertText()
        assert ("Success" in alertText)