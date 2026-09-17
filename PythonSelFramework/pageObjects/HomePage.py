from selenium.webdriver.common.by import By

from PythonTesting.demoBrowser import driver
from pageObjects.CheckoutPage import CheckOutPage


class HomePage:

    def __init__(self, driver):
        self.driver = driver


    shop = (By.CSS_SELECTOR, "a[href*='shop']")
    name = (By.CSS_SELECTOR, "[name='name']")
    email = (By.NAME, "email")
    exampleCheck1 = (By.ID, "exampleCheck1")

    def shopItems(self):
        self.driver.find_element(*HomePage.shop).click()
        checkOutPage = CheckOutPage(self.driver)
        return checkOutPage
        #driver.find_element(By.CSS_SELECTOR, "a[href*='shop']")

    def getName(self):
        return self.driver.find_element(*HomePage.name)

    def getEmail(self):
        return self.driver.find_element(*HomePage.email)

    def getExampleCheck1(self):
        return self.driver.find_element(*HomePage.exampleCheck1)