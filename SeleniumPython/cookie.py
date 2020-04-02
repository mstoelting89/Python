from selenium import webdriver

driver = webdriver.Chrome('chromedriver.exe')

driver.get('https://www.googlcom/')
cookie = {'name' : 'token, value' : '2342342343'}
driver.add_cookie(cookie)