from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from PythonTesting.locators import driver
from pageObjects.HomePage import HomePage
from utilities.BaseClass import BaseClass

class TestHomePage(BaseClass):

    def test_formSubmission(self):

        homePage = HomePage(self.driver)
        homePage.getName().send_keys("Rahul")
        homePage.getEmail().send_keys("shetty")
        homePage.getExampleCheck1().click()
        sel = Select(driver.find_element(By.ID, "exampleFormControlSelect1"))
        sel.select_by_visible_text("Male")
        driver.find_element(By.XPATH, "//input[@value='Submit']").click()

        alertText = driver.find_element(By.CSS_SELECTOR, "[class*='alert-success']").text

        assert ("Success" in alertText)
