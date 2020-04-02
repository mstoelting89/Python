from selenium import webdriver

driver = webdriver.Chrome('chromedriver.exe')

driver.get('https://www.freelance.de')

driver.quit()