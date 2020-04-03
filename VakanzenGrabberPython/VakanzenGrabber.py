from selenium import webdriver
import time

class VakanzenGrabber(object):

    def __init__(self,site,suchBegriff):
        self.site = site
        self.suchBegriff = suchBegriff

        # Webdriver wird inizialisiert
        self.__driver = webdriver.Chrome()

    def vakanzenGrabben(self):

        self.__driver.get(self.site)
        suchFeld = self.__driver.find_element_by_xpath("//*[@id='__search']//input[@name= '__search_freetext']")
        suchButton = self.__driver.find_element_by_xpath("//*[@id='__search']//input[@name= '__search_freetext']/..//button")
        suchFeld.send_keys(self.suchBegriff)
        suchButton.click()

        time.sleep(5)

        self.__driver.quit()

vakanzenGrabben = VakanzenGrabber("https://www.freelance.de","Test")
vakanzenGrabben.vakanzenGrabben()