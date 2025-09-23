from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import time

options = webdriver.FirefoxOptions()
driver = webdriver.Firefox(options=options)
driver.get("https://www.saucedemo.com")

login = driver.find_element(By.ID, 'user-name')
login.send_keys('performance_glitch_user')
password = driver.find_element(By.ID, 'password')
password.send_keys('secret_sauce')
button = driver.find_element(By.ID, 'login-button').click()

select_element = driver.find_element(By.CLASS_NAME, 'product_sort_container')
select = Select(select_element)
az = driver.find_element(By.CSS_SELECTOR, "option[value=az]")
select.select_by_value('az')
assert az.is_selected()

add_to_cart = driver.find_element(By.NAME, 'add-to-cart-sauce-labs-onesie').click()

time.sleep(5)
driver.quit()