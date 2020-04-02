from selenium import webdriver
import time

class search_Project_Names(object):
    def __init__(self,content):
        self.content = content

    def filterTitles(self):
        for i in range(1,len(self.content)):
            print(self.content[i].find_element_by_tag_name('a').text)

    def filterDetails(self):
        for i in range(1,len(self.content)):
            print(self.content[i].find_element_by_class_name('freelancer-more').text)

    def useLink(self):
        for i in range(1,len(self.content)):
            link = self.content[i].find_element_by_tag_name('a')
            link.click()

driver = webdriver.Chrome('chromedriver.exe')
driver.get('https://www.freelance.de/')

searchObject = 'Tester'

search_projects = driver.find_element_by_class_name('form-control')
search_projects.send_keys(searchObject)
search_projects.submit()

project_list = driver.find_elements_by_class_name('freelancer-content')

search_Project_Names(project_list).useLink()

driver.quit()

