import datetime
import pytest
import subprocess
import csv
import os
import time
import Classes.Logging
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from os import path
from selenium.webdriver.common.action_chains import ActionChains
#from webdriver_manager.chrome import ChromeDriverManager
#from webdriver_manager.firefox import GeckoDriverManager

# Basisadresse zur Jira
# dient zum erzeugen der korrekten URL zum Akzaptanzkriterium
jira_base_url = "https://jira.lak.local:8443/browse/"

# Anzahl der Kopfzeilen innerhalb einer GeVo/Test Datei
kopfzeilen = 5

# Web Applikation URL
download_target_path = 'http://www.seleniumeasy.com/test/basic-first-form-demo.html'
#
test_browser = "ch"
# Browser Paths
ChromePath = 'Browser/Chrome/GoogleChromePortable.exe'
FirefoxPath = 'Browser/Chrome/FirefoxPortable.exe'
# Webdriver Paths
ChromeDriverPath = 'Browser/Chrome/chromedriver'
FirefoxDriverPath = 'Browser/Firefox/geckodriver'

# Ablageort für GeVo Dateien
gevo_ordner = "Tests/GeVos/"

# Name der Übersichtsdatei
name_overview_file = "Testlauf-Übersicht.md.html"
# Steuert ob pro Tag mehre Übersichtdateien möglich sind
# True = Übersichtsdatei wird mit jeder Ausführung Überschrieben
# False = Mit jeder Ausführung wird eine Datei, auf Basis der Variablen "name_overview_file" mit einem Index (erster freier Index) erstellt
#         Bsp. Testlauf-Übersicht_1.md.html
overview_single_file = True

# zusätzliche Testfallspezifische Testdaten, welche zur Laufzeit des Tests durch vom Nutzer verwendete Aktionen
# erzeugt/geändert/verwendet werden
testfall_variablen = {}
waitcount = 20

# Im Testablauf können Testdaten referenziert werden.
# mittels der folgenden Identifier werden die Referenzen ermittelt
testdaten_identifier_anfang = "[@@"
testdaten_identifier_ende = "@@]"
testdaten_identifier_ende_int = "@@:int]"
testdaten_identifier_ende_float = "@@:float]"

###### Übergebenes Skript ausführen #######
def testfaelle_ausfuehren(self, url, testliste, zielordner, browser, headless, loglevel):
    # global die browser variable setzen
    global test_browser
    test_browser = browser

    # Tabelle für die, nach Abschluss des Testlaufs, erzeugte Übersicht
    test_overview = []
    test_overview.append("Testfallame,Testfall-Ordner,Akzeptanzkriterium,TF-Gesamt,TF-Erfolgreich,TF-Fehlerhaft")
    # prüfen ob der übergebene Zielordner existiert und tatsächlich ein Verzeichnis ist
    if path.exists(zielordner) and path.isdir(zielordner):
        datum = datetime.datetime.now().strftime("%Y%m%d")
        zielordner = zielordner + datum + "\\"
        Classes.Logging.logfile_overview_anlegen(zielordner, name_overview_file, overview_single_file)
        for i in range(len(testliste)):
            pfad = testliste[i]
            # Dokumentenheader für Logdatei erzeugen
            # Prüfen, ob die Übergebene Skriptdatei existiert
            if path.exists(pfad):
                resultat = testskript_ausfuehren(self, url, pfad, zielordner, browser, headless, loglevel)
                # Liste aller Testergebnisse um das durchgeführte erweitern
                test_overview.append(resultat)
            else:
                print(pfad + " - Skript nicht gefunden")
        Classes.Logging.logfile_overview_abschließen(test_overview)
    else:
        # Classes.Logging.fehler_nachricht_anlegen("Fehler", "Zielordner wurde nicht gefunden - Testlauf wurde abgebrochen")
        pytest.fail("Fehler beim ausführen der Testfälle - Zielordner nicht gefunden\n->'" + zielordner + "'")


##### Testskript ausführen #####
def testskript_ausfuehren(self, url, pfad, zielordner, browser, headless, loglevel):
    # Variablen zur Erstellung der Test-Übersicht
    anzahl_testfälle = 0
    anzahl_erfolgreich = 0
    anzahl_fehlerhaft = 0
    testfall_akzeptanzkriterium = ""

    # Testfall Datei einlesen
    aktionsliste, pfad, tablemeta, tablesteps, tf_name, testfall_akzeptanzkriterium = datei_auslesen(pfad, "testfall")
    # Testdaten einlesen
    ## den Pfad für die Testdatendatei erzeugen
    testdatenpfad = (path.dirname(path.normpath(pfad)) + "\\Testdaten\\" + path.basename(path.normpath(pfad))).replace(".tc", ".csv")
    tablemeta.append("Testdaten-Datei,[Datei](file:/" + testdatenpfad + ")")
    ## Prüfen, ob der erzeugte Pfad auch existiert
    if not path.exists(testdatenpfad):
        #Classes.Logging.fliesstext_eintrag(testdatenpfad)
        #Classes.Logging.fehler_nachricht_anlegen("Testdaten Datei nicht gefunden", "Es wurde keine Testdatendatei
        #unter dem erwarteten Pfad ("+testdatenpfad+") gefunden")
        pytest.fail("Testdatendatei nicht gefunden")
        return
    ## aus dem erzeugten Pfad/Testdaten-Datei wird ein Data-Dictionary erzeugt
    testdaten_dict = dict_aus_datei_erzeugen(testdatenpfad)
    #pprint(testdaten_dict[0])
    # Testlauf für
    t = 0
    ## Uhrzeit der Testdurchführung wird gesichert (dient zur Ablage der Testablauf-Dokumentation)
    result = 0
    uhrzeit = datetime.datetime.now().strftime("%H_%M_%S")
    for t in range(len(testdaten_dict)):
        self.driver, log_ordner = test_vorbereiten(self, headless, browser, url, zielordner, loglevel, uhrzeit, tf_name, tablemeta, tablesteps, t+1)
        if self.driver is None:
            test_abschliessen(result)
            continue;
        for i in range(len(aktionsliste)):
            # Kopfzeile wird übersprungen
            # Eintrag innerhalb der CSV wird gesplitted und Variablen zugewiesen
            if aktionsliste[i] == "":
                continue
            splitted = aktionsliste[i].split(";")
            if len(splitted) < 5:
                nachricht = "Die Aktion in der **Zeile " + str(i + 1) + "** hat nicht genügend Parameter"
                print (nachricht)
                Classes.Logging.fehler_nachricht_anlegen("Fehler in Testdurchführungs-Datei (*.tc)",nachricht)
                return 0
            art = splitted[0].lower()
            aktion = splitted[1].lower()
            identifier = splitted[2].lower()
            element = splitted[3]
            parameter = splitted[4]
            optional = False
            if len(splitted) > 5:
                if splitted[5].lower() == "optional":
                        optional = True
            result = 1
            # sofern ein Parameter Identifikator für die Testdaten übergeben wurde, so wird dieser ersetzt
            # Bsp. Bei Buttons wird kein weiterer Parameter erwartet, somit wäre "parameter" in diesem fall ""
            if art == "steuerung":
                result = aktion_ausfuehren(self.driver, aktion, identifier, element, parameter, testdaten_dict, t, optional)
            elif art == "gevo":
                result = gevo_ausfuehren(self.driver, aktion, testdaten_dict, t)
            else:
                result = 0
                break
            if result == 0:
                break
        if result == 0:
            anzahl_fehlerhaft = anzahl_fehlerhaft + 1
        else:
            anzahl_erfolgreich = anzahl_erfolgreich + 1
        test_abschliessen(result)
        # die Testfall Variablen werden nach jedem Testlauf zurückgesetzt
        # Stellt sicher, dass für jeden Testlauf die Variablen vor ihrer Verwendung neu angelegt werden
        global testfall_variablen
        testfall_variablen = {}
        t = t + 1
    anzahl_testfälle = len(testdaten_dict)
    ### Um eine Testablaufsübersicht zu erstellen wird pro Testfall eine Übersicht über
    ### die durchgeführten Testläufe dokumentiert
    return tf_name + "," + log_ordner + "," + testfall_akzeptanzkriterium + "," + str(anzahl_testfälle) + "," + \
           str(anzahl_erfolgreich) + "," + str(anzahl_fehlerhaft)

###### GeVo ausführen
def gevo_ausfuehren(driver, aktion, testdaten_dict, tesfall_von_testdaten_dict):
    #### 0. GeVo Informationen in Log-Schreiben.
    pfad = gevo_ordner + aktion + ".gevo"
    if not path.exists(pfad):
        print("Pfad nicht gefunden - " + pfad)
        Classes.Logging.fehler_nachricht_anlegen(
            "Fehler beim ausführen des GeVos","Der GeVo konnte nicht gefunden werden - **"
                                              + pfad + "**. Der Testlauf wurde abgebrochen")
        return 0
    gevo_aktionsliste, pfad, tablemeta, tablesteps, gevo_name, gevo_akzeptanzkriterium = datei_auslesen(pfad, "gevo")

    Classes.Logging.fliesstext_eintrag("Der GeVo-Ablauf mit folgenden Steps wurde geladen")
    Classes.Logging.dokumenten_header_anlegen(tablemeta, tablesteps, True)
    #### 1. GeVo-Datei öffnen
    #### 2. Schleife über GeVo-Aktionen
    #### 3. Pro Aktion "aktion_ausführen" aufrufen
    k = 0
    for k in range(len(gevo_aktionsliste)):
        gevo_splitted = gevo_aktionsliste[k].split(";")
        if len(gevo_splitted) < 5:
            nachricht = "Die Aktion in der **Zeile " + str(k + 1) + "** hat nicht genügend Parameter"
            print (nachricht)
            Classes.Logging.fehler_nachricht_anlegen("Fehler in GeVo-Datei (*.gevo)",nachricht)
            return 0

        gevo_aktion = gevo_splitted[1].lower()
        gevo_identifier = gevo_splitted[2].lower()
        gevo_element = gevo_splitted[3]
        gevo_parameter = gevo_splitted[4]
        optional = False
        if len(gevo_splitted) > 5:
            if gevo_splitted[5].lower() == "optional":
                    optional = True
        result = aktion_ausfuehren(driver, gevo_aktion, gevo_identifier, gevo_element, gevo_parameter,
                                   testdaten_dict, tesfall_von_testdaten_dict, optional)
        k = k + 1
        if result == 0:
            return 0
    return 1

# Liest die übergebene Datei gemäß der folgenden Vorgabe aus
# Zeile 1 = Name
# Zeile 2 = Beschreibung
# Zeile 3 = Akzeptanzkriterien (die ";"-separierten Akzeptanzkriterien werden mit der Jira Basis URL verkettet)
# Zeile 4 = <bisher nicht verwendet>
# Zeile 5 = <bisher nicht verwendet>
# Zeile 6ff. = Testablauf (wird in in Liste geschrieben)
def datei_auslesen(pfad, art):
    akzeptanzkriterium = ""
    name_aus_datei = ""
    tablemeta = []
    tablemeta.append("Feld,Wert")
    tablesteps = []
    aktionsliste = []
    tablesteps.append("Step #,typ,Aktion,Parameter")
    print(pfad)
    cnt = 1
    try:
        with open(pfad, 'r', encoding="UTF-8") as fp:
            line = fp.readline()
            cnt = 1
            while line:
                if cnt == 1:
                    name_aus_datei = line.strip()
                    text = "Testfall-Name"
                    if art.lower() == "gevo":
                        text = "GeVo-Name"
                    tablemeta.append(text + "," + line.strip())
                elif cnt == 2:
                    text = "Testfall-Beschreibung"
                    if art.lower() == "gevo":
                        text = "GeVo-Beschreibung"
                    tablemeta.append(text + "," + line.strip())
                elif cnt == 3:
                    if not line.strip() == "":
                        if ";" in line.strip():
                            splitted_akz = line.strip().split(";")
                            for i in range(len(splitted_akz)):
                                akzeptanzkriterium = akzeptanzkriterium + jira_base_url + \
                                                              splitted_akz[i] + "<br>"
                        else:
                            akzeptanzkriterium = jira_base_url + line.strip()
                        tablemeta.append(
                            "Akzeptanzkriterium(**Jira-#**)," + akzeptanzkriterium)
                    else:
                        tablemeta.append(
                            "Akzeptanzkriterium(**Jira-#**)," + "nicht hinterlegt")
                elif cnt > kopfzeilen:
                    if str(line.strip()) != "" and "---!>" not in str(line.strip()):
                        aktionsliste.append(str(line.strip()))
                        aktion = line.strip().split(";")
                        tablesteps.append(str(cnt - kopfzeilen) + "," + aktion[0] + "," + aktion[1] + "," + aktion[4])
                line = fp.readline()
                cnt += 1
    except Exception as e:
        nachricht = ""
        if art.lower() == "gevo":
            nachricht = "Fehler beim öffnen/auslesen der .gevo Datei " + pfad
            Classes.Logging.fehler_nachricht_anlegen("Fehler in GeVo-Datei (*.gevo)",nachricht)
        else:
            nachricht = "Fehler beim öffnen/auslesen der .tc Datei " + pfad
            Classes.Logging.fehler_nachricht_anlegen("Fehler in Testablauf-Datei (*.tc)",nachricht)
        zusatz = "**Datei**:" + pfad + "<br>**Zeile**: " + str(cnt) + "<br>**Meldung**:"
        Classes.Logging.exception_log("GUI-Automation -> Datei auslesen", zusatz + str(e))
        pytest.fail(nachricht)
    return aktionsliste, pfad, tablemeta, tablesteps, name_aus_datei, akzeptanzkriterium


###### aktion ausführen
def aktion_ausfuehren(driver, aktion, identifier, element, parameter, testdaten_dict, t, optional):
    type = ""
    par_alt = ""
    result = 0

    element, par_alt, parameter, erfolgreich = platzhalter_ersetzen(testdaten_dict, aktion, element, parameter, t)
    ### Prüfen ob die Platzhalter korrekt ersetzt wurden.
    if erfolgreich == False:
        return 0
    #############################
    ## Abbilden der Aktionen
    ## weitere Aktionen können mit weiteren elif-Blöcken und dazugehörigen Funktionen, analog zu
    #  den bereits bestehenden, ergänzt werden.
    if aktion == "element_klicken":
        #### Element Klicken
        Classes.Logging.ueberschrift_anlegen(2, 'Element Klicken')
        result = element_klicken(driver, identifier, element)
    elif aktion == "element_prüfen":
        #### Element pruefen
        Classes.Logging.ueberschrift_anlegen(2, 'Element prüfen')
        Classes.Logging.testdaten_ersetzung(par_alt, parameter, type)
        result = element_pruefen(driver, identifier, element, parameter)
    elif aktion == "element_enthält_wert_prüfen":
        Classes.Logging.ueberschrift_anlegen(2, 'Element auf enthaltenen Wert prüfen')
        result = element_enthaelt_wert_pruefen(driver, identifier, element, parameter)
    elif aktion == "element_enthält_wert_nicht":
        Classes.Logging.ueberschrift_anlegen(2, 'Wert in Element nicht vorhanden prüfen')
        result = element_enthaelt_wert_nicht(driver, identifier, element, parameter)
    elif aktion == "element_setzen":
        #### Eingabewert
        Classes.Logging.ueberschrift_anlegen(2, 'Element setzen')
        Classes.Logging.testdaten_ersetzung(par_alt, parameter, type)
        result = element_setzen(driver, identifier, element, parameter)
    elif aktion == "element_ueber_label_setzen":
        #### Eingabewert
        Classes.Logging.ueberschrift_anlegen(2, 'Element über Label setzen')
        Classes.Logging.testdaten_ersetzung(par_alt, parameter, type)
        result = element_ueber_label_setzen(driver, identifier, element, parameter)
    elif aktion == "variable_setzen":
        Classes.Logging.ueberschrift_anlegen(2, 'Variable setzen')
        result = variablen_setzen(driver, identifier, element, parameter)
    elif aktion == "wechseln_zu":
        Classes.Logging.ueberschrift_anlegen(2, 'Wechseln zu')
        result = wechseln_zu(driver, identifier, element, parameter)
    elif aktion == "schalter_setzen":
        Classes.Logging.ueberschrift_anlegen(2, 'Schalter setzen')
        result = schalter_setzen(driver, identifier, element, parameter)
    elif aktion == "schalter_prüfen":
        Classes.Logging.ueberschrift_anlegen(2, 'Schalter prüfen')
        result = schalter_prüfen(driver, identifier, element, parameter)
    elif aktion == "element_ein_ausklappen":
        Classes.Logging.ueberschrift_anlegen(2, 'Element ein-/ausgeklappt prüfen')
        result = element_ein_ausklappen(driver, identifier, element, parameter)
    elif aktion == "warten_auf_element":
        Classes.Logging.ueberschrift_anlegen(2, 'Warten auf Element')
        result = warten_auf_element(driver, identifier, element, parameter)
    elif aktion == "warte":
        Classes.Logging.ueberschrift_anlegen(2, 'Warte in Sekunden')
        result = warte(driver, identifier, parameter)
    elif aktion == "wartezeit_timeout_setzen":
        Classes.Logging.ueberschrift_anlegen(2, 'Wartezeit Timeout setzen')
        result = wartezeit_timeout_setzen(parameter)
    else:
        Classes.Logging.warnung_anlegen(
            "Die angegebene Aktion **" + aktion + "** ist nicht vorhanden. der Testschritt wurde übersprungen")
    ### Wenn das ein optionaler Schritt war wird das Ergebnis im Fehlerfall auf positiv gesetzt
    ### Fehlermeldungen im Log bleiben erhalten
    if optional == True and result == 0:
        Classes.Logging.warnung_anlegen("Aufgrund des Zusatzes **'Optional'** an der Aktion wurde "
                                        "der Fehler ignoriert. Der Testlauf wird fortgesetzt")
        result = 1
    return result
#####
def platzhalter_ersetzen(testdaten_dict, aktion, element, parameter, t):
    ### Platzhalter für Variablen und Testdaten ersetzen
    par_alt = ""
    if parameter != "" and testdaten_identifier_anfang in parameter and (
            testdaten_identifier_ende in parameter or testdaten_identifier_ende_int in parameter or testdaten_identifier_ende_float in parameter):
        par_alt = parameter
        type = ""
        if testdaten_identifier_ende_int in parameter:
            type = "intzahl"
        if testdaten_identifier_ende_float in parameter:
            type = "floatzahl"
        # Platzhalter werden aus dem Parameter entfernt
        temp_par = parameter.replace(testdaten_identifier_anfang, "").replace(testdaten_identifier_ende, "").replace(
            testdaten_identifier_ende_int, "").replace(testdaten_identifier_ende_float, "")
        try:
            # Sollte hinter jedem Eintrag zu "temp_par" innerhalb des Testdaten_Dics eine Liste stecken
            # so wird der Wert in einen String umgewandelt und die entsprechenden Platzhalter für eine Liste
            # entfernt.
            parameter = str(testdaten_dict[t][temp_par]).replace("['", "").replace("']", "")
            if type == "intzahl":
                parameter = int(parameter)
            if type == "floatzahl":
                parameter = float(parameter)
        except Exception as e:
            Classes.Logging.ueberschrift_anlegen(2, 'Testdatum')
            table = []
            table.append("Beschreibung,Wert")
            table.append("Aktion," + aktion)
            table.append("Parameter," + parameter)
            Classes.Logging.fliesstext_eintrag("Beim Auflösen der Referenz (auf Testdatum oder Testvariable) ist ein "
                                               "Fehler aufgetreten. Die folgende Aktion wurde nicht durchgeführt.")
            Classes.Logging.tabelle_anlegen(table)
            Classes.Logging.fehler_nachricht_anlegen(
                "Fehler beim lesen des Testdatum", "Das Testdatum **" + temp_par + "** konnte nicht gelesen werden, "
                "da sie wohlmöglich nicht in der Testdaten-Datei hinterlegt ist. Der Testlauf wurde abgebrochen")
            Classes.Logging.exception_log("GUI-Automation -> Platzhalter ersetzen", str(e))
            return  "", "", "", False
        if testdaten_identifier_anfang in element and (
            testdaten_identifier_ende in element or testdaten_identifier_ende_int in element or testdaten_identifier_ende_float in element):
            element = element.replace(par_alt, parameter)
        type = "testdaten"
    #### Variable innerhalb der Parameter mit dem hinterlegten Wert erstetzen
    elif aktion != "variable_setzen" and parameter != "" and "[var:" in parameter and "]" in parameter:
        par_alt = parameter
        temp_par = parameter.replace("[var:", "").replace("]", "")
        if temp_par in testfall_variablen:
            try:
                parameter = testfall_variablen[temp_par]
            except Exception as e:
                Classes.Logging.exception_log("GUI-Automation -> Platzhalter ersetzen", str(e))
                Classes.Logging.fehler_nachricht_anlegen("Fehler beim ersetzen der Variablen",
                                                     "Die variable **" + temp_par + "** konnte nicht ersetzt werden. "
                                                                                    "Der Testlauf wurde abgebrochen")
                return "", "", "", False
        else:
            Classes.Logging.ueberschrift_anlegen(2, 'Testvariable')
            table = []
            table.append("Beschreibung,Wert")
            table.append("Aktion," + aktion)
            table.append("Parameter," + parameter)
            Classes.Logging.fliesstext_eintrag("Beim Auflösen der Referenz (auf Testdatum oder Testvariable) ist ein "
                                               "Fehler aufgetreten. Die folgende Aktion wurde nicht durchgeführt.")
            Classes.Logging.tabelle_anlegen(table)
            Classes.Logging.fehler_nachricht_anlegen("Fehler beim lesen der Variablen",
                                                     "Die variable **" + temp_par + "** konnte nicht gelesen werden. "
                                                                                    "Der Testlauf wurde abgebrochen")
            # return 0 zum abbrechen des Testlaufs
            return "", "", "", False
        if element != "" and "[var:" in element and "]" in element:
            element = element.replace(par_alt, parameter)
    ## Wenn zum Beispiel bei der Aktion "element_klicken" der Linktext als Wert übergeben wird, wird dieser
    ## in der Variablen "element" gespeichert.
    if element == "":
        element = parameter

    return element, par_alt, parameter, True

#######
def test_vorbereiten(self, headless, browser, url, zielordner, loglevel, uhrzeit, tf_name, tablemeta, tablesteps, testfallnr):
    log_ordner = zielordner + tf_name.replace(" ", "_") + "\\" + uhrzeit
    zielordner = log_ordner + "\\TF_" + str(testfallnr) + "\\"
    global download_target_path
    download_target_path = zielordner
    if not path.exists(zielordner):
        os.makedirs(zielordner)
    # Logfile anlegen
    Classes.Logging.logfile_anlegen(zielordner, "log.md.html", loglevel)
    # Logfile Header anlegen
    Classes.Logging.dokumenten_header_anlegen(tablemeta, tablesteps)
    # Webdriver erzeugen
    self.driver = webbrowser_anlegen(browser, headless)
    if self.driver is None:
        Classes.Logging.fehler_nachricht_anlegen("Fehler", "Webdriver nicht gefunden")
        #pytest.fail("Webdriver nicht korrekt initiiert")
        return None,""
    try:
        self.driver.fullscreen_window()
    except Exception as e:
        Classes.Logging.exception_log("GUI-Automation -> Test vorbereiten", "Fehler beim wechseln zum Vollbildmodus.<br>" + str(e))
        return None
    Classes.Logging.log_webdriver(self.driver, browser)
    result = 0
    result = URLOeffnen(self.driver, url)
    if result == 0:
        self.driver.close()
        self.driver.quit()
        Classes.Logging.fehler_nachricht_anlegen("Fehler beim öffnen der Seite",
                                                 "Beim öffnen der Seite ist ein Fehler aufgetreten")
        #pytest.fail("Fehler beim öffnen der Seite")
        return None,""
    warten_auf_element(self.driver,"tag_name", "iframe")
    wechseln_zu(self.driver, "tag_name", "iframe", "frame")
    return self.driver, log_ordner

###### Am Ende der Testdurchführung wird der Testlauf abgeschlossen.
###### Die Log Datei wird abgeschlossen und die offenen Tasks werden gekillt
def test_abschliessen(result = 0):
    ## Da diese Funktion standardmäßig am Ende der Testfalldurchführung aufgerufen wird,
    ## muss geprüft werden. ob der Testabschluss bereits vorgenommen wurde. Im Falle eines
    ## erfolgreichen Test wird die Funktion nach vollständiger Beendigung des Testlaufs
    ## nicht erneut durchgeführt (standardmäßig würde der Aufrauf mit result == 0 (negativ) am
    ## Ende des Testlaufs erneut erfolgen
    if not path.exists(Classes.Logging.LogFilePath):
        return
    if Classes.Logging.testabschluss_pruefen() == 1:
        return
    Classes.Logging.ueberschrift_anlegen(1, "Testfall Abschluss")
    if result == 0:
        Classes.Logging.fehler_nachricht_anlegen("Fehler", "Der Testlauf war nicht erfolgreich")
    elif result == 1:
        Classes.Logging.erfolg_nachricht_anlegen("Der Testlauf war erfolgreich")
    Classes.Logging.ueberschrift_anlegen(2, "Prozesse bereinigen")
    if test_browser.lower() == "firefox" or test_browser.lower() == "ff":
        kill_tasks("firefox")
    elif test_browser.lower() == "chrome" or test_browser.lower() == "ch":
        kill_tasks("chrome")
    Classes.Logging.ueberschrift_anlegen(2, "Durchführunsdauer")
    Classes.Logging.logfile_abschliessen()


###### Webseite per Uebergebene URL oeffnen
def webbrowser_anlegen(browser, headless):
    # WebDriver Object
    driver = None
    try:
        if browser.lower() == "firefox" or browser.lower() == "ff":
            kill_tasks("firefox")
            if not path.exists(FirefoxDriverPath) and not path.exists(FirefoxPath):
                Classes.Logging.fehler_nachricht_anlegen(
                    "Fehler beim Erzeugen des WebDrivers", "Der WebDriver für Firefox konnte nicht erzeugt werden. "
                    "Überprüfen Sie die Ablage des portablen Browsers und GeckDriver")
                return None
            options = webdriver.FirefoxOptions()
            if headless == "1":
                options.add_argument('--headless')
            options.add_argument("--start-maximized")
            options.binary_location = FirefoxPath
            driver = webdriver.Firefox(executable_path=FirefoxDriverPath, options=options)
            #driver = webdriver.Firefox(executable_path=GeckoDriverManager.install(), options=options)
        elif browser.lower() == "chrome" or browser.lower() == "ch":
            # Sicherstellen, dass keine Prozesse von vorherigen läufen mehr offen sind
            kill_tasks("chrome")
            if not path.exists(ChromeDriverPath) and not path.exists(ChromePath):
                Classes.Logging.fehler_nachricht_anlegen(
                    "Fehler beim Erzeugen des WebDrivers", "Der WebDriver für Chrome konnte nicht erzeugt werden. "
                    "Überprüfen Sie die Ablage des portablen Browsers und ChromeDriver")
                return None
            options = webdriver.ChromeOptions()
            # Tests ohne Menuleiste
            options.add_argument("--no-sandbox")  # Bypass OS security model
            # if headless == 1:
            if headless == "1":
                options.add_argument('--headless')
            # options.add_argument("--kiosk")
            # options.add_argument('--disable-extensions')
            options.add_argument("--disable-gpu")
            options.add_argument("--remote-debugging-port=9222")
            options.add_argument("--disable-dev-shm-usage")  # overcome limited resource problems
            # options.add_argument("--start-maximized")
            options.add_argument("--silent")
            options.add_argument("--disable-infobars")
            prefs = {"profile.default_content_settings.popups": 0,
                     "download.default_directory": download_target_path,
                     "directory_upgrade": True}
            options.add_experimental_option("prefs", prefs)
            options.binary_location = ChromePath

            driver = webdriver.Chrome(executable_path=ChromeDriverPath, options=options)
            #driver = webdriver.Chrome(executable_path=ChromeDriverManager.install(), options=options)
    except Exception as e:
        Classes.Logging.exception_log("GUI-Automation -> Webbrowser anlegen", "Fehler beim anlegen des Webdrivers <br>" + str(e))
        return None
    return driver


###### beendet alle Tasks für den übergebenen Browser
def kill_tasks(b):
    command_1 = ""
    command_2 = ""
    ausgabe_err_1 = ""
    ausgabe_1 = ""
    ausgabe_err_2 = ""
    ausgabe_2 = ""
    if b == "chrome":
        command_1 = 'TASKKILL /f /IM CHROMEDRIVER.EXE'
        proc = subprocess.Popen(command_1,
                                shell=True,
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                )
        proc.wait()
        ausgabe_1, ausgabe_err_1 = proc.communicate()
        command_2 = 'TASKKILL /f /IM CHROME.EXE'
        proc = subprocess.Popen(command_2,
                                shell=True,
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                )
        proc.wait()
        ausgabe_2, ausgabe_err_2 = proc.communicate()
    elif b == "firefox":
        command_1 = 'TASKKILL /f /IM GECKODRIVER.EXE'
        proc = subprocess.Popen(command_1,
                                shell=True,
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                )
        proc.wait()
        ausgabe_1, ausgabe_err_1 = proc.communicate()
        command_2 = 'TASKKILL /f /IM FIREFOX.EXE'
        proc = subprocess.Popen(command_2,
                                shell=True,
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                )
        proc.wait()
        ausgabe_2, ausgabe_err_2 = proc.communicate()

    ### Ausgabe der Resultate in die Log-Datei
    Classes.Logging.log_taskkill(command_1, ausgabe_1, ausgabe_err_1, command_2, ausgabe_2, ausgabe_err_2)


###### Webseite per Uebergebene URL oeffnen
def URLOeffnen(driver, pageUrl):
    Classes.Logging.ueberschrift_anlegen(2, "Webseite öffnen")
    driver.maximize_window()
    try:
        driver.get(pageUrl)
        Classes.Logging.fliesstext_eintrag("Die URL wurde mit dem Browser geöffnet")
    except Exception as e:
        Classes.Logging.fliesstext_eintrag("Fehler beim öffnen Webseite")
        Classes.Logging.exception_log("GUI-Automation -> URLOeffnen", str(e))
    result = benutzer_anmelden(driver)
    if result == 1:
        table = []
        table.append("Beschreibung,Wert")
        table.append("URL," + pageUrl)
        Classes.Logging.tabelle_anlegen(table)
        Classes.Logging.screenshot_anlegen(driver)
        return 1
    else:
        Classes.Logging.fehler_nachricht_anlegen("Fehler beim Erzeugen des WebDrivers",
                                                 "Bei der Anmeldung ist ein Fehler aufgetreten. Die "
                                                 "Anmeldung konnte nicht durchgeführt werden")
        return 0

###############
###### Webseite per Uebergebene URL oeffnen
def benutzer_anmelden(driver):
    ## Benutzername eintragen
    ## Logging
    Classes.Logging.ueberschrift_anlegen(2, 'Anmeldung')
    lowered_page_title = str(driver.title).lower()
    if lowered_page_title == "sign in to your account":
        #### Es wurde bereits eine Anmeldung mit einem Nutzer durchgeführt
        #### Die Benutzerdaten sind hinterlegt und müssen zur Anmeldung ausgewählt werden.
        lowered_pagesource = str(driver.page_source).lower()
        if lowered_pagesource.find("mnaas@soka-dach.de"):
            Classes.Logging.fliesstext_eintrag("Es wird eine Anmeldung durchgeführt")
            #Benutzername setzen
            element_setzen(driver, "name", "loginfmt", "mnaas@soka-dach.de")
            # nicht notwendig, da ein Enter bei elemente_setzen durchgeführt wird - Next Klicken
            #element_klicken(driver, "id","idSIButton9")
            # Passwort setzen
            element_setzen(driver, "name", "passwd", "start123#")
            # nicht notwendig, da ein Enter bei elemente_setzen durchgeführt wird -  SignIn Klicken
            #element_klicken(driver, "id","idSIButton9")
            # Stay signed in Klicken
            element_klicken(driver, "id","idSIButton9")
            Classes.Logging.fliesstext_eintrag(
                "Es wurde eine neue Benutzeranmeldung durchgeführt")
            return 1
        else:
            #### Benutzername muss eingetragen werden
            #### Passwort muss eingetragen werden.
            #### Anmelden klicken
            element_pruefen(driver, "xpath", "//div[contains(text(),'mnaas@soka-dach.de')]", "mnaas@soka-dach.de")
            element_klicken(driver, "xpath", "//div[contains(text(),'mnaas@soka-dach.de')]")
            #nicht notwendig, da ein Enter bei elemente_setzen durchgeführt wird -  SignIn Klicken
            #element_klicken(driver, "id","idSIButton9")
            # Stay signed in Klicken
            element_klicken(driver, "id","idSIButton9")
            Classes.Logging.fliesstext_eintrag(
                "Aufgrund von bereits hinterlegten Anmeldedaten erfolgt die Anmeldung über Auswahl des hinterlegten Nutzers")
            return 1
    elif lowered_page_title == "microsoft dynamics nav":
        #### Anmeldung war nicht notwendig, Startseite von Microsoft NAV wird bereits angezeigt
        Classes.Logging.notiz_anlegen(
            "Aufgrund einer bereits bestehenen Anmeldung musste keine erneute Anmeldung durchgeführt werden.")
        return 1
    else:
        ####
        Classes.Logging.fehler_nachricht_anlegen("Fehlerhafter Seitentitel",
            "Der Seitentitel der geöffneten Seite entsprach keinem der erwarteten Titel - " + driver.title)
        return 0


########################
# Verwaltet die zusätzlichen Variablen
# type = read  ->  Variable wird ausgelesen
# type = write   ->  Variable wird gesetzt/aktualisiert
def variablen_setzen(driver, identifier_type, identifier, parameter):
    element = get_element(driver, identifier_type, identifier)
    global testfall_variablen
    wert = element.text
    parameter = parameter.replace("[var:","").replace("]","")
    if parameter not in testfall_variablen:
        ## Logging
        eintrag = 'Die Variable (**%s**) mit dem Wert (**%s**) wurde hinzugefügt' % (parameter, wert)
        Classes.Logging.fliesstext_eintrag(eintrag)
    else:
        ## Logging
        eintrag = 'Die Variable (**%s**) mit dem Wert (**%s**) wurde auf den Wert (**%s**) geändert' % (parameter, testfall_variablen[parameter], wert)
        Classes.Logging.fliesstext_eintrag(eintrag)
    try:
        testfall_variablen[parameter] = wert
    except Exception as e:
        Classes.Logging.exception_log("GUI-Automation -> Variable Setzen", str(e))


###### Element setzen
def element_setzen(driver, identifier_type, identifier, wert):
    ## Wert eintragen
    ########################
    element = get_element(driver, identifier_type, identifier)
    ## Logging
    if element is None:
        eintrag = 'Fehler beim setzen von (** %s **) auf den Wert (** %s **)' % (identifier, wert)
        Classes.Logging.fehler_nachricht_anlegen("Fehler beim setzen des Elementes", eintrag)
        return 0
    # Wenn über den Testlauf ein RETURN gesendet wird, wird der Inhalt nicht geleert und an das
    # Element ausschließlich ein RETURN gesendet
    if wert == "[RETURN]":
        try:
            element.send_keys(Keys.RETURN)
            return 1
        except Exception as e:
            eintrag = 'Fehler beim senden der ENTER-Taste für das Element (** %s **)' % (identifier)
            Classes.Logging.fehler_nachricht_anlegen("Fehler beim setzen des Elementes", eintrag)
            Classes.Logging.exception_log("GUI-Automation -> Element setzen", str(e))
            return 0
    try:
        element.clear()
    except Exception as e:
        Classes.Logging.notiz_anlegen("Das Element " + identifier + " konnte nicht geleert werden")
        Classes.Logging.exception_log("GUI-Automation -> Element setzen", str(e))
    try:
        element.send_keys(wert)
    except Exception as e:
        eintrag = 'Fehler beim setzen von (** %s **) auf den Wert (** %s **)' % (identifier, wert)
        Classes.Logging.fehler_nachricht_anlegen("Fehler beim setzen des Elementes", eintrag)
        Classes.Logging.exception_log("GUI-Automation -> Element setzen", str(e))
        return 0
    try:
        element.send_keys(Keys.RETURN)
    except Exception as e:
        Classes.Logging.notiz_anlegen("RETURN konnte nicht an das Element + " + identifier + " gesendet werden")
        Classes.Logging.exception_log("GUI-Automation -> Element setzen", str(e))
    eintrag = 'Das Element (** %s **) wurde auf den Wert (** %s **) gesetzt' % (identifier, wert)
    Classes.Logging.fliesstext_eintrag(eintrag)

    styled_screenshot(driver, element)

    return 1

############### Funktioniert bisher noch nocht
############### Funktion muss noch gefixed werden
def element_ueber_label_setzen(driver, identifier_type, identifier, wert):
    label_element = get_element(driver, identifier_type, identifier)
    if label_element is None:
        eintrag = 'Fehler beim setzen von (**%s**) auf den Wert (**%s**)' % (identifier, wert)
        Classes.Logging.fehler_nachricht_anlegen("Fehler beim setzen des Elementes", eintrag)
        return 0

    label_id = str(label_element.get_attribute("for"))
    eintrag = 'Über das Label wurde die folgende Input-ID identifiziert (**%s**)' % (label_id)
    Classes.Logging.fliesstext_eintrag(eintrag)

    styled_screenshot(driver, element)

    eingabe_element = get_element(driver, "id", label_id)

    if eingabe_element is None:
        eintrag = 'Fehler beim setzen von (**%s**) auf den Wert (**%s**)' % (identifier, wert)
        Classes.Logging.fehler_nachricht_anlegen("Fehler beim setzen des Elementes", eintrag)
        return 0

    styled_screenshot(driver, element)

    eingabe_element.clear()
    eingabe_element.send_keys(wert)
    return 1


###### Element klicken
def element_klicken(driver, identifier_type, identifier):
    # Finding "Show Your Message" button element by css selector using both id and class name. And clicking it.
    element = get_element(driver, identifier_type, identifier, True)
    if element is None:
        eintrag = 'Fehler beim Klicken auf das Element (**%s**). Das Element wurde nicht gefunden.' % (identifier)
        Classes.Logging.fehler_nachricht_anlegen("Fehler beim klicken auf das Elementes", eintrag)
        return 0
    eintrag = 'Es wurde auf das Element (**%s**) geklickt' % (identifier)
    Classes.Logging.fliesstext_eintrag(eintrag)

    styled_screenshot(driver, element)
    try:
        element.click()
        ## Logging
    except Exception as e:
        eintrag = 'Element (**%s**) - konnte nicht geklickt werden' % (identifier)
        Classes.Logging.fehler_nachricht_anlegen("Fehler beim klicken des Elementes", eintrag)
        Classes.Logging.exception_log("GUI-Automation -> Element klicken", str(e))
        #pytest.fail(str(element) + " - Element konnte nicht geklickt werden")
        return 0
    return 1

###############


###### Element pruefen
def element_pruefen(driver, identifier_type, identifier, wert):
    # Checking whether the input text and output text are same using assertion.
    element = get_element(driver, identifier_type, identifier)
    ## Logging
    eintrag = ""
    if identifier == "":
        eintrag = 'Es wird geprüft, dass das Element (**%s**) exakt dem folgenden Wert entspricht (**%s**)' % (wert, wert)
    else:
        eintrag = 'Es wird geprüft, dass das Element (**%s**) exakt dem folgenden Wert entspricht (**%s**)' % (identifier, wert)

    Classes.Logging.fliesstext_eintrag(eintrag)
    Classes.Logging.notiz_anlegen("Der Vergleich ist Case-Sensitiv")
    if element is None:
        Classes.Logging.fehler_nachricht_anlegen("Fehler beim prüfen des Elementes", eintrag)
        #pytest.fail(element + " = None")
        return 0
    try:
        WebDriverWait(driver, waitcount).until(EC.textToBePresentInElementLocated(element, wert))
    except Exception as e:
        eintrag = 'Das Element (**%s**) hat innerhalb von **%s** Sekunden nicht den erwarteten Wert (**%s**) angenommen' % (identifier, str(waitcount), wert)
        Classes.Logging.fehler_nachricht_anlegen("Fehler beim prüfen des Elementes", eintrag)
        Classes.Logging.exception_log("GUI-Automation -> Element prüfen", str(e))
        return 0
    styled_screenshot(driver, element)

    if wert == element.text:
        eintrag = 'Der Wert (**%s**) entspricht dem erwarteten Wert (**%s**)' % (element.text, wert)
        Classes.Logging.erfolg_nachricht_anlegen(eintrag)
        return 1
    else:
        eintrag = 'Der Wert (**%s**) entspricht **nicht** dem erwarteten Wert (**%s**)' % (element.text, wert)
        Classes.Logging.fehler_nachricht_anlegen("Fehler beim prüfen des Elementes", eintrag)
        return 0

###### Element enthält prüfen
def element_enthaelt_wert_pruefen(driver, identifier_type, identifier, wert):
    # Checking whether the input text and output text are same using assertion.
    element = get_element(driver, identifier_type, identifier)
    ## Logging
    eintrag = ""
    if identifier == "":
        eintrag = 'Es wird gepürft, dass das Element (**%s**) den folgenden Wert enthält (**%s**)' % (wert, wert)
    else:
        eintrag = 'Es wird gepürft, dass das Element (**%s**) den folgenden Wert enthält (**%s**)' % (identifier, wert)

    Classes.Logging.fliesstext_eintrag(eintrag)
    Classes.Logging.notiz_anlegen("Der Vergleich ist Case-Sensitiv")
    if element is None:
        Classes.Logging.fehler_nachricht_anlegen("Fehler beim prüfen des Elementes", eintrag)
        #pytest.fail(element + " = None")
        return 0
    count = 0
    sleeptime = 1
    while True:
        try:
            if wert in element.text:
                higlight_wert = "<span style = \"text-decoration: underline;\" > _" + wert + "_ </span>"
                wert_markiert = element.text.replace(wert, higlight_wert)
                eintrag = 'Der Wert (**%s**) ist in dem geprüften Wert (**%s**) enthalten. Es wurden (**%s**) Sekunden gewartet' % (wert, wert_markiert, (count)*sleeptime)
                Classes.Logging.erfolg_nachricht_anlegen(eintrag)
                return 1
        except Exception as e:
            element = get_element(driver, identifier_type, identifier)
            print("Fehler beim ermittelt des Inhalts für das Element " + str(element))
            Classes.Logging.exception_log("GUI-Automation -> Element enthält Wert prüfem", str(e))
        time.sleep(sleeptime)
        count = count + 1
        if count >= waitcount:
            break
    if wert not in element.text:
        eintrag = 'Der Wert (**%s**) ist in dem geprüften Wert (**%s**) **nicht** enthalten' % (wert , element.text)
        Classes.Logging.fehler_nachricht_anlegen("Fehler beim prüfen des Elementes", eintrag)
        return 0

###### Element enthält prüfen
def element_enthaelt_wert_nicht(driver, identifier_type, identifier, wert):
    # Checking whether the input text and output text are same using assertion.
    element = get_element(driver, identifier_type, identifier)
    ## Logging
    eintrag = ""
    if identifier == "":
        eintrag = 'Es wird gepürft, dass das Element (**%s**) den folgenden Wert enthält (**%s**)' % (wert, wert)
    else:
        eintrag = 'Es wird gepürft, dass das Element (**%s**) den folgenden Wert enthält (**%s**)' % (identifier, wert)

    Classes.Logging.fliesstext_eintrag(eintrag)
    Classes.Logging.notiz_anlegen("Der Vergleich ist Case-Sensitiv")
    if element is None:
        Classes.Logging.fehler_nachricht_anlegen("Fehler beim prüfen des Elementes", eintrag)
        #pytest.fail(element + " = None")
        return 0
    count = 0
    sleeptime = 1
    while True:
        try:
            if wert not in element.text:
                higlight_wert = "<span style = \"text-decoration: underline;\" > _" + wert + "_ </span>"
                wert_markiert = element.text.replace(wert, higlight_wert)
                eintrag = 'Der Wert (**%s**) ist in dem geprüften Wert (**%s**) **nicht** mehr enthalten. Es wurden (**%s**) Sekunden gewartet' % (wert, wert_markiert, (count)*sleeptime)
                styled_screenshot(driver, element)
                Classes.Logging.erfolg_nachricht_anlegen(eintrag)
                return 1
        except Exception as e:
            element = get_element(driver, identifier_type, identifier)
            print("Fehler beim ermittelt des Inhalts für das Element " + str(element))
            zusatz = "<br>**Das Element wurde erneut gesetzt und der Testlauf wird fortgesetzt.**"
            Classes.Logging.exception_log("GUI-Automation -> Element enthält Wert nicht", str(e) + zusatz)
        time.sleep(sleeptime)
        count = count + 1
        if count >= waitcount:
            break
    if wert in element.text:
        eintrag = 'Der Wert (**%s**) ist in dem geprüften Wert (**%s**) **weiterhin** enthalten' % (wert , element.text)
        Classes.Logging.fehler_nachricht_anlegen("Fehler beim prüfen des Elementes", eintrag)
        styled_screenshot(driver, element)
        return 0
###############
def wechseln_zu(driver, identifier_type, identifier, type = "frame"):
    if type == "frame":
        try:
            driver.switch_to.frame(get_element(driver, identifier_type, identifier))
            #wait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it(get_element(driver, identifier_type, identifier)))
        except Exception as e:
            Classes.Logging.notiz_anlegen("Es konnte nicht zu dem Frame gewechselt werden")
            Classes.Logging.exception_log("GUI-Automation -> Wechseln zu", str(e))
    if type == "form":
        try:
            get_element(driver, identifier_type, identifier)
        except Exception as e:
            Classes.Logging.notiz_anlegen("Es konnte nicht zu der Form gewechselt werden")
            Classes.Logging.exception_log("GUI-Automation -> Wechseln zu", str(e))
    eintrag = 'Es wurde zu folgendem Element (**%s**) gewechselt' % (identifier)
    Classes.Logging.fliesstext_eintrag(eintrag)


###############
def schalter_setzen(driver, identifier_type, identifier, wert):
    element = get_element(driver, identifier_type, identifier)
    if wert is None:
        wert = ""
    if element is None:
        eintrag = 'Fehler beim setzen des Schalter (**%s**) - auf den Wert' % (identifier, wert)
        Classes.Logging.fehler_nachricht_anlegen("Fehler setzen des Schalters", eintrag)
        #pytest.fail(element + " = None")
        return 0
    schalter_wert = str(element.get_attribute("title")).lower()
    styled_screenshot(driver, element)

    if schalter_wert == str(wert).lower():
        eintrag = 'Das Element (**%s**) entspricht dem erwarteten Wert (%s)' % (identifier, wert)
        Classes.Logging.erfolg_nachricht_anlegen(eintrag)
    else:
        eintrag = 'Das Element (**%s**) entspricht nicht dem erwarteten Wert (%s) und wird nun geklickt' % (identifier, wert)
        Classes.Logging.fliesstext_eintrag(eintrag)
        element_klicken(driver, identifier_type, identifier)
        schalter_setzen(driver, identifier_type, identifier, wert)
        #driver.execute_script("arguments[0].title = '" + str(wert) + "'", element)
    return 1


##### Zum prüfen von Checkboxen mittels Titel des Input-Tags
def schalter_prüfen(driver, identifier_type, identifier, wert):
    element = get_element(driver, identifier_type, identifier)
    if element is None:
        eintrag = 'Fehler beim setzen des Schalter (**%s**) - auf den Wert - Das Element wurde nicht gefunden' % (identifier, wert)
        Classes.Logging.fehler_nachricht_anlegen("Fehler setzen des Schalters", eintrag)
        #pytest.fail(element + " = None")
        return 0

    styled_screenshot(driver, element)

    if str(element.get_attribute("title")).lower() == str(wert).lower():
        eintrag = 'Das Element (**%s**) entspricht dem erwarteten Wert (%s)' % (identifier, wert)
        Classes.Logging.erfolg_nachricht_anlegen(eintrag)
        return 1
    else:
        eintrag = 'Das Element (**%s**) entspricht nicht dem erwarteten Wert (%s) - aktueller Wert ist (%s)' % (identifier, wert, element.get_attribute("title"))
        Classes.Logging.fehler_nachricht_anlegen("Schalter entspricht nicht erwartetem Wert", eintrag)
        return 0
    return 1
###############

def element_ein_ausklappen(driver, identifier_type, identifier, ausklappen = "ausklappen"):
    element = get_element(driver, identifier_type, identifier)
    if element is None:
        eintrag = 'Fehler beim ein/ausklappen des Elements (**%s**) - Das Element wurde nicht gefunden' % (identifier)
        Classes.Logging.fehler_nachricht_anlegen("Fehler setzen des Schalters", eintrag)
        #pytest.fail(element + " = None")
        return 0

    styled_screenshot(driver, element)
    class_value = str(element.get_attribute('class'))
    if ("expanded" in class_value and str(ausklappen).lower() == "einklappen") or ("collapsed" in class_value and str(ausklappen).lower() == "ausklappen"):
        new_identifier = identifier + "/div[1]/span[@class=\"ms-nav-columns-caption icon-RightCaret-after\"]"
        eintrag = 'Das Element (**%s**) wird durch einen Klick ein-/ausgeklappt' % (new_identifier)
        Classes.Logging.fliesstext_eintrag(eintrag)
        element_klicken(driver, identifier_type, new_identifier)
        # erneuter Aufruf zum prüfen, ob das Element korrekt gesetzt wurde
        element_ein_ausklappen(driver, identifier_type, identifier, ausklappen)
    else:
        eintrag = 'Das Element (**%s**) mit der Klasse (**%s**) und dem Inhalt (**%s**) ' \
                  'entspricht dem erwarteten Wert ausklappen = (**%s**)' \
                  % (identifier, class_value, element.text, str(ausklappen))
        Classes.Logging.fliesstext_eintrag(eintrag)

    return 1

###############
def warten_auf_element(driver, identifier_type, identifier, type = "appear"):
    count = int(waitcount/5)
    if str(type).lower() == "appear":
        while True:
            element = get_element(driver, identifier_type, identifier, show_error=False)
            time.sleep(1)
            count = count - 1
            if element is not None or count <= 0:
                break
        if element is None:
            Classes.Logging.fehler_nachricht_anlegen(
                "Fehler beim Warten", "Fehler beim Warten auf das anzeigen des Elements - **" +
                identifier + "**. Es wurde nach **" + str(int(waitcount/5)) + "** Versuchen abgebrochen")
            return 0
        else:
            Classes.Logging.erfolg_nachricht_anlegen("Das Element - **" + identifier + "** ist vorhanden.")
            return 1
    elif str(type).lower() == "gone":
        while True:
            element = get_element(driver, identifier_type, identifier, show_error=False)
            time.sleep(1)
            count = count - 1
            if element is None or count <= 0:
                break
        if element is None:
            Classes.Logging.erfolg_nachricht_anlegen("Das Element - **" + identifier + "** ist nicht mehr vorhanden.")
            return 1
        else:
            Classes.Logging.fehler_nachricht_anlegen(
                "Fehler beim Warten", "Fehler beim Warten auf das verschwinden des Elements - **" +
                identifier + "**. Es wurde nach **" + str(int(waitcount/5)) + "** Versuchen abgebrochen")
            return 0
    return 0

###############
def warte(driver, identifier_type, wert):
    wartezeit = 0
    if str(identifier_type).lower() == "sekunden":
        wartezeit = int(wert)
        time.sleep(wartezeit)
    elif str(identifier_type).lower() == "minuten":
        wartezeit = int(wert) * 60
        time.sleep(wartezeit)
    Classes.Logging.notiz_anlegen("Es wurde, gemäß Testfallablauf, **" + str(wartezeit) + " Sekunde(n)** gewartet")
    return 1

def wartezeit_timeout_setzen(wert):
    global waitcount
    if str(wert).lower() == "default":
        waitcount = 20;
    else:
        waitcount = int(wert)
    Classes.Logging.notiz_anlegen("Die Wartezeit bis zu einem Timeout wurde auf *" + str(waitcount) + "* sekunden gesetzt")
###############

def get_element(driver, identifier_type, identifier, is_button = True, show_error = True):
    element = None
    identifier = str(identifier)

    identifier_type_lower = identifier_type.lower()
    by_type = By.ID
    if identifier_type_lower == "id":
        by_type = By.ID
    elif identifier_type_lower == "xpath":
        by_type = By.XPATH
    elif identifier_type_lower == "link_text":
        by_type = By.LINK_TEXT
    elif identifier_type_lower == "partial_link_text":
        by_type = By.PARTIAL_LINK_TEXT
    elif identifier_type_lower == "name":
        by_type = By.NAME
    elif identifier_type_lower == "tag_name":
        by_type = By.TAG_NAME
    elif identifier_type_lower == "class_name":
        by_type = By.CLASS_NAME
    elif identifier_type_lower == "css_selector":
        by_type = By.CSS_SELECTOR
    else:
        Classes.Logging.fehler_nachricht_anlegen("Fehler beim identifizieren",
                                                 "Es wurde ein nicht untertützter Identifier-Typ übergeben - **" + identifier_type + "**")
        return None
    if is_button == False:
        element = WebDriverWait(driver, waitcount).until(EC.presence_of_element_located((by_type, identifier)))
    else:
        try:
            element = WebDriverWait(driver, waitcount).until(EC.element_to_be_clickable((by_type, identifier)))
            WebDriverWait(driver, waitcount).until(EC.visibility_of(element))
            #element = WebDriverWait(driver, waitcount).until(EC.element_to_be_clickable(element))
        except Exception as e:
            Classes.Logging.exception_log("GUI-Automation -> Get Element", str(e))
            if len(driver.find_elements(by_type, identifier)) > 1:
                Classes.Logging.fehler_nachricht_anlegen(
                    "Fehler beim identifizieren", "Fehler beim identifizieren des Elements - **" +
                    identifier + "**. Es kein eindeutiges Element gefunden")
                element = None
            elif len(driver.find_elements(by_type, identifier)) == 0:
                Classes.Logging.fehler_nachricht_anlegen(
                    "Fehler beim identifizieren", "Fehler beim identifizieren des Elements - **" +
                    identifier + "**. Es konnte kein Element identifiziert werden.")
                element = None
            return element
    if element is None:
        if show_error == True:
            Classes.Logging.fehler_nachricht_anlegen(
                "Fehler beim identifizieren", "Fehler beim identifizieren des Elements - **" +
                identifier + "**. Es wurde nach **" + str(waitcount) + "** Sekunden ein Timeout erzeugt")
        return None
    actions = ActionChains(driver)
    try:
        actions.move_to_element(element).perform()
    except Exception as e:
        Classes.Logging.exception_log("GUI-Automation -> Get Element", str(e))
        if show_error == True:
            Classes.Logging.fehler_nachricht_anlegen("Fehler bei dem Wechsel zum Element",
                                                     "Es konnte nicht mittels switch zum Element gewechselt werden")
    eintrag = ""
    if identifier != "":
        eintrag = 'Das folgende Element (**%s**) wurde mittels (**%s**) selektiert' % (identifier, identifier_type)
    else:
        eintrag = 'Das folgende Element (**%s**) wurde mittels (**%s**) selektiert' % (identifier, identifier_type)
    Classes.Logging.fliesstext_eintrag(eintrag)
    Classes.Logging.screenshot_von_element_anlegen(element)
    return element

#### Die Testdatendatei wird in ein Dictionary geselen
#### Das Dictionary besteht aus einem Eintrag in dem alle alle Keys mit deren testfallspezifischen Werte hinterlegt sind
#### Der Wert eines Testfalls kann wie folgt ermittelt werden
####     - dict_list[0][<Key-Name>][<Testfall-Nr>]
def dict_aus_datei_erzeugen(testdatenpfad):
    delimiter = ';'
    dict_list = []
    # Wenn der Testdatenpfad nicht gefunden wird, wird ein Element im Dict angelegt.
    # Grund können Testfälle ohne Testdaten-Datei (nur fixe Aktionswerte) sein.
    if not path.exists(testdatenpfad):
        dict_list.append("keine Testdaten")
    try:
        input_file = csv.DictReader(open(testdatenpfad, 'r'), delimiter=delimiter)
    except Exception as e:
        Classes.Logging.exception_log("GUI-Automation -> Dict aus Datei erzeugen", str(e))
        Classes.Logging.fehler_nachricht_anlegen("Fehler","Fehler bei lesen der Testdaten-Datei")
        return []
    csv_dict = {elem: [] for elem in input_file.fieldnames}
    for row in input_file:
        for key in csv_dict.keys():
            csv_dict[key].append(row[key])
        dict_list.append(csv_dict.copy())
        csv_dict.clear()
        csv_dict = {elem: [] for elem in input_file.fieldnames}
    return dict_list

#### Erzeugt einen Screenshot mit hervorgehobenem Element
#### zu diesem Zweck wird ein
####    1. Style an das Element angefügt
####    2. Screenshot über die Logging-Klasse angelegt
####    3. der ursprüngliche Style wieder an das Element angefügt
def styled_screenshot(driver, element):
    try:
        # aktuellen Style sichern um ihn wieder zurücksetzen zu können
        original_style = element.get_attribute('style')
        # Style zum hervorheben von Elementen übergeben/setzen
        style_setzen(driver, element, "background: yellow; border: 2px solid red;")
        # Screenshot erstellen
        Classes.Logging.screenshot_anlegen(driver)
        # Style zurücksetzen
        style_setzen(driver, element, original_style)
    except Exception as e:
        Classes.Logging.exception_log("GUI-Automation -> Styled Screenshot", str(e))
        Classes.Logging.notiz_anlegen("Der Style zum markieren innerhalb des Screenshots konnte nicht gesetzt werden")

def style_setzen(driver, element, style):
    try:
        # übergebenen Style setzen
        driver.execute_script("arguments[0].setAttribute('style', arguments[1]);",
                          element, style)
    except Exception as e:
        Classes.Logging.exception_log("GUI-Automation -> Style setzen", str(e))
        Classes.Logging.notiz_anlegen("Der übergebene Style für das element **" + str(element) + "** konnte nicht gesetzt werden")
        # Fehlverhalten hat keine Auswirkungen auf den Testablauf