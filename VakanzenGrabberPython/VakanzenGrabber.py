from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import csvData
import datetime
import logData

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
        # Log Datei wird erstellt
        ##############################
        logName = "logData/Log_" + str(datetime.datetime.now())
        logName = logName.replace(":", "-")
        logName = logName.replace(".", "-")
        logName = logName.replace(" ", "_")

        self.log = logData.logData(logName)

        ##############################
        # Webdriver wird inizialisiert
        ##############################
        #self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver = webdriver.Chrome('chromedriver.exe')
        self.log.logSchreiben("Webdriver wurde initialisiert")

        ##############################
        # CSV Datei wird geöffnet
        ##############################
        resultName = "Results/Ausgabe"
        self.result = csvData.CSV_Daten(resultName)

    ############################################################
    #   Funktion definiert die verschiedenen Möglichkeiten zum
    #   finden von Webelementen
    ############################################################
    def webelement_finden(self, pstrElementType, pstrElementName):
        #Uppercase einfügen
        if pstrElementType.lower() == "xpath":
            try:
                element = self.driver.find_element_by_xpath(pstrElementName)
                return element
            except Exception as e:
                self.log.logSchreiben("Beim finden des Webelementes ist ein Fehler aufgetreten: " + str(e))

        elif pstrElementType.lower() == "xpaths":
            try:
                element = self.driver.find_elements_by_xpath(pstrElementName)
                return element
            except Exception as e:
                self.log.logSchreiben("Beim finden des Webelementes ist ein Fehler aufgetreten: " + str(e))

        elif pstrElementType.lower() == "tagname":
            try:
                element = self.driver.find_element_by_tag_name(pstrElementName)
                return element
            except Exception as e:
                self.log.logSchreiben("Beim finden des Webelementes ist ein Fehler aufgetreten: " + str(e))

        else:
            self.log.logSchreiben("Der Elementtyp " + pstrElementType + " wurde nicht gefunden.")
            return None

    ############################################################
    #   Funktion definiert die verschiedenen Möglichkeiten zum
    #   setzen von Webelementen
    ############################################################
    def webelement_setzen(self, pstrElement, pstrWert):
        #prüfen ob element none ist... + try catch in if abfrage
        try:
            pstrElement.send_keys(pstrWert)
            self.log.logSchreiben("Das Element '" + str(pstrElement.get_attribute("name")) + "' wird auf den Wert '" + str(pstrWert) + "' gesetzt.")
        except Exception as e:
            self.log.logSchreiben("Beim setzen des Elementes ist ein Fehler aufgetreten: " + e)

    ############################################################
    #   Funktion definiert die Möglichkeiten zum
    #   klicken von Webelementen
    ############################################################
    def webelement_klicken(self,pstrElement):
        try:
            pstrElement.click()
            return True
        except Exception as e:
            self.log.logSchreiben("Beim klicken des Elementes '" + str(pstrElement.get_attribute("name")) + "' ist ein Fehler aufgetreten: " + str(e))
            return False

    ############################################################
    #   Funktion definiert browser back
    ############################################################
    def webelement_Back(self):
        try:
            self.driver.back()
            return True
        except Exception as e:
            self.log.logSchreiben("Beim Rücksprung ist ein Fehler aufgetreten: " + e)
            return False

    ############################################################
    #   Funktion definiert browser quit
    ############################################################
    def webelement_quit(self):
        try:
            self.driver.quit()
            return True
        except Exception as e:
            self.log.logSchreiben("Beim Schließen des Browsers ist ein Fehler aufgetreten: " + e)
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
        try:
            self.driver.get(self.site)
            self.driver.maximize_window()
            self.log.logSchreiben("Webseite übergeben: " + str(self.site))
        except Exception as e:
            self.log.logSchreiben("Beim Aufrufen der Website " + str(self.site) + " ist ein Fehler aufgetreten: " + str(e))

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
            try:
                self.webelement_setzen(suchFeld,self.suchBegriff)
            except Exception as e:
                self.log.logSchreiben("Bei der Eingabe und der Ausführung der Suche ist ein Fehler aufgetreten: " + str(e))

            if self.webelement_klicken(suchButton) == True:
                self.log.logSchreiben("Der Suchbutton wurde erfolgreich geklickt")
            else:
                self.log.logSchreiben("Beim klicken vom Suchbutton ist ein Fehler aufgetreten")

            ##############################
            # Methode gibt True zurück
            # wenn erfolgreich durchgelaufen
            ##############################
            return True

        ##############################
        # Wenn keine Übereinstimmung
        ##############################
        else:
            self.log.logSchreiben("Der Seitentitel '" + self.seitenTitel + "' stimmt nicht mit dem Originalseitentilt '" + self.driver.title + "' überein")
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
        if anzahlSuchPosition == 1:
            anzahlSuchPosition = 2

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

            ##############################
            # Titel des Sucheintrages
            # wird gespeichert und Leer-
            # zeichen entfernt
            ##############################
            suchPositionText = str(suchPosition.get_attribute("text")).strip()
            suchPositionText = suchPositionText.replace(" ","")

            time.sleep(2)

            ##############################
            # Titel wird geklickt
            ##############################
            if self.webelement_klicken(suchPosition) == True:

                ##############################
                # Titel der Ergebnisseite wird
                # gespeichert und Leerzeichen
                # entfernt
                ##############################
                titelErgebnis = self.webelement_finden("xpath", "//div[@class='panel-body project-header panel-white']//h1")
                titelErgebnis = str(titelErgebnis.text)
                titelErgebnis = titelErgebnis.replace(" ","")

                ############################################################
                # Wenn der Seitentitel mit dem Sucheintrag auf der
                # Ergebnisseite übereinstimmt, werden weitere Daten in ein
                # Array gespeichert und in eine CSV Datei geschrieben
                ############################################################
                if titelErgebnis == suchPositionText:
                    self.log.logSchreiben("Die Seite " + titelErgebnis + " wurde erfolgreich aufgerufen")

                    ############################################################
                    # Vordefinition der in die CSV zu schreibenden Variablen
                    ############################################################
                    von = "Keine Angaben"
                    bis = "Keine Angaben"
                    standort = "Keine Angaben"
                    preis = "Keine Angaben"
                    remote = "Keine Angaben"
                    lastUpdate = "Keine Angaben"
                    reference = "Keine Angaben"

                    ############################################################
                    # Durchlaufen der Tabelle auf der Website
                    ############################################################
                    for f in range(1,3):
                        for p in range(1,4):

                            ############################################################
                            # Filtern des KlassenNamens der entsprechenden Tabellen-
                            # einträge
                            ############################################################
                            try:
                                wert = self.webelement_finden("xpath","//div[@class='project-right-content']//div[" + str(f) + "]//p[" + str(p) + "]")
                            except Exception as e:
                                self.log.logSchreiben("Es konnte kein Webelement(1) in der Tabelle gefunden werden: " + str(e))

                            try:
                                wert2 = wert.get_property("children")
                            except Exception as e:
                                self.log.logSchreiben("Es konnte kein Webelement(2) in der Tabelle gefunden werden: " + str(e))

                            try:
                                wert3 = wert2[0].get_attribute("className")
                            except Exception as e:
                                self.log.logSchreiben("Es konnte kein Webelement(3) in der Tabelle gefunden werden: " + str(e))

                            try:
                                ############################################################
                                # Abfragen zu welcher Klasse der in "wert" gespeicherten
                                # Daten gehören - danach abspeichern in der entsprechendne
                                # Variable
                                ############################################################
                                if wert3 == "fa fa-sign-in":
                                    von = str(wert.get_attribute("innerText"))
                                elif wert3 == "fa fa-sign-out":
                                    bis = str(wert.get_attribute("innerText"))
                                elif wert3 == "fa fa-globe":
                                    standort = str(wert.get_attribute("innerText"))
                                elif wert3 == "fa fa-money":
                                    preis = str(wert.get_attribute("innerText"))
                                elif wert3 == "fa fa-home":
                                    remote = str(wert.get_attribute("innerText"))
                                elif wert3 == "fa fa-refresh":
                                    lastUpdate = str(wert.get_attribute("innerText"))
                                elif wert3 == "fa fa-tag":
                                    reference = str(wert.get_attribute("innerText"))
                            except Exception as e:
                                self.log.logSchreiben("Es konnte kein Webelement(4) in der Tabelle gefunden werden: " + str(e))

                    ############################################################
                    # Übergabe der Ergebnisse als Array in die CSV Datei
                    ############################################################
                    timestamp = str(datetime.datetime.now())
                    ergebnis = [timestamp,titelErgebnis,von,bis,standort,preis,remote,lastUpdate,reference]
                    self.result.csvSchreiben(ergebnis)
                else:
                    self.log.logSchreiben("Die Seite '" + titelErgebnis + "' stimmt nicht mit '" + suchPositionText + "' überein")

            else:
                self.log.logSchreiben("Beim klicken der Suchposition ist ein Fehler aufgetreten")

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
            # Nach 1 Durchläufen wird
            # abgebrochen
            ##############################
            #if i == 2:
            #    break

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
        self.log.logSchreiben("------ Seite 1 wird  anaylsiert ------")
        VakanzenGrabber.vakanzenGrabbenSuchseite(self)

        ##############################
        # Speichern der Seitenzahlen
        # am unteren Ende der Seite
        ##############################
        try:
            laengeArraySeiten = len(self.webelement_finden("xpaths", "//ul[@class='pagination']/li")) - 1
            letzteSeite = self.webelement_finden("xpath","//div[@id='pagination']//li[" + str(laengeArraySeiten) + "]//a[1]")
        except Exception as e:
            self.log.logSchreiben("Die Seitenzahl konnte nicht gefunden werden " + str(e))

        ##############################
        # Schleife zum Durchlaufen
        # jeder einzelnen Seite
        ##############################
        if letzteSeite:
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
                    self.log.logSchreiben("----Seite " + str(i + 1) + " wird analysiert ----")
                    VakanzenGrabber.vakanzenGrabbenSuchseite(self)

        ##############################
        # Schließen des Browsers,
        # der CSV datei und der Log
        # Datei
        ##############################
        self.webelement_quit()
        self.log.logSchreiben("Die Seite wurde geschlossen")

        self.result.csvClose()
        self.log.close()

