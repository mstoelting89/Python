from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ExpectedCondition
from selenium.webdriver.common.by import By

driver = webdriver.Chrome('chromedriver.exe')
driver.implicitly_wait(5)
driver.get('https://www.google.de/xhtml')

myelement = driver.find_element_by_name('q')