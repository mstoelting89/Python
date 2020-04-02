from selenium import webdriver
import time

driver = webdriver.Chrome('chromedriver.exe')
driver.get('https://www.autoscout24.de/')

search_field = driver.find_element_by_class_name('react-autocomplete__input')
search_field.click()
time.sleep(2)
search_field = driver.find_elements_by_class_name('react-autocomplete__list-item')


for i in range(1,len(search_field)):
    print(search_field[i].text)


driver.close()