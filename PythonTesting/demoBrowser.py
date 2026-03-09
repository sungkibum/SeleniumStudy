from selenium import webdriver

#chrome driver
from selenium.webdriver.chrome.service import Service
# -- Chrome
driver = webdriver.Chrome()

# -- Firefox
# service_obj = Service()
# driver = webdriver.Firefox()

# -- MS Edge
#driver = webdriver.Edge()

driver.get("https://rahulshettyacademy.com")
print(driver.title)
print(driver.current_url)
driver.get("https://rahulshettyacademy.com/seleniumPractise/#/")
driver.minimize_window()
driver.maximize_window()
driver.back()
driver.refresh()
driver.forward()
driver.close()