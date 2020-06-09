from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
# ToDo 1. Speicherung der Titel in einer .csv Datei - Hierfür extra Klasse erstellen
# ToDo 2. Speicherung der LogDaten in einer LogDatei - Hierfür extra Klasse erstellen

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
        #self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver = webdriver.Chrome('chromedriver.exe')
        print("Webdriver wurde initialisiert")

    ############################################################
    #   Funktion definiert die verschiedenen Möglichkeiten zum
    #   finden von Webelementen
    ############################################################
    def webelement_finden(self, pstrElementType, pstrElementName):
        #Uppercase einfügen
        if pstrElementType.lower() == "xpath":
            element = self.driver.find_element_by_xpath(pstrElementName)
            #print("Der XPath '" + str(element) + "' wurde aufgerufen")
            return element

        elif pstrElementType.lower() == "xpaths":
            element = self.driver.find_elements_by_xpath(pstrElementName)
            #print("Es wurden mehrere XPathes zurückgegeben " + str(element))
            return element

        elif pstrElementType.lower() == "tagname":
            element = self.driver.find_element_by_tag_name(pstrElementName)
            #print("Der Tag Name '" + str(element) + "' wurde aufgerufen")
            return element

        else:
            print("Der Elementtyp " + pstrElementType + " wurde nicht gefunden.")
            return None

    ############################################################
    #   Funktion definiert die verschiedenen Möglichkeiten zum
    #   setzen von Webelementen
    ############################################################
    def webelement_setzen(self, pstrElement, pstrWert):
        #prüfen ob element none ist... + try catch in if abfrage
        try:
            pstrElement.send_keys(pstrWert)
            print("Das Element '" + str(pstrElement.get_attribute("name")) + "' wird auf den Wert '" + str(pstrWert) + "' gesetzt.")
        except Exception as e:
            print("Beim setzen des Elementes ist ein Fehler aufgetreten: " + e)

    ############################################################
    #   Funktion definiert die Möglichkeiten zum
    #   klicken von Webelementen
    ############################################################
    def webelement_klicken(self,pstrElement):
        try:
            pstrElement.click()
            return True
        except Exception as e:
            print("Beim klicken des Elementes '" + str(pstrElement.get_attribute("name")) + "' ist ein Fehler aufgetreten: " + e)
            return False

    ############################################################
    #   Funktion definiert browser back
    ############################################################
    def webelement_Back(self):
        try:
            self.driver.back()
            return True
        except Exception as e:
            print("Beim Rücksprung ist ein Fehler aufgetreten: " + e)
            return False

    ############################################################
    #   Funktion definiert browser quit
    ############################################################
    def webelement_quit(self):
        try:
            self.driver.quit()
            return True
        except Exception as e:
            print("Beim Schließen des Browsers ist ein Fehler aufgetreten: " + e)
            return False

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
        self.driver.maximize_window()
        print("Log: Webseite übergeben: " + str(self.site))

        ##############################
        # Stimmt Seitentitel überein?
        ##############################
        if self.seitenTitel == self.driver.title:

            ##############################
            # Heraussuchen des Suchfeldes
            # und des Buttons
            ##############################
            suchFeld = self.webelement_finden("xpath","//*[@id='__search']//input[@name= '__search_freetext']")
            suchButton = self.webelement_finden("xpath","//*[@id='__search']//input[@name= '__search_freetext']/..//button")

            ##############################
            # Eingeben des Suchbegriffes
            ##############################
            self.webelement_setzen(suchFeld,self.suchBegriff)

            if self.webelement_klicken(suchButton) == True:
                print("Der Suchbutton wurde erfolgreich geklickt")
            else:
                print("Beim klicken vom Suchbutton ist ein Fehler aufgetreten")

            ##############################
            # Methode gibt True zurück
            # wenn erfolgreich durchgelaufen
            ##############################
            return True

        ##############################
        # Wenn keine Übereinstimmung
        ##############################
        else:
            print("Der Seitentitel '" + self.seitenTitel + "' stimmt nicht mit dem Originalseitentilt '" + self.driver.title + "' überein")
            self.webelement_quit()
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
            suchPositionText = str(suchPosition.get_attribute("text")).strip()

            time.sleep(2)

            ##############################
            # Titel wird geklickt
            ##############################
            if self.webelement_klicken(suchPosition) == True:
                titelErgebnis = self.webelement_finden("xpath", "//div[@class='panel-body project-header panel-white']//h1")

                if titelErgebnis.text == suchPositionText:
                    print("Die Seite " + titelErgebnis.text + " wurde erfolgreich aufgerufen")
                else:
                    print("Die Seite '" + titelErgebnis.text + "' stimmt nicht mit '" + suchPositionText + "' überein")

            else:
                print("Beim klicken der Suchposition ist ein Fehler aufgetreten")

            #suchPosition.click()
            time.sleep(2)

            ##############################
            # Nutzen der Browser-Zurück
            # Funktion
            ##############################
            self.webelement_Back()

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

    ############################################################
    #   Methode definiert Sprung auf die nächste Seite
    ############################################################
    def naechste_seite(self):

        ##############################
        # Ausführung der Suchmethode
        # auf der ersten Seite
        ##############################
        print("------ Seite 1 wird  anaylsiert ------")
        VakanzenGrabber.vakanzenGrabbenSuchseite(self)

        ##############################
        # Speichern der Seitenzahlen
        # am unteren Ende der Seite
        ##############################
        laengeArraySeiten = len(self.webelement_finden("xpaths", "//ul[@class='pagination']/li")) - 1
        letzteSeite = self.webelement_finden("xpath","//div[@id='pagination']//li[" + str(laengeArraySeiten) + "]//a[1]")
        #pfeil_naechste_seite = self.webelement_finden("xpath","//div[@id='pagination']//li[" + str(len(self.webelement_finden("xpaths", "//ul[@class='pagination']/li"))) + "]//a[1]")

        ##############################
        # Schleife zum Durchlaufen
        # jeder einzelnen Seite
        ##############################
        for i in range(1,int(letzteSeite.get_attribute("innerHTML"))):
            ##############################
            # Speichern der Position
            # des "Next"-Pfeils
            ##############################
            pfeil_naechste_seite = self.webelement_finden("xpath", "//div[@id='pagination']//li[" + str(len(self.webelement_finden("xpaths", "//ul[@class='pagination']/li"))) + "]//a[1]")

            ##############################
            # Durchführung der Methode
            # vakanzenGrabbenSuchseite
            # fuer jede Seite
            ##############################
            if self.webelement_klicken(pfeil_naechste_seite) == True:
                print("----Seite " + str(i + 1) + " wird analysiert ----")
                VakanzenGrabber.vakanzenGrabbenSuchseite(self)


        ##############################
        # Schließen des Browsers
        ##############################
        self.webelement_quit()

        print("Die Seite wurde geschlossen")