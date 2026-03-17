import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

driver = webdriver.Chrome()
driver.implicitly_wait(2)   #페이지에 아무 요소도 뜨지 않으면 뜰 때까지 최대 5초 대기(암시적 대기)
correctProducts = ["Cucumber - 1 Kg", "Raspberry - 1/4 Kg", "Strawberry - 1/4 Kg"]

driver.get("https://rahulshettyacademy.com/seleniumPractise/#/")

driver.find_element(By.CSS_SELECTOR, ".search-keyword").send_keys("ber")
time.sleep(2)

products = driver.find_elements(By.CSS_SELECTOR, "div h4")
aaa = []

for product in products:
    aaa.append(product.text)

assert  aaa == correctProducts

elements = driver.find_elements(By.XPATH, "//div[@class='products']/div")
assert len(elements) > 0

for element in elements:
    element.find_element(By.XPATH, "div/button").click()


driver.find_element(By.XPATH, "//img[@alt='Cart']").click() #15
driver.find_element(By.XPATH, "//button[text()='PROCEED TO CHECKOUT']").click()

#SUM Validation
sum = 0
total = driver.find_elements(By.XPATH, "//td[5]/p[@class='amount']")
for price in total:
    sum += int(price.text)

print(sum)
totalAmount = int(driver.find_element(By.XPATH, "//span[@class='totAmt']").text)

assert totalAmount == sum

driver.find_element(By.CSS_SELECTOR, ".promoCode").send_keys("rahulshettyacademy")
driver.find_element(By.XPATH, "//div/button[@class = 'promoBtn']").click()
wait = WebDriverWait(driver, 10)
wait.until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, ".promoInfo")))
print(driver.find_element(By.CSS_SELECTOR, ".promoInfo").text)
afterDiscount = float(driver.find_element(By.XPATH, "//span[@class='discountAmt']").text)
assert totalAmount > afterDiscount



time.sleep(5)
