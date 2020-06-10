import datetime
import pytest
# Einlesen von Excel-Mappen
import xlrd
import subprocess
import csv
import os
import time
# Zur Prüfung von Jira Vorgängen
import requests
# Custom Library zur Testablaufdokumentation
import Classes.Logging
import xml.etree.ElementTree as ET
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from os import path
from selenium.webdriver.common.action_chains import ActionChains
#from webdriver_manager.chrome import ChromeDriverManager
#from webdriver_manager.firefox import GeckoDriverManager


###
###
### Hinweis für Rückgabewerte von allen Funktion innerhalb dieser Klasse
### Allgemein gilt
###     - return 0 = Funktion war nicht erfolgreich
###     - return 1 = Funktio war erfolgreich
###

# Basisadresse zur Jira
# dient zum erzeugen der korrekten URL zum Akzaptanzkriterium
jira_base_url = ""

# Anzahl der Kopfzeilen innerhalb einer GeVo/Test Datei (wird über die Config.xml gesetzt)
# # Die funktion "read_config" liest die Werte ein
kopfzeilen = -1
# Browser Paths (wird über die Config.xml gesetzt)
# Die funktion "read_config" liest die Werte ein
ChromePath = ''
FirefoxPath = ''
# Webdriver Paths (wird über die Config.xml gesetzt)
# # Die funktion "read_config" liest die Werte ein
ChromeDriverPath = ''
FirefoxDriverPath = ''

# Ablageort für GeVo Dateien (wird über die Config.xml gesetzt)
# # Die funktion "read_config" liest die Werte ein
gevo_ordner = ""

# Ablageort für Testlisten Dateien (wird über die Config.xml gesetzt)
# # Die funktion "read_config" liest die Werte ein
testlisten_ordner = ""

# Um am Ende eines Testfalldurchlaufs anzugeben, welche der Testdaten aus der Testdatendatei nicht verwendet wurden
# werden alle Testdaten in die folgende Liste gespeichert. Bei Testfalldurchlaufabschluss wird die Differenz
# zwischen der Liste der verwendeten Testdaten und den zu Beginn angelegten Testdaten gebildet und ausgegeben
# erzeugt/geändert/verwendet werden
nicht_verwendete_testdaten = []

# zusätzliche Testfallspezifische Testdaten, welche zur Laufzeit des Tests durch vom Nutzer verwendete Aktionen
# erzeugt/geändert/verwendet werden
testfall_variablen = {}
# Legt die Maximale Wartezeit bis zum Timeout fest (wird über die Config.xml gesetzt)
# # Die funktion "read_config" liest die Werte ein
waitcount = -1

# Im Testablauf können Testdaten referenziert werden.
# mittels der folgenden Identifier werden die Referenzen zu Testdaten ermittelt (wird über die Config.xml gesetzt)
# # # Die funktion "read_config" liest die Werte ein
testdaten_identifier_anfang = ""
testdaten_identifier_ende = ""
testdaten_identifier_ende_int = "@@:int]"
testdaten_identifier_ende_float = "@@:float]"
# mittels der folgenden Identifier werden die Referenzen Testvariablen ermittelt (wird über die Config.xml gesetzt)
# # # Die funktion "read_config" liest die Werte ein
testvariablen_identifier_anfang = ""
testvariablen_identifier_ende = ""



# Browser mit dem test Test tatsächlich durchgeführt wird
test_browser = ""

# Web Applikation URL (wird aktuell nicht in Testabläufen verwendet)
download_target_path = 'http://www.seleniumeasy.com/test/basic-first-form-demo.html'

## Pfad zur Config.xml
config_file_pfad = "E:/Testautomatisierung/config.xml"

# Der Style, der für das erstellen von Screenshots an das Element gehängt wird, um diese hervorzuheben (wird über die Config.xml gesetzt)
# Die funktion "read_config" liest die Werte ein
highlight_style =""

# Name der Übersichtsdatei
name_overview_file = "Testlauf-Übersicht.md.html"

# Steuert ob pro Tag mehre Übersichtdateien möglich sind
# True = Übersichtsdatei wird mit jeder Ausführung Überschrieben
# False = Mit jeder Ausführung wird eine Datei, auf Basis der Variablen "name_overview_file" mit einem Index (erster freier Index) erstellt
#         Bsp. Testlauf-Übersicht_1.md.html
overview_single_file = True

testdaten_dict = {}

### Liest eine XML Datei im dem aktuellen Ausführungsverzeichnisses ein
### und speichert die Werte in den entsprechenden Variablen
### Dies dient zur Steuerung von Attributen ohne Anpassung des Codes
def read_config():
    try:
        # Die Config Datei wir mittels XML-Parser eingelesen
        tree = ET.parse(config_file_pfad.strip())
        ################################# Allgemein
        ## GeVo Pfad laden
        global gevo_ordner
        gevo_ordner = str(tree.find("Allgemein").find("GeVoPfad").text).strip()

        ## Testlisten Pfad laden
        global testlisten_ordner
        testlisten_ordner = str(tree.find("Allgemein").find("TestlistenOrdner").text).strip()

        ## Anzahl kopfzeilen laden
        global kopfzeilen
        kopfzeilen = int(tree.find("Allgemein").find("Kopfzeilen").text.strip())

        ## Anzahl kopfzeilen laden
        global waitcount
        waitcount = int(tree.find("Allgemein").find("MaximaleWartezeit").text.strip())

        global highlight_style
        highlight_style = tree.find("Allgemein").find("HighlightStyle").text.strip()

        global jira_base_url
        jira_base_url = tree.find("Allgemein").find("Jira_Basis_URL").text.strip()
        ################################# Browser
        ## Browser Config laden
        global ChromePath
        global ChromeDriverPath
        global FirefoxPath
        global FirefoxDriverPath
        ChromePath = str(tree.find("Browser").find("Chrome").text).strip()
        ChromeDriverPath = str(tree.find("Webdriver").find("Chrome").text).strip()
        FirefoxPath = str(tree.find("Browser").find("Firefox").text).strip()
        FirefoxDriverPath = str(tree.find("Webdriver").find("Firefox").text).strip()

        ## Identifier für Testvariablen und Testdaten laden
        global testdaten_identifier_anfang
        global testdaten_identifier_ende
        global testvariablen_identifier_anfang
        global testvariablen_identifier_ende

        testdaten_identifier_anfang = str(tree.find("Allgemein").find("Testdaten").find("Identifier_Anfang").text).strip()
        testdaten_identifier_ende = str(tree.find("Allgemein").find("Testdaten").find("Identifier_Ende").text).strip()

        testvariablen_identifier_anfang = str(tree.find("Allgemein").find("Testvariablen").find("Identifier_Anfang").text).strip()
        testvariablen_identifier_ende = str(tree.find("Allgemein").find("Testvariablen").find("Identifier_Ende").text).strip()
    except Exception as e:
        pytest.fail("Fehler beim laden der \"Config.xml\"" + "\n" + str(e))
    ###############################################
    ##### Prüfen ob alle Werte korrekt gefüllt sind
    ## Allgemein
    if not path.exists(gevo_ordner):
        pytest.fail("Fehler - Überprüfen Sie die Pfade zum GeVo-Ablageort.")
    if not path.exists(testlisten_ordner):
        pytest.fail("Fehler - Überprüfen Sie die Pfade zum Testlisten-Ablageort.")
    if kopfzeilen <= 0:
        pytest.fail("Fehler - Überprüfen Sie den Konfigurationsparameter \"Kopfzeilen\".")
    if waitcount <= 0:
        pytest.fail("Fehler - Überprüfen Sie den Konfigurationsparameter \"MaximaleWartezeit\".")
    ##
    ## Browser
    if not path.exists(ChromePath) or not path.exists(ChromeDriverPath):
        pytest.fail("Fehler - Überprüfen Sie die Pfade zum Chrome-Browser und Chrome WebDriver.")
    if not path.exists(FirefoxPath) or not path.exists(FirefoxDriverPath):
        pytest.fail("Fehler - Überprüfen Sie die Pfade zum Firefox-Browser und Firefox WebDriver.")
    ##
    ## Identifier für Testvariablen und Testdaten laden
    if testdaten_identifier_anfang == "" or testdaten_identifier_ende == "":
        pytest.fail("Fehler - Überprüfen Sie die Konfigurationsparameter zu den Testdaten - Identifier.")
    if testvariablen_identifier_anfang == "" or testvariablen_identifier_ende == "":
        pytest.fail("Fehler - Überprüfen Sie die Konfigurationsparameter zu den Testvariablen - Identifier.")


###### Übergebenes Skript ausführen #######
def testfaelle_ausfuehren(self, url, testliste, zielordner, browser, headless, loglevel, jenkins_job_name):
    global name_overview_file
    ## Wenn ein Jobname übergeben wird, wird dieser als Name für die Übersichtsdatei gesetzt
    ## Falls keiner Übergeben wurde, bleibt der global definierte Standardname
    if jenkins_job_name != "":
        name_overview_file = jenkins_job_name.strip() + ".md.html"
    # global die browser variable setzen
    global test_browser
    test_browser = browser
    ### Config Datei einlesen
    ###read_config()
    ### Ende Config Einlesen
    # Tabelle für die, nach Abschluss des Testlaufs, erzeugte Übersicht
    test_overview = []
    test_overview.append("Testfallame,Testfall-Ordner,Akzeptanzkriterium,TF-Gesamt,TF-Erfolgreich,TF-Fehlerhaft")
    akzeptanzkriterium_link_erstellen("Unitop-7")
    results = []
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
                results.append(resultat)
                test_overview.append(resultat)
            else:
                print(pfad + " - Skript nicht gefunden")
        Classes.Logging.logfile_overview_abschließen(test_overview)
    else:
        # Classes.Logging.fehler_nachricht_anlegen("Fehler", "Zielordner wurde nicht gefunden - Testlauf wurde abgebrochen")
        pytest.fail("Fehler beim ausführen der Testfälle - Zielordner nicht gefunden\n->'" + zielordner + "'")
    return results

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
    testdatenpfad = (path.dirname(path.normpath(pfad)) + "\\Testdaten\\" + path.basename(path.normpath(pfad))).replace(".tc", ".xlsx")
    tablemeta.append("Testdaten-Datei,[Datei](file:/" + testdatenpfad + ")")
    ## Prüfen, ob der erzeugte Pfad auch existiert
    if not path.exists(testdatenpfad):
        #Classes.Logging.fliesstext_eintrag(testdatenpfad)
        #Classes.Logging.fehler_nachricht_anlegen("Testdaten Datei nicht gefunden", "Es wurde keine Testdatendatei
        #unter dem erwarteten Pfad ("+testdatenpfad+") gefunden")
        pytest.fail("Testdatendatei nicht gefunden")
        return
    ## aus dem erzeugten Pfad/Testdaten-Datei wird ein Data-Dictionary erzeugt
    #testdaten_dict = dict_aus_datei_erzeugen(testdatenpfad)
    global testdaten_dict
    testdaten_dict = dict_aus_excel_erzeugen(testdatenpfad)
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
            continue
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
            if len(splitted) > 5:
                if splitted[5].lower() == "optional":
                        optional = True
                else:
                    optional = splitted[5]
            else:
                optional = False
            result = 1
            # sofern ein Parameter Identifikator für die Testdaten übergeben wurde, so wird dieser ersetzt
            # Bsp. Bei Buttons wird kein weiterer Parameter erwartet, somit wäre "parameter" in diesem fall ""
            if art == "steuerung":
                result = aktion_ausfuehren(self.driver, aktion, identifier, element, parameter, t, optional)
            elif art == "gevo":
                result = gevo_ausfuehren(self.driver, aktion, t)
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
def gevo_ausfuehren(driver, aktion, tesfall_von_testdaten_dict):
    #### 0. GeVo Informationen in Log-Schreiben.
    pfad = gevo_ordner + aktion + ".gevo"
    if not path.exists(pfad):
        print("Pfad nicht gefunden - " + pfad)
        Classes.Logging.fehler_nachricht_anlegen(
            "Fehler beim ausführen des GeVos","Der GeVo konnte nicht gefunden werden - **"
                                              + pfad + "**. Der Testlauf wurde abgebrochen")
        return 0
    gevo_aktionsliste, pfad, tablemeta, tablesteps, gevo_name, gevo_akzeptanzkriterium = datei_auslesen(pfad, "gevo")

    Classes.Logging.dokumenten_header_anlegen(tablemeta, tablesteps, True)
    #### 1. GeVo-Datei öffnen
    #### 2. Schleife über GeVo-Aktionen
    #### 3. Pro Aktion "aktion_ausführen" aufrufen
    k = 0
    for k in range(len(gevo_aktionsliste)):
        gevo_splitted = gevo_aktionsliste[k].split(";")
        if len(gevo_splitted) < 5:
            nachricht = "Die Aktion in der **Zeile " + str(k + 1) + "** hat nicht genügend Parameter"
            Classes.Logging.fehler_nachricht_anlegen("Fehler in GeVo-Datei (*.gevo)",nachricht)
            return 0

        gevo_typ = gevo_splitted[0].lower()
        gevo_aktion = gevo_splitted[1].lower()
        gevo_identifier = gevo_splitted[2].lower()
        gevo_element = gevo_splitted[3]
        gevo_parameter = gevo_splitted[4]
        if len(gevo_splitted) > 5:
            if gevo_splitted[5].lower() == "optional":
                    optional = True
            else:
                optional = gevo_splitted[5]
        else:
            optional = False
        # Wenn innerhalb eines GeVo's eine Steuerungsaktion aufgerufen wird, wird die Funktion "aktion_ausführen" aufgerufen
        if gevo_typ == "steuerung":
            result = aktion_ausfuehren(driver, gevo_aktion, gevo_identifier, gevo_element, gevo_parameter,
                                   tesfall_von_testdaten_dict, optional)
        # Wenn innerhalb eines GeVo's eine GeVo-Aktion aufgerufen wird, wird die Funktion "gevo_ausführen"
        # mit der aktuellen Aktion erneut aufgerufen. Somit können GeVo's weitere GeVo's verschachtelt aufrufen
        elif gevo_typ == "gevo":
            result = gevo_ausfuehren(driver, gevo_aktion, tesfall_von_testdaten_dict)
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
def akzeptanzkriterium_link_erstellen(akz):
    req_url = jira_base_url + "/rest/api/latest/issue/" + akz
    result = requests.get(req_url, auth=('mnaas', 'start123#'), verify=False)
    if "EXISTIERT NICHT" in result.text:
        return akz + " - Jira-Vorgang existiert nicht"
    else:
        # Die für den Request erhaltene JSON ermittelt die erste hinterlegte Komponente
        # und ergänzt diese hinter den Link zum Vorgang
        json_result = result.json()
        komponente = json_result['fields']['components'][0]['name']
        return "[" + akz + "]" + "(" + jira_base_url +"/browse/"+ akz + ")" + " - (Komponente: **" + komponente + "**)"
def datei_auslesen(pfad, art):
    akzeptanzkriterium = ""
    name_aus_datei = ""
    tablemeta = []
    tablemeta.append("Feld,Wert")
    tablesteps = []
    aktionsliste = []
    tablesteps.append("Step #,typ,Aktion,Parameter")
    cnt = 1
    try:
        with open(pfad.strip(), 'r', encoding="UTF-8") as fp:
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
                                akzeptanzkriterium = akzeptanzkriterium + akzeptanzkriterium_link_erstellen(splitted_akz[i]) + "<br>"
                        else:
                            akzeptanzkriterium = akzeptanzkriterium_link_erstellen(line.strip())
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
def aktion_ausfuehren(driver, aktion, identifier, element, parameter, testfall_index, optional):
    type = ""
    par_alt = ""
    result = 0

    element, par_alt, parameter, erfolgreich = platzhalter_ersetzen(aktion, element, parameter, testfall_index)
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
        result = variablen_setzen(driver, identifier, element, parameter, False, testfall_index)
    elif aktion == "wechseln_zu":
        Classes.Logging.ueberschrift_anlegen(2, 'Wechseln zu')
        result = wechseln_zu(driver, identifier, element, parameter)
    elif aktion == "schalter_setzen":
        Classes.Logging.ueberschrift_anlegen(2, 'Schalter setzen')
        Classes.Logging.testdaten_ersetzung(par_alt, parameter, type)
        result = schalter_setzen(driver, identifier, element, parameter)
    elif aktion == "schalter_prüfen":
        Classes.Logging.ueberschrift_anlegen(2, 'Schalter prüfen')
        Classes.Logging.testdaten_ersetzung(par_alt, parameter, type)
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
    elif aktion == "testvariable_bearbeiten":
        Classes.Logging.ueberschrift_anlegen(2, 'Testvariable bearbeiten')
        zielvariable = optional
        result = testvariable_bearbeiten(driver, identifier, element, parameter, zielvariable)
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
##### Funktionen zum ersetzen von Platzhaltern
# Zählen wie viele Variablen oder Testdaten innerhalb des Strings vorhanden sind
def platzhalter_zaehlen(wert):
    return wert.count(testdaten_identifier_anfang) + wert.count(testvariablen_identifier_anfang)
    
def ersetzen(type, aktion, wert, index = -1):
    ausgabe = ""
    if type == "var":
        try:
            ausgabe = testfall_variablen[wert]
        except Exception as e:
            Classes.Logging.ueberschrift_anlegen(2, 'Testvariable')
            table = []
            table.append("Beschreibung,Wert")
            table.append("Aktion," + aktion)
            table.append("Parameter," + wert)
            table.append("Exception," + str(e).replace("," ,";"))
            Classes.Logging.fliesstext_eintrag("Beim Auflösen der Referenz (auf Testdatum oder Testvariable) ist ein "
                                               "Fehler aufgetreten. Die folgende Aktion wurde nicht durchgeführt.")
            Classes.Logging.tabelle_anlegen(table)
            Classes.Logging.fehler_nachricht_anlegen("Fehler beim lesen der Variablen",
                                                     "Die variable **" + wert + "** konnte nicht gelesen werden. "
                                                                                    "Der Testlauf wurde abgebrochen")
            return ">>>FEHLER<<<"
    elif type == "test":
        if index < 0:
            return "fehlender Index"
        try:
            # Quick and dirty solution (der Rückgabewert für das Dictionary enthält sieht wie folgt aus
            # ['<Wert>']
            # erwartet wird
            # <Wert>
            ausgabe = str(testdaten_dict[index][wert]).replace("['", "").replace("']", "")
        except Exception as e:
            Classes.Logging.ueberschrift_anlegen(2, 'Testdatum')
            table = []
            table.append("Beschreibung,Wert")
            table.append("Aktion," + aktion)
            table.append("Parameter," + wert)
            table.append("Exception," + str(e).replace(",",";"))
            Classes.Logging.fliesstext_eintrag("Beim Auflösen der Referenz (auf Testdatum oder Testvariable) ist ein "
                                               "Fehler aufgetreten. Die folgende Aktion wurde nicht durchgeführt.")
            Classes.Logging.tabelle_anlegen(table)
            Classes.Logging.fehler_nachricht_anlegen(
                "Fehler beim lesen des Testdatum", "Das Testdatum **" + wert + "** konnte nicht gelesen werden, "
                "da sie wohlmöglich nicht in der Testdaten-Datei hinterlegt ist. Der Testlauf wurde abgebrochen")
            return ">>>FEHLER<<<"
        # Alle verwendeten Testdaten werden entfernt
        # Testdaten die am Ende übrig bleiben, wurden nicht verwendet
        if wert in nicht_verwendete_testdaten:
            nicht_verwendete_testdaten.remove(wert)
    return ausgabe

def im_parameter_ersetzen(aktion, parameter, t):
    replace_string = ""
    if testdaten_identifier_anfang in parameter:
        start = parameter.find(testdaten_identifier_anfang)
        end = parameter.find(testdaten_identifier_ende, start) + 3
        replace_string = parameter[start:end]
        replace_string_cleaned = replace_string.replace(testdaten_identifier_anfang, "").replace(testdaten_identifier_ende, "")
        parameter = parameter.replace(replace_string, ersetzen("test", aktion, replace_string_cleaned, t))
    elif testvariablen_identifier_anfang in parameter:
        start = parameter.find('[var:')
        end = parameter.find(':]', start) + 2
        replace_string = parameter[start:end]
        replace_string_cleaned = replace_string.replace(testvariablen_identifier_anfang, "").replace(testvariablen_identifier_ende, "")
        parameter = parameter.replace(replace_string, ersetzen("var", aktion, replace_string_cleaned))
    return parameter, replace_string

#### Platzhalter werden ersetzt
def platzhalter_ersetzen(aktion, element, parameter, t):
    ### Platzhalter für Variablen und Testdaten ersetzen
    par_alt = parameter
    ##### Platzhalter im Parameter ersetzen
    if aktion == "variable_setzen" or aktion == "testvariable_bearbeiten":
        return element, par_alt, parameter, True
    anzahl_platzhalter = platzhalter_zaehlen(parameter)
    if anzahl_platzhalter > 0:
        for i in range(anzahl_platzhalter):
            parameter, tmep_par_alt = im_parameter_ersetzen(aktion, parameter, t)
    ##### Platzhalter im Element ersetzen
    anzahl_platzhalter = platzhalter_zaehlen(element)
    if anzahl_platzhalter > 0:
        for i in range(anzahl_platzhalter):
            element, temp_par_alt = im_parameter_ersetzen(aktion, element, t)
    # Wenn beim ersetzen ein Fehler aufgetreten ist wird die Funktion als nicht erfolgreich
    # zurückgegeben
    if parameter == ">>>FEHLER<<<":
        return "","","",False
    if element == "":
        element = parameter
    return element, par_alt, parameter, True
##### Ende aller Funktionen zum ersetzen von Platzhaltern

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
    self.driver, browser_exe_path, webdriver_exe_path = webbrowser_anlegen(browser, headless)
    if self.driver is None:
        Classes.Logging.fehler_nachricht_anlegen("Fehler", "Webdriver nicht gefunden")
        #pytest.fail("Webdriver nicht korrekt initiiert")
        return None, ""
    try:
        self.driver.delete_all_cookies();
    except Exception as e:
        Classes.Logging.exception_log("GUI-Automation -> Test vorbereiten", "Fehler beim löschen der Cookies.<br>" + str(e))
    try:
        self.driver.fullscreen_window()
    except Exception as e:
        Classes.Logging.exception_log("GUI-Automation -> Test vorbereiten", "Fehler beim wechseln zum Vollbildmodus.<br>" + str(e))
        return None, ""
    Classes.Logging.log_webdriver(self.driver, browser, browser_exe_path, webdriver_exe_path)
    result = 0
    result = url_oeffnen(self.driver, url, headless)
    if result == 0:
        self.driver.close()
        self.driver.quit()
        Classes.Logging.fehler_nachricht_anlegen("Fehler beim öffnen der Seite",
                                                 "Beim öffnen der Seite ist ein Fehler aufgetreten")
        #pytest.fail("Fehler beim öffnen der Seite")
        return None, ""
    # Wechselt automatisch zu dem gewünschten Frame
    Classes.Logging.ueberschrift_anlegen(2, "Wechseln zu IFrame")
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
    nicht_verwendete_testdaten_ausgeben()
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
                options.headless = True
            else:
                options.headless = False
            options.binary_location = FirefoxPath
            # Capabilities
            caps = webdriver.DesiredCapabilities.FIREFOX.copy()
            caps["marionette"] = True
            caps['platform'] = "WINDOWS"
            caps["wires"] = True
            driver = webdriver.Firefox(executable_path=FirefoxDriverPath, options=options, capabilities=caps)
            #driver = webdriver.Firefox(executable_path=GeckoDriverManager.install(), options=options)
            return driver, FirefoxPath, FirefoxDriverPath
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
            return driver, ChromePath, ChromeDriverPath
    except Exception as e:
        Classes.Logging.exception_log("GUI-Automation -> Webbrowser anlegen", "Fehler beim anlegen des Webdrivers <br>" + str(e))
        return None


###### beendet alle Tasks für den übergebenen Browser
def kill_tasks(target_browser):
    command_1 = ""
    command_2 = ""
    ausgabe_err_1 = ""
    ausgabe_1 = ""
    ausgabe_err_2 = ""
    ausgabe_2 = ""
    if target_browser == "chrome":
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
    elif target_browser == "firefox":
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
def url_oeffnen(driver, pageUrl, headless):
    Classes.Logging.ueberschrift_anlegen(2, "Webseite öffnen")
    table = []
    table.append("Beschreibung,Wert")
    table.append("URL," + pageUrl)
    Classes.Logging.tabelle_anlegen(table)
    Classes.Logging.screenshot_anlegen(driver)
    try:
        driver.get(pageUrl)
        Classes.Logging.fliesstext_eintrag("Die URL wurde mit dem Browser geöffnet")
    except Exception as e:
        Classes.Logging.fliesstext_eintrag("Fehler beim öffnen Webseite")
        Classes.Logging.exception_log("GUI-Automation -> URLOeffnen", str(e))

    if headless == 0:
        try:
            driver.maximize_window()
        except:
            Classes.Logging.fliesstext_eintrag("Fehler beim maximieren Webseite")
            Classes.Logging.exception_log("GUI-Automation -> URLOeffnen", str(e))

    result = benutzer_anmelden(driver, "mnaas@soka-dach.de", "start123#")
    #### Anmeldung war erfolgreich
    if result == 1:
        Classes.Logging.erfolg_nachricht_anlegen("Die Anmeldung wurde erfolgreich durchgeführt")
        return 1
    #### Anmeldung war nicht erfolgreich
    else:
        Classes.Logging.fehler_nachricht_anlegen("Fehler beim Erzeugen des WebDrivers",
                                                 "Bei der Anmeldung ist ein Fehler aufgetreten. Die "
                                                 "Anmeldung konnte nicht durchgeführt werden")
        return 0

###############
###### Webseite per Uebergebene URL oeffnen
def benutzer_anmelden(driver, benutzername, passwort):
    ## Benutzername eintragen
    ## Logging
    Classes.Logging.ueberschrift_anlegen(2, 'Anmeldung')
    table = []
    table.append("Attribut,Wert")
    table.append("Seitentitel," + driver.title)
    table.append("Benutzername," + benutzername)
    Classes.Logging.tabelle_anlegen(table)
    lowered_page_title = str(driver.title).lower()
    if lowered_page_title == "sign in to your account" or lowered_page_title == "bei ihrem konto anmelden":
        #### Es wurde bereits eine Anmeldung mit einem Nutzer durchgeführt
        #### Die Benutzerdaten sind hinterlegt und müssen zur Anmeldung ausgewählt werden.
        lowered_pagesource = str(driver.page_source).lower()
        ## Es wird nach dem Benutzernamen gesucht
        ##      -> ist dieser Vorhanden wird er geklickt
        ##      -> ist er nicht vorhanden, wird der Benutzername und das Passwort eingetragen
        if lowered_pagesource.find(benutzername):
            Classes.Logging.fliesstext_eintrag("Es wird eine Anmeldung durchgeführt")
            #Benutzername setzen
            element_setzen(driver, "name", "loginfmt", benutzername)
            # nicht notwendig, da ein Enter bei elemente_setzen durchgeführt wird - Next Klicken
            #element_klicken(driver, "id","idSIButton9")
            # Passwort setzen
            element_setzen(driver, "name", "passwd", passwort)
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
            element_pruefen(driver, "xpath", "//div[contains(text(),'"+ benutzername +"')]", benutzername)
            element_klicken(driver, "xpath", "//div[contains(text(),'"+ benutzername +"')]")
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
            "Der Seitentitel  (**" + driver.title + "**) der geöffneten Seite entsprach keinem der erwarteten Titel")
        return 0


########################
# Verwaltet die zusätzlichen Variablen
# type = read  ->  Variable wird ausgelesen
# type = write   ->  Variable wird gesetzt/aktualisiert
def variablen_setzen(driver, identifier_type, identifier, parameter, variable_bearbeiten = False, testfall_index = 1):
    global testfall_variablen
    parameter = parameter.replace(testvariablen_identifier_anfang,"").replace(testvariablen_identifier_ende,"")
    if variable_bearbeiten == False and str(identifier_type).lower() != "variable":
        element = get_element(driver, identifier_type, identifier)
        if element is None:
            eintrag = 'Fehler beim setzen der Variable (**%s**) auf Basis des Element-Wertes (**%s**). Das übergebene ' \
                      'Element konnte nicht identifiziert werden.' % (parameter, identifier)
            Classes.Logging.fehler_nachricht_anlegen("Fehler beim setzen der Variablen", eintrag)
            return 0
        ## Logging
        if "/input" in identifier.lower():
            wert = element.get_attribute("value")
            Classes.Logging.notiz_anlegen("Die Variable wird auf den Attribut-Wert **value** des Elements gesetzt.")
        else:
            wert = element.text
            Classes.Logging.notiz_anlegen("Die Variable wird auf den **Textinhalt** des Elements gesetzt.")
    else:
        ## Wenn die Testvariable bearbeitet wird, wird im Parameter der Name der Variablen übergeben
        ## Im Identifiert wird der neue Inhalt der Variablen übergeben
        element, par_alt, identifier, result = platzhalter_ersetzen("", "", identifier, testfall_index)
        if result == False:
            eintrag = 'Das Testdatum (**%s**) konnte nicht mit einem Wert aus der Testdaten-Datei erstetzt werden. Bitte überprüfen sie die Zuweisung und die Testdaten-Datei.' % (par_alt)
            Classes.Logging.fehler_nachricht_anlegen("Fehler beim ersetzen der Variablen", eintrag)
        wert = str(identifier)
    try:
        testfall_variablen[parameter] = wert
    except Exception as e:
        Classes.Logging.exception_log("GUI-Automation -> Variable Setzen", str(e))
        eintrag = 'Fehler beim setzen der Variable (**%s**) auf Basis des Element-Wertes (**%s**)' % (parameter, identifier)
        Classes.Logging.fehler_nachricht_anlegen("Fehler beim setzen der Variablen", eintrag)
        return 0
    if parameter not in testfall_variablen:
        ## Logging
        eintrag = 'Die Variable (**%s**) mit dem Wert (**%s**) wurde hinzugefügt' % (parameter, wert)
        Classes.Logging.fliesstext_eintrag(eintrag)
    else:
        ## Logging
        eintrag = 'Die Variable (**%s**) mit dem Wert (**%s**) wurde auf den Wert (**%s**) geändert' % (parameter, testfall_variablen[parameter], wert)
        Classes.Logging.fliesstext_eintrag(eintrag)
    return 1

###### Element setzen
def element_setzen(driver, identifier_type, identifier, wert):
    ## Wert eintragen
    ########################
    element = get_element(driver, identifier_type, identifier)
    ## Logging
    if element is None:
        eintrag = 'Fehler beim setzen von (**%s**) auf den Wert (**%s**)' % (identifier, wert)
        Classes.Logging.fehler_nachricht_anlegen("Fehler beim setzen des Elementes", eintrag)
        return 0
    ### Wenn das Element ein Input Element mit dem Attribut "Checkbox" ist, dann wird die Aktion mit einem Fehler abgebrochen
    ### Gegebenfalls kann hier ein Absprung in die Funktion Schalter_Setzen automatisch erfolgen
    if str(element.get_attribute("type")) == "checkbox":
        eintrag = 'Fehler beim setzen von (**%s**) auf den Wert (**%s**). <br>Bitter verwenden Sie die Funktion ' \
                  '"Schalter_setzen" um den Wert einer Checkbox zu ändern' % (identifier, wert)
        Classes.Logging.fehler_nachricht_anlegen("Fehler beim setzen des Elementes", eintrag)
        return 0
    ## Wenn an das Element ausschließlich eine Enter Taste gesendet werden soll, werden im
    ## Anschluss keine weiteren Aktionen (innerhalb dieser Funktion) durchgeführt
    if wert == "[RETURN]":
        try:
            element.send_keys(Keys.RETURN)
            return 1
        except Exception as e:
            eintrag = 'Fehler beim senden der ENTER-Taste für das Element (**%s**)' % (identifier)
            Classes.Logging.fehler_nachricht_anlegen("Fehler beim setzen des Elementes", eintrag)
            Classes.Logging.exception_log("GUI-Automation -> Element setzen", str(e))
            return 0
    ## Alle Element (außer Select) werden vor dem Setzen des Wertes geleert
    if "/select" not in identifier:
        try:
            element.clear()
        except Exception as e:
            Classes.Logging.notiz_anlegen("Das Element " + identifier + " konnte nicht geleert werden")
            Classes.Logging.exception_log("GUI-Automation -> Element setzen", str(e))
    ##################
    try:
        element.send_keys(wert)
    except Exception as e:
        eintrag = 'Fehler beim setzen von (**%s**) auf den Wert (**%s**)' % (identifier, wert)
        Classes.Logging.fehler_nachricht_anlegen("Fehler beim setzen des Elementes", eintrag)
        Classes.Logging.exception_log("GUI-Automation -> Element setzen", str(e))
        return 0
    try:
        element.send_keys(Keys.RETURN)
    except Exception as e:
        Classes.Logging.notiz_anlegen("RETURN konnte nicht an das Element + " + identifier + " gesendet werden")
        Classes.Logging.exception_log("GUI-Automation -> Element setzen", str(e))

    eintrag = 'Das Element (**%s**) wurde auf den Wert (**%s**) gesetzt' % (identifier, wert)
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
    count = 0
    sleeptime = 1
    while True:
        try:
            if wert == element.text or element.get_attribute("value") == wert or ("/select" in identifier and element.get_attribute("title") == wert):
                if wert == element.text:
                    eintrag = 'Der Wert (**%s**) entspricht dem erwarteten Wert (**%s**). Es wurde der Elementtext geprüft' % (element.text, wert)
                elif element.get_attribute("value") == wert:
                    eintrag = 'Der Wert (**%s**) entspricht dem erwarteten Wert (**%s**). Es wurde der Elementvalue geprüft' % (element.get_attribute("value"), wert)
                elif element.get_attribute("title") == wert:
                    eintrag = 'Der Wert (**%s**) entspricht dem erwarteten Wert (**%s**). Es wurde der Elementtitel geprüft' % (element.get_attribute("title"), wert)
                Classes.Logging.erfolg_nachricht_anlegen(eintrag)
                return 1
        except Exception as e:
            element = get_element(driver, identifier_type, identifier)
            Classes.Logging.exception_log("GUI-Automation -> Element prüfen", str(e))
        if wert != element.text and element.get_attribute("value") != wert or ("/select" in identifier and element.get_attribute("title") != wert):
            time.sleep(sleeptime)
        count = count + 1
        if count >= waitcount:
            break
    styled_screenshot(driver, element)
    if wert != element.text and element.get_attribute("value") != wert or ("/select" in identifier and element.get_attribute("title") != wert):
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
            Classes.Logging.exception_log("GUI-Automation -> Element enthält Wert prüfen", str(e))

        if wert in element.text:
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
            zusatz = "<br>**Das Element wurde erneut gesetzt und der Testlauf wird fortgesetzt.**"
            Classes.Logging.exception_log("GUI-Automation -> Element enthält Wert nicht", str(e) + zusatz)
        time.sleep(sleeptime)
        count = count + 1
        if count >= waitcount:
            break
    if element is None:
        # Der Testlauf wird mit einer Warnung fortgesetzt
        eintrag = 'Das Element (**%s**) konnte nicht auf den Wert (**%s**) geprüft werden, da das Element nicht vorhanden war' % (identifier , wert)
        Classes.Logging.warnung_anlegen(eintrag)
        styled_screenshot(driver, element)
        return 1
    if wert in element.text:
        # Der Testlauf wird mit mit einer Fehlermeldung abgebrochen
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
def schalter_setzen(driver, identifier_type, identifier, wert, anzahl_versuche = 3):
    element = get_element(driver, identifier_type, identifier)
    # Wenn kein korrekter Wert übergeben wurde, wird der Wert auf Nein gesetzt
    if wert is None or wert == "":
        Classes.Logging.notiz_anlegen("Es wurde kein korrekter Wert für einen Schalter übergeben. Bitte übergeben Sie "
                                      "nur die Werte (**Ja**) oder (**Nein**). <br>Der übergebene Wert (**" + wert + "**) kann "
                                      "nicht für einen Schalter gesetzt werden und wurde durch (**Nein**) ersetzt")
        wert = "Nein"
    if element is None:
        eintrag = 'Fehler beim setzen des Schalter (**%s**) - auf den Wert (**%s**)' % (identifier, wert)
        Classes.Logging.fehler_nachricht_anlegen("Fehler setzen des Schalters", eintrag)
        #pytest.fail(element + " = None")
        return 0
    # Wenn der Wert auf den der Schalter gesetzt werden soll != "ja" oder "nein" ist, wird der Testlauf abgebrochen
    if str(wert).lower() != "ja" and str(wert).lower() != "nein":
        Classes.Logging.fehler_nachricht_anlegen("Fehler setzen des Schalters",
                                                 "Der Schalter kann ausschließlich auf die Werte **Ja** oder **Nein** "
                                                 "gesetzt werden.<br> Bitte prüfen sie die Aktion/Testdaten-Datei auf "
                                                 "den korrekten Wert")
        return 0
    styled_screenshot(driver, element)
    # Wenn das element keine Checkbox ist, wird ein Fehler zurückgegeben
    try:
        type = str(element.get_attribute("type")).lower()
        if type != "checkbox":
            Classes.Logging.fehler_nachricht_anlegen("Element nicht korrekt","Das zu setzende Element ist keine Checkbox")
            return 0
    except:
        Classes.Logging.fehler_nachricht_anlegen("Element nicht korrekt","Das zu setzende Element ist keine Checkbox")
        return 0
    # Aktuellen Schalterwert auslesen
    schalter_wert = str(element.get_attribute("title")).lower()
    # Wenn Schalterwert == Zielwert -> Erfolg wird geloggt
    if schalter_wert == str(wert).lower():
        eintrag = 'Das Element (**%s**) entspricht dem erwarteten Wert (%s)' % (identifier, wert)
        Classes.Logging.erfolg_nachricht_anlegen(eintrag)
    # Wenn der Schalterwert != Zielwert ist -> Schalter wird geklickt und die Funktion wird erneut ausgerufen
    else:
        eintrag = 'Das Element (**%s**) entspricht nicht dem erwarteten Wert (%s) und wird nun geklickt' % (identifier, wert)
        Classes.Logging.fliesstext_eintrag(eintrag)
        element_klicken(driver, identifier_type, identifier)
        anzahl_versuche -= 1
        if anzahl_versuche > 0:
            schalter_setzen(driver, identifier_type, identifier, wert, anzahl_versuche)
        else:
            Classes.Logging.fehler_nachricht_anlegen("Fehler setzen des Schalters", "Es wurde nach 3 Versuchen nicht das erwartete Ergebnis (**"+ wert + "**) erzielt")
            return 0
        #driver.execute_script("arguments[0].title = '" + str(wert) + "'", element)
    return 1


##### Zum prüfen von Checkboxen mittels Titel des Input-Tags
def schalter_prüfen(driver, identifier_type, identifier, wert):
    element = get_element(driver, identifier_type, identifier)
    if element is None:
        eintrag = 'Fehler beim setzen des Schalter (**%s**) - auf den Wert (**%s**) - Das Element wurde nicht gefunden' % (identifier, wert)
        Classes.Logging.fehler_nachricht_anlegen("Fehler setzen des Schalters", eintrag)
        #pytest.fail(element + " = None")
        return 0

    styled_screenshot(driver, element)

    # Wenn das element keine Checkbox ist, wird ein Fehler zurückgegeben
    try:
        type = str(element.get_attribute("type")).lower()
        if type != "checkbox":
            return 0
    except:
        Classes.Logging.fehler_nachricht_anlegen("Element nicht korrekt","Das zu setzende Element ist keine Checkbox")
        return 0

    if str(element.get_attribute("title")).lower() == str(wert).lower():
        eintrag = 'Das Element (**%s**) entspricht dem erwarteten Wert (%s)' % (identifier, wert)
        Classes.Logging.erfolg_nachricht_anlegen(eintrag)
        return 1
    else:
        eintrag = 'Das Element (**%s**) entspricht nicht dem erwarteten Wert (%s) - aktueller Wert ist (%s)' % (identifier, wert, element.get_attribute("title"))
        Classes.Logging.fehler_nachricht_anlegen("Schalter entspricht nicht erwartetem Wert", eintrag)
        return 0
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
        new_identifier = identifier + "//span[@class=\"ms-nav-columns-caption icon-RightCaret-after\"]"
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
    count = 2
    if str(type).lower() == "appear":
        while True:
            element = get_element(driver, identifier_type, identifier, show_error=False)
            if element is None:
                time.sleep(1)
            count = count - 1
            if element is not None or count <= 0:
                break
        if element is None:
            Classes.Logging.fehler_nachricht_anlegen(
                "Fehler beim Warten", "Fehler beim Warten auf das anzeigen des Elements - **" +
                identifier + "**. Es wurde nach **" + str(int(waitcount)) + "** Versuchen abgebrochen")
            return 0
        else:
            Classes.Logging.erfolg_nachricht_anlegen("Das Element - **" + identifier + "** ist vorhanden.")
            return 1
    elif str(type).lower() == "gone":
        while True:
            element = get_element(driver, identifier_type, identifier, show_error=False)
            if element is not None:
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
                identifier + "**. Es wurde nach **" + str(int(waitcount)) + "** Versuchen abgebrochen")
            return 0
    Classes.Logging.warnung_anlegen("Es wurde ein nicht unterstützter Typ übergeben.<br>Erwartet wurde:"
                                    "<br> - Appear<br> - Gone<br>Tatsächlich übergeben wurde ->" + type + "<-" +
                                    "Es wurde nicht auf das Element gewartet.")

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
        try:
            # Die Config Datei wir mittels XML-Parser eingelesen
            tree = ET.parse(config_file_pfad)
            waitcount = int(tree.find("Allgemein").find("MaximaleWartezeit").text)
        except Exception as e:
            Classes.Logging.exception_log("GUI-Automation -> Wartezeit Timeout setzen", str(e))
            return 0
    else:
        waitcount = int(wert)
    Classes.Logging.notiz_anlegen("Die Wartezeit bis zu einem Timeout wurde auf *" + str(waitcount) + "* sekunden gesetzt")
    return 1

def testvariable_bearbeiten(driver, identifier_type, identifier, wert, zielvariable):
    ##### String operationen ###############
    #### Der Wert des zu modifizierenden Platzhalters wird geladen
    element, par_alt, variablen_wert, result1 = platzhalter_ersetzen("", "", wert, 0)
    #### Der Wert eines möglichen Platzhalters innerhalb des Modifikationsparameter wird geladen
    element, par_alt, identifier, result2 = platzhalter_ersetzen("", "", identifier, 0)
    if result1 == False or result2 == False :
        # Wenn bei einem der Ersetzungen ein Fehler auftritt wird die Aktion fehlerhaft beendet
        Classes.Logging.fehler_nachricht_anlegen(
            "Fehler beim bearbeiten der Testvariablen", "Beim ersetzen der Testvariablen ist ein Fehler aufgetreten."
                                                        "Die Testvariable **" + wert + "** konnte nicht geladen werden.")
        return 0
    if identifier_type == "substring_entfernen":
        temp_string = variablen_wert
        temp_string = temp_string.replace(identifier, "")
        Classes.Logging.erfolg_nachricht_anlegen("Der Substring **" + identifier + "** wurde aus der Testvariablen **"
                                                 + wert + "** entfernt.")
    elif identifier_type == "präfix_ergänzen":
        temp_string = variablen_wert
        temp_string = str(identifier) + temp_string
        Classes.Logging.erfolg_nachricht_anlegen("Der Präfix **" + identifier + "** wurde vor der Testvariablen **"
                                                 + wert + "** ergänzt.")
    elif identifier_type == "suffix_ergänzen":
        temp_string = variablen_wert
        temp_string = temp_string + str(identifier)
        Classes.Logging.erfolg_nachricht_anlegen("Der Präfix **" + identifier + "** wurde hinter der Testvariablen **"
                                                 + wert + "** ergänzt.")
    ##### Zahlen operationen ###############
    elif identifier_type == "addieren" or identifier_type == "substrahieren" or identifier_type == "multiplizieren" or identifier_type == "dividieren":
        temp_string = calculate(variablen_wert, identifier, identifier_type)
    ##### Handhabung nicht vorhandener Operationen ###############
    else:
        Classes.Logging.fehler_nachricht_anlegen(
            "Fehler beim bearbeiten der Testvariablen", "Beim bearbeiten der Testvariablen ist ein Fehler aufgetreten."
                                                        "Der Befehlt **" + identifier_type + "** wurde nicht gefunden")
        return 0
    if zielvariable == "":
        variablen_setzen(driver, "", temp_string, wert, True)
    else:
        variablen_setzen(driver, "", temp_string, zielvariable, True)
    return 1

### Übergebene Strings werden in "int" oder "float" geparsed und entsprechend dem übergebenen identifier_type
###  * addiert
###  * subtrahiert
###  * multipliziert
###  * dividiert
### Der berechnete Wert wird als String zurückgegeben
def calculate(number1, number2, identifier_type):
    converted_number1 =  int_or_float(number1)
    converted_number2 =  int_or_float(number2)
    if converted_number1 == "NaN" or converted_number1 == "NaN":
        return 0
    if identifier_type == "addieren":
        result = str((converted_number1 + converted_number2))
        Classes.Logging.erfolg_nachricht_anlegen("Der Wert1 **" + str(converted_number1) + "** und  **" + str(converted_number2)
                                                 + " wurden addiert.")
        return result
    elif identifier_type == "substrahieren":
        result = str((converted_number1 - converted_number2))
        Classes.Logging.erfolg_nachricht_anlegen("Der Wert2 **" + str(converted_number2) + "** wurde von Wert1 **" + str(converted_number1)
                                                 + " subtrahiert.")
        return result
    elif identifier_type == "multiplizieren":
        result = str((converted_number1 * converted_number2))
        Classes.Logging.erfolg_nachricht_anlegen("Der Wert1 **" + str(converted_number1) + "** und  **" + str(converted_number2)
                                                 + " wurden multipliziert.")
        return result
    elif identifier_type == "dividieren":
        result = str((converted_number1 / converted_number2))
        Classes.Logging.erfolg_nachricht_anlegen("Der Wert1 **" + str(converted_number1) + "** wurde durch Wert 2"
                                                "  **" + str(converted_number2) + " dividiert.")
        return result

    return 0

### Versucht einen übergeben String auf "int" und "float" zu parsen
def int_or_float(number):
    try:
        numberint = int(number)
        return numberint
    except ValueError:
        print("not an int")
    try:
        numberfloat = float(number)
        return numberfloat
    except ValueError:
        print("not a float")
    return "NaN"

###############

def get_element(driver, identifier_type, identifier, is_button = True, show_error = True):
    element = None
    identifier = str(identifier)

    identifier_type_lower = identifier_type.lower()
    ### Sofern kein valider identifier_type übergeben wurde, wird standardmäßig die ID verwendet
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
    elif identifier_type_lower == "variable":
        Classes.Logging.notiz_anlegen("Aufgrund der Zuweisung einer Variablen wird keine Elementidentifikation durchgeführt")
        return None
    else:
        Classes.Logging.fehler_nachricht_anlegen("Fehler beim identifizieren",
                                                 "Es wurde ein nicht untertützter Identifier-Typ übergeben - **" + identifier_type + "**")
        return None
    if is_button == False:
        ### Wenn es kein Button ist, wird gewartet, bis das Element lokalisiert werden kann
        element = WebDriverWait(driver, waitcount).until(EC.presence_of_element_located((by_type, identifier)))
    else:
        ### Wenn es ein Button ist, wird gewartet, bis das Element geklickt werden kann
        try:
            element = WebDriverWait(driver, waitcount).until(EC.element_to_be_clickable((by_type, identifier)))
            WebDriverWait(driver, waitcount).until(EC.visibility_of(element))
            #element = WebDriverWait(driver, waitcount).until(EC.element_to_be_clickable(element))
        except Exception as e:
            element = None
            if show_error == True:
                Classes.Logging.exception_log("GUI-Automation -> Get Element", str(e))
                if len(driver.find_elements(by_type, identifier)) > 1:
                    Classes.Logging.fehler_nachricht_anlegen(
                        "Fehler beim identifizieren", "Fehler beim identifizieren des Elements - **" +
                        identifier + "**. Es kein eindeutiges Element gefunden")
                elif len(driver.find_elements(by_type, identifier)) == 0:
                    Classes.Logging.fehler_nachricht_anlegen(
                        "Fehler beim identifizieren", "Fehler beim identifizieren des Elements - **" +
                        identifier + "**. Es konnte kein Element identifiziert werden.")
            return element
    if element is None:
        ### Wenn das Element == None ist, wurde kein Element gefunden und eine Fehlernachricht erzeugt
        ### Die Funktion wird an dieser Stelle dann verlassen
        if show_error == True:
            Classes.Logging.fehler_nachricht_anlegen(
                "Fehler beim identifizieren", "Fehler beim identifizieren des Elements - **" +
                identifier + "**. Es wurde nach **" + str(waitcount) + "** Sekunden ein Timeout erzeugt")
        return None
    ### Es wird zu dem ermittelten Element gesprungen
    actions = ActionChains(driver)
    actions.move_to_element(element).perform()
    try:
        actions.move_to_element(element).perform()
        #driver.execute_script("arguments[0].scrollIntoView(true);", element)
    except Exception as e:
        Classes.Logging.exception_log("GUI-Automation -> Get Element", str(e))
        if show_error == True:
            Classes.Logging.warnung_anlegen("Es konnte nicht mittels switch zum Element gewechselt werden. Die Testdurchführung"
                                            "wird fortgesetzt.")
    eintrag = ""
    ### Logging
    if identifier != "":
        eintrag = 'Das folgende Element (**%s**) wurde mittels dem folgenden (**%s**) selektiert.<br>**%s** = (**%s**)' % (element, identifier_type, identifier_type, identifier)
    else:
        eintrag = 'Das folgende Element (**%s**) wurde mittels (**%s**) selektiert' % (identifier, identifier_type)
    Classes.Logging.fliesstext_eintrag(eintrag)
    Classes.Logging.log_element(element)
    Classes.Logging.screenshot_von_element_anlegen(element)
    return element
# ----------------------------------------------------------------------------------------------------------------------
# Diese Funktion ist vorerst obsolet, da von CSV auf Excel-Dateien gewechselt wurde
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
    except:
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
# Diese Funktion ist vorerst obsolet, da von CSV auf Excel-Dateien gewechselt wurde
# ----------------------------------------------------------------------------------------------------------------------
#### Excel zu Dictionary
def dict_aus_excel_erzeugen(testdatenpfad):
    # Wenn die Testdaten eingelesen werden, wird die Liste der verwendeten Testdaten zurückgesetzt
    global verwendete_testdaten
    verwendete_testdaten = {}
    workbook = xlrd.open_workbook(testdatenpfad, on_demand = True)
    worksheet = workbook.sheet_by_index(0)
    first_row = [] # Kopfzeile der Tabelle
    for col in range(worksheet.ncols):
        first_row.append( str(worksheet.cell_value(0,col)) )
    global nicht_verwendete_testdaten
    nicht_verwendete_testdaten = first_row.copy()
    # Workbook wird in Dictionary umgewandelt
    dict_list =[]
    for row in range(1, worksheet.nrows):
        elm = {}
        for col in range(worksheet.ncols):
            #elm[first_row[col]]=str(worksheet.cell_value(row,col))
            elm[first_row[col]] = str(worksheet.cell(rowx=row, colx=col).value)
        dict_list.append(elm)
    return dict_list

## Es wird ein Screenshot erzeugt mit entsprechender Markierung an dem selektierten Element
def styled_screenshot(driver, element):
    try:
        # aktuellen Style sichern um ihn wieder zurücksetzen zu können
        original_style = element.get_attribute('style')
        # Style zum hervorheben von Elementen übergeben/setzen
        style_setzen(driver, element, highlight_style)
        # Screenshot erstellen
        Classes.Logging.screenshot_anlegen(driver)
        # Style zurücksetzen
        style_setzen(driver, element, original_style)
    except:
        Classes.Logging.notiz_anlegen("Der Style zum markieren innerhalb des Screenshots konnte nicht gesetzt werden")

## Style wird am Element gesetzt
def style_setzen(driver, element, style):
    try:
        # übergebenen Style setzen
        driver.execute_script("arguments[0].setAttribute('style', arguments[1]);",
                          element, style)
    except:
        Classes.Logging.notiz_anlegen("Der übergebene Style für das element **" + str(element) + "** konnte nicht gesetzt werden")
        # Fehlverhalten hat keine Auswirkungen auf den Testablauf

### Um in Jekins die Lauf des Jobs ggf aufs Fehlerhaft zu setzen werden hier die erzielten Testfalldurchführungsresultate geprüft
### Es werden ausschließlich fehlerhafte Testfalldurchführungen ausgegeben
### - Konsolenausgabe in Jenkins -
def ausgabe_jenkins(results):
    try:
        failed = 0
        gesamt = 0
        ## Es wird durch die Liste der Rückgabewerte gegangen um die letzten Elemente (Anzahl Testfälle pro Testfallablauf & Anzahl fehlerhaften Testfalldurchführungen) gegangen
        ## Diese Zahlen werden jeweil summiert
        ##      - Anzahl fehlerhaft > 0 => Testlauf wird auf fehlerhaft gesetzt
        line = "-----------------------------------------------------------------------------------------"
        space = "    "
        print(line)
        print("########################### Zusammenfassung der Testresultate ###########################")
        ## Liste der fehlgeschlagenen Testfalldruchläufe wird ausgegeben
        for i in range(len(results)):
            splitted = results[i].split(",")
            testfallname = splitted[0]
            resultat_ordner = splitted[1]
            temp_gesamt = int(splitted[3])
            temp_failed = int(splitted[5])
            # Wenn das Resultat Fehlerhaft ist, wird eine Zeile in der Konsole ausgegeben
            if temp_failed > 0:
                print(space + str(i+1) + ". " + testfallname + " (" + resultat_ordner + ") -  Fehlerhaft ("
                      + str(temp_failed) + "/" + str(temp_gesamt) + ")")
            gesamt += temp_gesamt
            failed += temp_failed
        # Unter die Liste wird zusammengefasst dargestellt, wie viele der durchgeführten Testfalldurchläufe (Je Testdatensatz
        # ein durchlauf) fehlerhaft durchgeführt wurden
        if failed > 0:
            print(line)
            print("(" + str(failed) + "/" + str(gesamt) + ") der Testfalldurchführungen wurden fehlerhaft beedet.\n"
                  + "Weitere Informationen finden sie innerhalb der Testdokumentationen (F:\\Testresultate\\)")
            print(line)
            pytest.fail("Fehlerhaft")
    except Exception as e:
        print("Fehler beim erstellen der Jenkins Resultate.\nFehlermeldung: " + str(e))

### Erstellt eine Testfall liste (Liste mit absoluten Pfaden zu "*.tc" Dateien) und gibt diese zurück
### Übergeben wird ein Name der Testfallliste-Datei (Zeilenweise Auflistung von absoluten Testfallpfäden)
def testfallliste_aus_datei_erzeugen(testlisten_datei):
    testliste = []
    # Wenn ein Fehler innerhalb der Liste ist, wird das einlesen Abgebrochen
    hasfailure = False
    pfad = testlisten_ordner + testlisten_datei

    if not path.exists(pfad):
        print(pfad + " nicht gefunden")
        #return None

    try:
        with open(pfad.strip(), 'r', encoding="UTF-8") as fp:
            line = fp.readline()
            while line:
                testliste.append(line.strip())
                line = fp.readline()
    except Exception as e:
        print("Fehler beim einlesen der Testliste - " + pfad)
        print("Exception - " + str(e))
        return None
    if hasfailure:
        return None
    else:
        return testliste
### Erstellt eine Testfall liste (Liste mit absoluten Pfaden zu "*.tc" Dateien) und gibt diese zurück
### Übergeben wird ein ";"-separierter String mit Ordner für die eine Liste erstellt werden soll
def testfallliste_erzeugen(testfall_ordner, unterordner = True):
    # Ordnerliste wird getrennt
    splitted = testfall_ordner.strip().split(";")
    # Dateien mit der Endung "*.tc" aus dem übergebenen Ordner holen
    testliste = []
    sub_ordner_liste = []
    # Schleife über alle Einträge der Liste "splitted"
    for i in range(len(splitted)):
        ordner = splitted[i]
        try:
            # für jeden Ordner werden die Dateien mit der Endung "*.tc" aufgelistet (in testliste)
            sub_ordner_liste, testliste = run_fast_scandir(testliste, ordner, [".tc"], unterordner)
        except:
            pytest.fail("Fehler - Beim lesen des Testfallordners ist ein Fehler aufgetreten")
            return None

    # Prüfen ob Testfallabläufe in dem Ordner sind
    if range(len(testliste)) == 0:
        pytest.fail("Fehler - Es wurden keine Testfallabläufe in dem Verzeichnis gefunden")
        return None

    return testliste

# Ordner mit unterordnern rekursiv einlesen
def run_fast_scandir(testliste, dir, ext, sub_folder = True):    # dir: str, ext: list
    subfolders = []
    # aktueller Ordner und darin enthaltene Dateien werden der Liste hinzugefügt
    for f in os.scandir(dir):
        if f.is_dir() and sub_folder == True:
            subfolders.append(f.path)
        if f.is_file():
            if os.path.splitext(f.name)[1].lower() in ext:
                testliste.append(f.path)
    # Wenn unterordner eingelesen werden sollen, wird die Funktion rekursiv aufgerufen und
    # ergänzt die Unterordner und Dateien je Unterordner
    if sub_folder == True:
        for dir in list(subfolders):
            sf, f = run_fast_scandir(testliste, dir, ext, sub_folder)
            # entfernt duplikate aus der Liste
            # Die Differenz zwischen den Listen wird der Testfalliste hinzugefügt
            sf = list(set(subfolders) - set (sf))
            subfolders.extend(sf)
            # entfernt duplikate aus der Liste
            # Die Differenz zwischen den Listen wird der Testfalliste hinzugefügt
            f = list(set(testliste) - set (f))
            testliste.extend(f)
    return subfolders, testliste

def nicht_verwendete_testdaten_ausgeben():
    # Test
    Classes.Logging.ueberschrift_anlegen(2, "Nicht verwendete Testdaten")
    Classes.Logging.fliesstext_eintrag("Die folgenden Testdaten waren in der Testdatendatei vorhanden, wurde jedoch im "
                                       "Laufe der Testfalldurchführung nicht von einer Aktion verwendet.")
    nicht_verwendete_testdaten.insert(0, "Nicht verwendete Testdaten,Beschreibung")
    if range(len(nicht_verwendete_testdaten)) == 1:
        nicht_verwendete_testdaten.append("Keine,-")
    else:
        for i in range(len(nicht_verwendete_testdaten)):
            if i>0:
                nicht_verwendete_testdaten[i] = nicht_verwendete_testdaten[i] + ",Testdatum wurde nicht verwendet"
    Classes.Logging.tabelle_anlegen(nicht_verwendete_testdaten)
    Classes.Logging.fliesstext_eintrag("Alle nicht verwendeten Testdaten können aus der Testdatendatei entfernt werden.")
    Classes.Logging.notiz_anlegen("Sollte der Testlauf vorzeitig abgebrochen werden, ist die Liste nicht aussagekräftig, "
                                  "da die Testschritte nach dem Fehlereintritt nicht mehr berücksichtigt werden.<br>"
                                  "Zudem ist es möglich, das ein Testdatum doppelt in der Testdaten-Datei vorhanden ist.")