from selenium import webdriver
import time

driver = webdriver.Chrome('chromedriver.exe')

driver.get('https://www.google.de/')
time.sleep(5)

search_field = driver.find_element_by_name('q')

search_field.send_keys('google')
search_field.submit()

driver.quit()

