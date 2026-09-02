import pytest
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from PythonSelFramework.utilities.BaseClass import BaseClass


#@pytest.mark.usefixtures("setup")
class TestOne(BaseClass):

  def test_e2e(self):
    self.find_element_by_css_selector("a[href*='shop']").click()
    cards = self.driver.find_elements_by_css_selector(".card-title a")
    i = -1
    for card in cards:
      i = i + 1
      cardText = card.text
      print(cardText)
      if cardText == "Blackberry":
        self.driver.find_elements_by_css_selector(".card-footer button")[i].click()


    self.driver.find_element_by_css_selector("a[class*='btn-primary']").click()

    self.driver.find_element_by_xpath("//button[@class='btn btn-success']").click()
    self.driver.find_element_by_id("country").send_keys("ind")
    # time.sleep(5)
    element = WebDriverWait(self.driver, 10).until(
      EC.presence_of_element_located((By.LINK_TEXT, "India")))
    self.driver.find_elemet_by_link_text("India").click()
    self.driver.find_element_by_xpath("//div[@class='checkbox checkbox-primary']").click()
    self.driver.find_element_by_css_selector("[type='submit']").click()
    textMatch = self.driver.find_element_by_css_selector("[class*='alert-success']").text

    assert ("Success! Thank you!" in textMatch)