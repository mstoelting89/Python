from selenium import webdriver
import time

from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome('chromedriver.exe')
driver.get('https://www.google.de/xhtml')

#search_field = driver.find_element_by_name('q')

search_div = driver.find_elements_by_tag_name('div')

for i in search_div:
    print(i.is_displayed())

search_field = driver.find_elements_by_tag_name('input')

for i in search_field:
    if i.is_displayed() and i.is_enabled():
        i.send_keys('google')
        i.submit()
        break


driver.quit()