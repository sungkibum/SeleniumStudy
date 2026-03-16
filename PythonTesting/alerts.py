import time

from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()

driver.get("https://rahulshettyacademy.com/AutomationPractice/")

name = 'rahul'

driver.find_element(By.XPATH, "//input[@id='name']").send_keys("rahul")
driver.find_element(By.CSS_SELECTOR,"input[value='Alert']").click()
alert = driver.switch_to.alert
alertText = alert.text
print(alertText)
assert name in alertText
alert.accept()
#alert.dismiss()

time.sleep(5)
