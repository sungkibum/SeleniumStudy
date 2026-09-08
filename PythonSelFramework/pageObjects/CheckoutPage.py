from selenium.webdriver.common.by import By


class CheckOutPage:

    def __init__(self, driver):
        self.driver = driver

    #driver.find_elements(By.CSS_SELECTOR, ".card-title a")
    cardTitle = (By.CSS_SELECTOR, ".card-title a")
    #driver.find_elements(By.CSS_SELECTOR, ".card-footer button")[i].click()
    cardFooter = (By.CSS_SELECTOR, ".card-footer button")
    #driver.find_element(By.XPATH, "//button[@class='btn btn-success']").click()
    checkOut = (By.XPATH, "//button[@class='btn btn-success']")

    def getCardTitles(self):
        return self.driver.find_elements(*CheckOutPage.cardTitle)

    def getCardFooter(self):
        return self.driver.find_elements(*CheckOutPage.cardFooter)

    def checkOutItems(self):
        return self.driver.find_element(*CheckOutPage.checkOut)
