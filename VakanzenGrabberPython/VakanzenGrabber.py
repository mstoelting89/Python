from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time

##############################################################################################################################################
#
#   Klasse zum Durchlaufen der Webseite von Freelance.de und suchen nach bestimmten Suchbegriffen
#   danach aufrufen der einzelnen Ergebisse
#
##############################################################################################################################################
class VakanzenGrabber():

    ############################################################
    #   Constructor mit Übergabe von URL, Suchbegriff und
    #   seitentitel
    ############################################################
    def __init__(self,site,suchBegriff,seitenTitel):
        self.site = site
        self.suchBegriff = suchBegriff
        self.seitenTitel = seitenTitel

        ##############################
        # Webdriver wird inizialisiert
        ##############################
        self.driver = webdriver.Chrome(ChromeDriverManager().install())

    ############################################################
    #   Funktion definiert die verschiedenen Möglichkeiten zum
    #   finden von Webelementen
    ############################################################
    def webelement_finden(self, pstrElementType, pstrElementName):
        if pstrElementType == "xpath":
            element = self.driver.find_element_by_xpath(pstrElementName)
            return element

        elif pstrElementType == "xpaths":
            element = self.driver.find_elements_by_xpath(pstrElementName)
            return element

        elif pstrElementType == "tagName":
            element = self.driver.find_element_by_tag_name(pstrElementName)
            return element

    ############################################################
    #   Seite wird aufgerufen und es wird geprüft ob die Seite
    #   angezeigt wurde. Danach wird der Suchbegriff in ein
    #   Suchfeld eingegeben und die Schaltfläche "Suchen" wird
    #   getätigt
    ############################################################
    def vakanzenGrabbenHauptseite(self):

        ##############################
        # Aufrufen der Seite
        ##############################
        self.driver.get(self.site)

        ##############################
        # Stimmt Seitentitel überein?
        ##############################
        if self.seitenTitel == self.driver.title:

            ##############################
            # Heraussuchen des Suchfeldes
            # und des Buttons
            ##############################
            #suchFeld = self.driver.find_element_by_xpath("//*[@id='__search']//input[@name= '__search_freetext']")

            suchFeld = self.webelement_finden("xpath","//*[@id='__search']//input[@name= '__search_freetext']")
            suchButton = self.webelement_finden("xpath","//*[@id='__search']//input[@name= '__search_freetext']/..//button")

            ##############################
            # Eingeben des Suchbegriffes
            ##############################
            suchFeld.send_keys(self.suchBegriff)
            suchButton.click()
            return True

        ##############################
        # Wenn keine Übereinstimmung
        ##############################
        else:
            print("Der Seitentitel '" + self.seitenTitel + "' stimmt nicht mit dem Originalseitentilt '" + self.driver.title + "' überein")
            self.driver.quit()
            return False

    ############################################################
    #   Durchlaufen der Ergebnisseite
    ############################################################
    def vakanzenGrabbenSuchseite(self):

        ##############################
        # Anzahl der Sucheinträge wird
        # gespeichert
        ##############################
        anzahlSuchPosition = len(self.webelement_finden("xpaths",'(//*[contains(@id,"project_link")])'))

        ##############################
        # Schleife zum Durchlaufen
        # jedes einzelnen Ergebnisses,
        # öffnen und wieder zurück zur
        # Ergebnissseite
        ##############################
        for i in range(1,anzahlSuchPosition):

            ##############################
            # Titellink wird an Stelle i
            # gewählt
            ##############################
            suchPosition = self.webelement_finden("xpath",'(//*[contains(@id,"project_link")])[' + str(i) + ']')
            print(suchPosition)

            ##############################
            # Titel wird geklickt
            ##############################
            suchPosition.click()

            ##############################
            # Nutzen der Browser-Zurück
            # Funktion
            ##############################
            self.driver.back()

            ##############################
            # 1 sec warten
            ##############################
            time.sleep(1)

            ##############################
            # Nach 5 Durchläufen wird
            # abgebrochen
            ##############################
            if i == 5:
                break

        ##############################
        # 5 sec Warten
        ##############################
        time.sleep(5)

        ##############################
        # Schließen des Browsers
        ##############################
        self.driver.quit()