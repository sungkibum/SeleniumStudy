import time

from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()

driver.get("https://rahulshettyacademy.com/AutomationPractice/")

checkboxes = driver.find_elements(By.XPATH, "//input[@type='checkbox']")

print(len(checkboxes))

for checkbox in checkboxes:
    if checkbox.get_attribute("value") == 'option2':
        checkbox.click()
        checkbox.is_selected()
        break

radioButtons = driver.find_elements(By.XPATH, "//input[@type='radio']")

print(len(radioButtons))

for radioButton in radioButtons:
    if radioButton.get_attribute("value") == 'radio2':
        radioButton.click()
        radioButton.is_selected()

        break

driver.find_element(By.CSS_SELECTOR, "#hide-textbox").click()

driver.find_element(By.CSS_SELECTOR, "#displayed-text").is_displayed()


time.sleep(5)