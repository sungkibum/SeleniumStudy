import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

driver = webdriver.Chrome()

driver.get("https://rahulshettyacademy.com/angularpractice/")

# ID, Xpath, CSSSelector, Classname, name, linkText
driver.find_element(By.NAME, "email").send_keys("tjdrlqja5@naver.com")
driver.find_element(By.ID, "exampleInputPassword1").send_keys("123456")
driver.find_element(By.ID, "exampleCheck1").click()

# Xpath - //tagname[@attribute='value']   ->  //input[@type='submit']
# CSS - tagname[attribute='value']   ->  input[type='submit'],   #id, .classname
driver.find_element(By.CSS_SELECTOR, "input[name='name']").send_keys("Rahul")
driver.find_element(By.CSS_SELECTOR, "#inlineRadio1").click()


time.sleep(5)