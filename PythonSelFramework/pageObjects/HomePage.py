from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from pageObjects.CheckoutPage import CheckOutPage


class HomePage:

    def __init__(self, driver):
        self.driver = driver

    shop = (By.CSS_SELECTOR, "a[href*='shop']")
    name = (By.CSS_SELECTOR, "[name='name']")
    email = (By.NAME, "email")
    exampleCheck1 = (By.ID, "exampleCheck1")
    gender = (By.ID, "exampleFormControlSelect1")
    submitButton = (By.XPATH, "//input[@value='Submit']")
    successAlert = (By.CSS_SELECTOR, "[class*='alert-success']")

    def shopItems(self):
        self.driver.find_element(*HomePage.shop).click()
        checkOutPage = CheckOutPage(self.driver)
        return checkOutPage

    def getName(self):
        return self.driver.find_element(*HomePage.name)

    def getEmail(self):
        return self.driver.find_element(*HomePage.email)

    def getExampleCheck1(self):
        return self.driver.find_element(*HomePage.exampleCheck1)

    def getGender(self):
        return self.driver.find_element(*HomePage.gender)

    def clickSubmit(self):
        self.driver.find_element(*HomePage.submitButton).click()

    def getSuccessAlertText(self):
        return self.driver.find_element(*HomePage.successAlert).text