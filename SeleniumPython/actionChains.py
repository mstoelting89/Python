import unittest
from selenium import webdriver
from selenium.webdriver import ActionChains

driver = webdriver.Chrome('chromedriver.exe')

ac = ActionChains(driver)
ac. 