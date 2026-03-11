import time

from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()

driver.get("https://rahulshettyacademy.com/dropdownsPractise/")

driver.find_element(By.ID, "autosuggest").send_keys("ind")
time.sleep(2)
countries = driver.find_elements(By.CSS_SELECTOR, "li[class='ui-menu-item'] a")
print(len(countries))   # 3 countries 리스트의 크기

for country in countries:
    if country.text == "India":
        country.click()
        break

# print(driver.find_element(By.ID, "autosuggest").text)   # 유효성 검증을 시도했으나 text는 웹사이트가 처음 로딩될때부터 있어야하기때문에 실패
assert driver.find_element(By.ID, "autosuggest").get_attribute("value") == "India"


time.sleep(5)