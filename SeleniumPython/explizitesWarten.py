from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ExpectedCondition
from selenium.webdriver.common.by import By

class has_css_class(object):
    def __init__(self,locator, css):
        self.locator = locator
        self.css = css

    def __call__(self, driver):
        element = driver.find_element(*self.locator)
        if self.css in element.get_attribute("class"):
            return element
        else:
            return False

driver = webdriver.Chrome('chromedriver.exe')
driver.get('https://www.google.de/xhtml')

try:
    element = WebDriverWait(driver, 5).until(has_css_class((By.NAME, "q"), "gsfi"))
    element.send_keys("google")
    time.sleep(5)
finally:
    driver.quit()