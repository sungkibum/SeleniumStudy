import time

from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.implicitly_wait(5)   #페이지에 아무 요소도 뜨지 않으면 뜰 때까지 최대 5초 대기(암시적 대기)

driver.get("https://rahulshettyacademy.com/seleniumPractise/#/")

driver.find_element(By.CSS_SELECTOR, ".search-keyword").send_keys("ber")
time.sleep(2)

elements = driver.find_elements(By.XPATH, "//div[@class='products']/div")
assert len(elements) > 0

for element in elements:
    element.find_element(By.XPATH, "div/button").click()


driver.find_element(By.XPATH, "//img[@alt='Cart']").click()
driver.find_element(By.XPATH, "//button[text()='PROCEED TO CHECKOUT']").click()
driver.find_element(By.CSS_SELECTOR, ".promoCode").send_keys("rahulshettyacademy")
driver.find_element(By.XPATH, "//div/button[@class = 'promoBtn']").click()

print(driver.find_element(By.CSS_SELECTOR, ".promoInfo").text)

time.sleep(5)
