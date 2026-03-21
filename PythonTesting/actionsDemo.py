import time

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()

driver.implicitly_wait(5)
driver.maximize_window()
driver.get("https://rahulshettyacademy.com/AutomationPractice/")
action = ActionChains(driver)

# action.double_click()   #더블클릭
# action.click_and_hold() #길게 누르기
# action.context_click()  #우클릭
# action.drag_and_drop()  #끌어다 놓기
action.move_to_element(driver.find_element(By.ID, "mousehover")).perform()
# action.context_click(driver.find_element(By.LINK_TEXT, "Top")).perform()
# action.move_to_element(driver.find_element(By.LINK_TEXT, "Reload")).click().perform()
driver.find_element(By.LINK_TEXT, "Reload").click()

time.sleep(5)