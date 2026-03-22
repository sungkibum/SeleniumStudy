from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Firefox()
driver.implicitly_wait(5)
driver.get("https://the-internet.herokuapp.com/windows")


driver.find_element(By.LINK_TEXT, "Click Here").click() #새 창 열림
windowsOpened = driver.window_handles

driver.switch_to.window(windowsOpened[1])
print(driver.find_element(By.TAG_NAME, "h3").text)
driver.close()
driver.switch_to.window(windowsOpened[0])
assert "Opening a new window" == driver.find_element(By.XPATH, "//h3").text

driver.quit()