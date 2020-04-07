from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time

class VakanzenGrabber():

    def __init__(self,site,suchBegriff):
        self.site = site
        self.suchBegriff = suchBegriff

        # Webdriver wird inizialisiert
        self.__driver = webdriver.Chrome(ChromeDriverManager().install())

    def vakanzenGrabben(self):

        self.__driver.get(self.site)
        suchFeld = self.__driver.find_element_by_xpath("//*[@id='__search']//input[@name= '__search_freetext']")
        suchButton = self.__driver.find_element_by_xpath("//*[@id='__search']//input[@name= '__search_freetext']/..//button")

        suchFeld.send_keys(self.suchBegriff)
        suchButton.click()


        for i in range(1,4):
            suchPosition = self.__driver.find_element_by_xpath('(//*[contains(@id,"project_link")])[' + str(i) + ']')
            print(suchPosition)
            suchPosition.click()
            self.__driver.back()
            time.sleep(2)

        time.sleep(5)
        #self.__driver.quit()

vakanzenGrabben = VakanzenGrabber("https://www.freelance.de","Test Manager")
vakanzenGrabben.vakanzenGrabben()
