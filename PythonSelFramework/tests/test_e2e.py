import pytest
from selenium import webdriver


@pytest.mark.usefixtures("setup")
class TestOne:

  def test_e2e(self):
    driver.find_element_by_css_selector("a[href*='shop']").click()
    cards = driver.find_elements_by_css_selector("/card-title a")
    i = -1
    for card in cards:
      i = i + 1
      cardText = card.text
      print(cardText)
      if cardText == "Blackberry":
        driver.find_elements_by_css_selector(".card-footer button")[i].click()


    driver.find_element_by_css_selector("a[class*='btn-primary']").click()