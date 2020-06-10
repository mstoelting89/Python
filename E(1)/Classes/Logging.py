import datetime
from os import path
from selenium import webdriver
import os

### LogFile Variable
LogFilePath = ""
LogFileParentFolder = ""
MarkDeepPfad = "G:/Projekte/GOB/02_Teilprojekte/06_Test/Testautomatisierung/Markdeep/markdeep.min.js"
CSSPfad = "G:/Projekte/GOB/02_Teilprojekte/06_Test/Testautomatisierung/Markdeep/Style.css"
MarkDeepHeader = "<meta lang=\"de\" charset=\"utf-8\" emacsmode=\"-*- markdown -*-\">" + "<link rel=\"stylesheet\" href=\"file:/" + CSSPfad + "?\">\n"
MarkDeepFooter = "\n<!-- Markdeep: --><style class=\"fallback\">body{visibility:hidden}</style><script src=\"file:/" + MarkDeepPfad + "?\" charset=\"utf-8\"></script>"

# Test dauer
startzeit = ""
endezeit = ""

### Overview Variablen
LogOverviewFilePath = ""



# Bestimmt dem Umfangdes Loggings
# 2 = vollständig
# 1 = minimal
# 0 = aus
loglvl = 2

###### Logging
###### Schreibt die aktuelle Systemzeit in das Logfile#
def zeit_loggen(is_overview = False):
    if loglvl == 0:
        return
    logstring = "<div class = \"TimeStamp\" > (" + datetime.datetime.now().strftime("%d.%m.%Y - %H:%M:%S") + ") </div>\n"
    if is_overview == False:
        append_file(logstring)
    else:
        append_overview_file(logstring)


###### Legt ein Loggingfile für den gesamten Testlauf an dem Pfad "LogOverviewFilePath" an und erzeugt den Header des Markdeepfiles
###### in der Overview werden tabellarisch die Ergebnisse pro Testlauf dokumentiert
def logfile_overview_anlegen(ParentFolder, FileName, single_file_only):
    global LogOverviewFilePath
    LogOverviewFilePath = ParentFolder + FileName
    global LogOverviewFileParentFolder
    LogOverviewFileParentFolder = ParentFolder
    if not path.exists(LogOverviewFileParentFolder):
        os.makedirs(LogOverviewFileParentFolder)
    if single_file_only == False:
        count = 1
        single_file_temp_overview = LogOverviewFilePath
        if path.exists(single_file_temp_overview):
            while True:
                single_file_temp_overview = LogOverviewFilePath.replace(".md.", "_(" + str(count) + ").md.")
                if path.exists(single_file_temp_overview):
                    count += 1
                else:
                    break
            LogOverviewFilePath = single_file_temp_overview
    try:
        file = open(LogOverviewFilePath, "w+")
        file.close()
    except:
        print("Fehler beim erstellen der Übersichts-Datei")
    append_overview_file (MarkDeepHeader)
    append_overview_file("<div class = \"Title\" > " + u"Testlaufdurchführung-Übersicht" + " </div>\n")
    append_overview_file("<div class = \"Subtitle\" > " + "Dies ist eine automatisiert generierte Testdurchführungsübersicht. Diese Übersicht wird mit jeder Ausführung überschrieben" + " </div>\n")
    ueberschrift_anlegen(1, "Übersicht zum Testlauf (" + datetime.datetime.now().strftime("%d.%m.%Y - %H:%M:%S") + ")", True)

###### Schreibt eine übergebenen Tabelle in das Overview-Logfiles
def overview_abschluss_tabelle_anlegen(Liste):
    if loglvl == 0:
        return
    i = 0
    while i < len(Liste):
        splitted = Liste[i].split(",")
        if i == 0:
            j = 0
            string = ""
            while j < len(splitted):
                if j == 0:
                    string = "\n" + " | " + splitted[j] + " |"
                else:
                    string = string + " " + splitted[j] + " |"
                j += 1
            append_overview_file (string)
            j = 0
            string = ""
            while j < len(splitted):
                if j == 0:
                    string = " | " + "---" + " |"
                else:
                    string = string + " " + "---" + " |"
                j += 1
            append_overview_file (string)
        else:
            j = 0
            string = ""
            while j < len(splitted):
                if j == 0:
                    string = " | " + splitted[j] + " |"
                else:
                    string = string + " " + splitted[j] + " |"
                j += 1
            append_overview_file (string)
        i += 1

###### Schreibt eine übergebenen Tabelle in das Overview-Logfile, formatiert diese und sammelt Daten über die Ausführung
def overview_tabelle_anlegen(Liste):
    anzahl_gesamt = 0
    anzahl_erfolgreich = 0
    anzahl_fehlerhaft = 0
    if loglvl == 0:
        return
    i = 0
    while i < len(Liste):
        splitted = Liste[i].split(",")
        #Titelleiste der Tabelle
        if i == 0:
            j = 0
            string = ""
            while j < len(splitted):
                if j == 0:
                    string = "\n" + " | " + splitted[j] + " |"
                else:
                    # Wenn der Titel "Erfolgreich" enthält wird die Schriftfarbe auf Grün gesetzt
                    if "erfolgreich" in str(splitted[j]).lower():
                        string = string + "<font color=\"green\">" + splitted[j] + "</font> |"
                    # Wenn der Titel "Fehlerhaft" enthält wird die Schriftfarbe auf Rot gesetzt
                    elif "fehlerhaft" in str(splitted[j]).lower():
                        string = string + "<font color=\"red\">" + splitted[j] + "</font> |"
                    else:
                        string = string + " " + splitted[j] + " |"
                j += 1
            append_overview_file (string)
            j = 0
            string = ""
            while j < len(splitted):
                if j == 0:
                    string = " | " + "---" + " |"
                else:
                    string = string + " " + "---" + " |"
                j += 1
            append_overview_file (string)
        #weitere Zeilen der Tabelle
        else:
            j = 0
            string = ""
            while j < len(splitted):
                anzahl_in_testfall = 0
                zusatz_prozente = ""
                if j == 0:
                    string = " | " + splitted[j] + " |"
                else:
                    # Spalte 1 "Testfall-Ordner"
                    if j == 1:
                        # Markdeep-Link zum Ablagepfad erzeugen
                        string = string + " [" + "Ordner öffnen" + "](\"file://" + splitted[j] + "\") |"
                    # Spalte 1 "Akzeptanzkriterium"
                    if j == 2:
                        string = string +  splitted[j] + " |"
                    # Spalte 3 "Gesamt"
                    if j == 3:
                        anzahl_in_testfall = int(splitted[j])
                        # Gesamtanzahl der Testfälle Zählen
                        anzahl_gesamt = anzahl_gesamt + anzahl_in_testfall
                        string = string + " " + splitted[j] + " |"
                    # Spalte 4 "Erfolgreich"
                    if j == 4:
                        anzahl_in_testfall_erf = int(splitted[j])
                        # Gesamtanzahl der erfolgreichen Testfälle Zählen
                        anzahl_erfolgreich = anzahl_erfolgreich + anzahl_in_testfall_erf
                        if anzahl_in_testfall != 0:
                            zusatz_prozente = " " + str(int(anzahl_in_testfall_erf / anzahl_in_testfall) * 100) + "% "
                        else:
                            zusatz_prozente = ""
                        string = string + " " + splitted[j] + zusatz_prozente + " |"
                    # Spalte 5 "Fehlerhaft"
                    if j == 5:
                        anzahl_in_testfall_fehl = int(splitted[j])
                        # Gesamtanzahl der fehlerhaften Testfälle Zählen
                        anzahl_fehlerhaft = anzahl_fehlerhaft + anzahl_in_testfall_fehl
                        if anzahl_in_testfall != 0:
                            zusatz_prozente = " " + str(int(anzahl_in_testfall_fehl / anzahl_in_testfall) * 100) + "% "
                        else:
                            zusatz_prozente = ""
                        string = string + " " + splitted[j] + zusatz_prozente + " |"
                j += 1
            append_overview_file (string)
        i += 1
    return anzahl_erfolgreich, anzahl_fehlerhaft, anzahl_gesamt

###### Schließt das Log-File für die Übersicht ab und erzeugt eine Tabelle mit einer Übersicht über die ausgeführten Testfälle
def logfile_overview_abschließen(test_overview):
    anzahl_erfolgreich, anzahl_fehlerhaft, anzahl_gesamt = overview_tabelle_anlegen(test_overview)
    #### Übersicht über die durchgeführten Tests erzeugen
    ueberschrift_anlegen(1, "Testlauf Gesamt-Ergebnis", True)
    table = []
    table.append("Beschreibung,Anzahl,Prozent")
    table.append("Gesamt," + str(anzahl_gesamt) + ",-")
    if anzahl_gesamt > 0:
        table.append("<font weight=\"bold\" color=\"green\"> Erfolgreich </font>," + str(anzahl_erfolgreich) + "," + str(int((anzahl_erfolgreich/anzahl_gesamt)*100)) + "%")
        table.append("<font weight=\"bold\" color=\"red\"> Fehlerhaft </font>," + str(anzahl_fehlerhaft) + "," + str(int((anzahl_fehlerhaft/anzahl_gesamt)*100)) + "%")
    overview_abschluss_tabelle_anlegen(table)
    append_overview_file("\n" + MarkDeepFooter)

###### Legt ein Loggingfile an dem Pfad "LogFilePath" an und erzeugt den Header des Markdeepfiles
def logfile_anlegen(ParentFolder, FileName, loglevel = 1):
    global loglvl
    loglvl = int(loglevel)
    if loglvl == 0:
        return
    global startzeit
    startzeit = datetime.datetime.now() #.strftime("%d.%m.%Y - %H:%M:%S")
    global LogFilePath
    LogFilePath = ParentFolder + FileName
    global LogFileParentFolder
    LogFileParentFolder = ParentFolder
    try:
        file = open(LogFilePath, "w+")
        file.close()
    except:
        print("Fehler beim erstellen der Log-Datei")
    append_file (MarkDeepHeader)
    append_file("<div class = \"Title\" > " + u"Testlaufdurchführungs-Log" + " </div>\n")
    append_file("<div class = \"Subtitle\" > " + "Dies ist ein automatisiert generiertes Log" + " </div>\n")


###### Dokumenten Header anlegen ########
def dokumenten_header_anlegen(tablemeta, tablesteps, isgevo = False):
    if loglvl == 0:
        return
    if isgevo == False:
        ueberschrift_anlegen(1, "Test Informationen")
        tabelle_anlegen(tablemeta)
        ueberschrift_anlegen(1, "Test Ablauf")
        fliesstext_eintrag("Innerhalb des Testcases werden die folgenden Schritte durchgeführt.")
        tabelle_anlegen(tablesteps)
        ueberschrift_anlegen(1, "Testfall")
        notiz_anlegen("Testfall Ablauf wird nun gestartet")
        ueberschrift_anlegen(2, "Testfall Ablauf wird vorbereitet")
    else:
        ueberschrift_anlegen(2, "GeVo Informationen")
        tabelle_anlegen(tablemeta)
        ueberschrift_anlegen(2, "GeVo Ablauf")
        fliesstext_eintrag("Innerhalb des GeVos werden die folgenden Schritte durchgeführt.")
        tabelle_anlegen(tablesteps)
        ueberschrift_anlegen(2, "GeVo")
        notiz_anlegen("GeVo Ablauf wird nun gestartet")
        ueberschrift_anlegen(3, "GeVo Ablauf wird vorbereitet")

###### Bei einer Ersetzung von Testdaten Identifikator mit einem Testdatum wird ein Log Eintrag erzeugt
def testdaten_ersetzung(par_alt, parameter, type):
    if loglvl == 0:
        return
    table = []
    if type == "testdaten":
        fliesstext_eintrag("Der Testfall Indikator aus der Testablauf-Datei wurde durch ein Testdatum aus der Testdaten-Datei ersetzt")
    elif type == "variablen":
        fliesstext_eintrag("Der Variablen Indikator aus der Testablauf-Datei wurde durch den gespeicherten Variablenwert ersetzt")
    table.append("Parameter Identifikator,Testdatum")
    table.append(str(par_alt) + "," + str(parameter))
    tabelle_anlegen(table)

##### Bereitet den übergebenen String für die AUsgabe der Tasks auf
def task_aufbereiten(ausgabestring):
    if loglvl == 0:
        return
    ausgabe = str(ausgabestring).replace("\\r\\n", "\n")
    ausgabe = str(ausgabe).replace("b'", "")
    ausgabe = str(ausgabe).replace("\n'", "")
    ausgabe = str(ausgabe).replace("b'", "")
    return ausgabe
###### Log Einträge zu TASKKILL anlegen
def log_taskkill(command_1, ausgabe_1, ausgabe_err_1, command_2, ausgabe_2, ausgabe_err_2):
    if loglvl == 0:
        return
    ### bereinigen und aufbereiten der Ausgabe
    ausgabe_1 = task_aufbereiten(ausgabe_1)
    ausgabe_2 = task_aufbereiten(ausgabe_2)
    ausgabe_err_1 = task_aufbereiten(ausgabe_err_1)
    ausgabe_err_2 = task_aufbereiten(ausgabe_err_2)

    ### Ausgabe in Log
    ueberschrift_anlegen(3, "Bestehende Prozesse entfernen")
    fliesstext_eintrag("Bereits bestehende Prozesse werden mittels der folgenden Befehle vor Erzeugung einer neuen Webdriver-Instanz entfernt.")
    notiz_anlegen("Hier können Fehler angezeigt werden. Diese haben jedoch keinen unmittelbaren Einfluss auf den Testablauf. Das Kommando \"TASKKILL\" erzeugt eine Fehlerausgabe, sobald der gewünschte Prozesse nicht vorhanden ist")
    ueberschrift_anlegen(4, "Webdriver")
    fliesstext_eintrag("Der folgende Befehl wurde ausgeführt.")
    code_anlegen("", command_1, 0)
    fliesstext_eintrag("Der Befehl erzeugte folgende Ausgabe.")
    if ausgabe_1 == "'":
        code_anlegen("", "Es wurden keine Ausgabe erzeugt.", 0)
    else:
        code_anlegen("", ausgabe_1, 1)
    fliesstext_eintrag("Der Befehl erzeugte folgende Fehler.")
    if ausgabe_err_1 == "'":
        code_anlegen("", "Es wurden keine Fehler erzeugt.", 0)
    else:
        code_anlegen("", ausgabe_err_1, 1)
    ueberschrift_anlegen(4, "Browser")
    fliesstext_eintrag("Der folgende Befehl wurde ausgeführt.")
    code_anlegen("", command_2, 0)
    fliesstext_eintrag("Der Befehl erzeugte folgende Ausgabe.")
    if ausgabe_2 == "'":
        code_anlegen("", "Es wurden keine Ausgabe erzeugt.", 0)
    else:
        code_anlegen("", ausgabe_2, 1)
    fliesstext_eintrag("Der Befehl erzeugte folgende Fehler.")
    if ausgabe_err_2 == "'":
        code_anlegen("", "Es wurden keine Fehler erzeugt.", 0)
    else:
        code_anlegen("", ausgabe_err_2, 1)


###### Schreibt das ende des LogFiles
def logfile_abschliessen():
    if loglvl == 0:
        return
    testdauer_berechnen()
    append_file("\n" + MarkDeepFooter)

def testabschluss_pruefen():
    if loglvl == 0:
        return
    file_abgeschlossen = 0
    ## Wenn die Log-Datei bereits die Footer-Zeile enthält wurde die Datei bereits abgeschlossen
    try:
        if open(LogFilePath, 'r').read().find(MarkDeepFooter) >= 0:
            file_abgeschlossen = 1
    except:
        print("Fehler beim Lesen der Log-Datei")
    return file_abgeschlossen



def log_webdriver(driver, browser, binary_pfad, webdriver_pfad):
    if loglvl == 0:
        return
    table = []
    browser_norm = ""
    table.append("Beschreibung,Wert")
    if browser == "ch" or browser == "chrome":
        browser_norm = "Chrome"
    elif browser == "ff" or browser == "firefox":
        browser_norm = "Firefox"
    ueberschrift_anlegen(2,"Webdriver erzeugen")
    fliesstext_eintrag("Der Webdriver wurde angelegt. Die Testdurchführung wird mit " + browser_norm + " und folgenden Eigenschaften durchgeführt.")
    table.append("Browser,"+browser_norm)

    table.append("Browser-Version," + driver.capabilities['browserVersion'])
    table.append("Broswer-EXE," + binary_pfad)

    table.append("Webdriver-Version," + "to be done")
    table.append("Webdriver-EXE," + webdriver_pfad)
    tabelle_anlegen(table)

###### Testdauer berechnen
def testdauer_berechnen():
    if loglvl == 0:
        return
    endezeit = datetime.datetime.now()
    testdauer = endezeit - startzeit
    table = []
    table.append("Beschreibung,Wert")
    ausgabestring = ""
    testdauer_in_sekunden = testdauer.seconds
    if int(testdauer_in_sekunden/60) > 0:
        int_min = int(testdauer_in_sekunden/60)
        testdauer_in_sekunden = testdauer_in_sekunden - (int_min*60)
        ausgabestring = str(int_min) + " Minuten "

    ausgabestring = ausgabestring + str(testdauer_in_sekunden) + " Sekunden"

    table.append("Start Zeit,"+ startzeit.strftime("%d.%m.%Y - %H:%M:%S"))
    table.append("Ende Zeit,"+ endezeit.strftime("%d.%m.%Y - %H:%M:%S"))
    table.append("Testdauer(gerundet),"+ ausgabestring)
    fliesstext_eintrag("Der Testlauf wurde beendet. Im folgenden die Testabschlussinformationen sowie die Testdurchführungsdauer.")
    tabelle_anlegen(table)

###### Schreibt eine Überschrift mit der übergebenen Ebene in das LogFile
def ueberschrift_anlegen(Ebene, Eintrag, is_overview = False):
    if loglvl == 0:
        return
    header = ""
    if Ebene==1:
        header = "# "
    elif Ebene==2:
        header = "## "
    elif Ebene==3:
        header = "### "
    elif Ebene==4:
        header = "#### "
    elif Ebene==5:
        header = "##### "
    else:
        header = "# "
    if is_overview == True:
        append_overview_file("\n" + header + Eintrag)
        zeit_loggen(True)
    else:
        append_file("\n" + header + Eintrag)
        zeit_loggen()


###### Schreibt einen übergebenen Fließtext in das Logfiles
def fliesstext_eintrag(Eintrag):
    if loglvl == 0:
        return
    append_file("\n" + Eintrag)


###### Schreibt eine übergebenen Tabelle in das Logfiles
def tabelle_anlegen(Liste):
    if loglvl == 0:
        return
    i = 0
    while i < len(Liste):
        splitted = Liste[i].split(",")
        if i == 0:
            j = 0
            string = ""
            while j < len(splitted):
                if j == 0:
                    string = "\n" + " | " + splitted[j] + " |"
                else:
                    string = string + " " + splitted[j] + " |"
                j += 1
            append_file (string)
            j = 0
            string = ""
            while j < len(splitted):
                if j == 0:
                    string = " | " + "---" + " |"
                else:
                    string = string + " " + "---" + " |"
                j += 1
            append_file (string)
        else:
            j = 0
            string = ""
            while j < len(splitted):
                if j == 0:
                    string = " | " + splitted[j] + " |"
                else:
                    string = string + " " + splitted[j] + " |"
                j += 1
            append_file (string)
        i += 1
    # sofern nur eine Überschriftszeile übergeben wurde, wird eine leere Tabellenzeile ergänzt
    if i == 1:
        string = ""
        j = 0
        print(len(Liste[0].split(",")))
        while j < len(Liste[0].split(",")):
            if j == 0:
                string = " | " + " keine Werte " + " |"
            else:
                string = string + " " + " keine Werte " + " |"
            j += 1
        append_file (string)


###### Schreibt eine übergebene Liste in das Logfiles
def liste_anlegen(eintrag):
    if loglvl == 0:
        return
    append_file("* " + eintrag)


###### Schreibt einen übergebenen Code in das Logfiles
def code_anlegen(code, eintrag, linenumbers):
    if loglvl == 0:
        return
    if code == "":
        code = "Python"
    if linenumbers == 1:
        append_file("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ " + code + " linenumbers")
    elif linenumbers == 0:
        append_file("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ " + code)
    append_file(eintrag)
    append_file("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")


###### Formel in das Log-File schreiben
def formel_anlegen(string):
    append_file("\\begin{equation}")
    append_file(string)
    append_file("\\end{equation}")


###### Block Zitat in das Log-File schreiben
def block_zitat_anlegen(zitat, author = ""):
    append_file("> <span class=\"zitat\">")
    for i in range(len(zitat)):
        append_file("> " + zitat[i])
        if i < len(zitat)-1:
            append_file(">  <br>")
    append_file("> </span> <br> ")
    append_file("> <span class=\"author\">")
    append_file("> " + author)
    append_file("> </span>")



###### Schreibt einen Screenshot in das Logfiles
def screenshot_anlegen(driver):
    if loglvl == 0 or loglvl == 1:
        return
    count = 1

    screenshot_ordner_pfad = LogFileParentFolder+"Screenshots/"

    if not path.exists(screenshot_ordner_pfad):
        os.makedirs(screenshot_ordner_pfad)
    pfad = screenshot_ordner_pfad + str(count)+".png"
    while path.exists(pfad):
        count = count + 1
        pfad = screenshot_ordner_pfad + str(count)+".png"
    if driver is None:
        text = "Es konnte kein Screenschot für von dem Element erzeugt werden, da kein Webdriver vorhanden war."
        fehler_nachricht_anlegen("Fehler beim Screenshot erstellen", text)
        return
    driver.save_screenshot(pfad)
    text = "\n\n![Bild - Screenshots/"+str(count)+".png](Screenshots/"+str(count)+".png)"
    append_file(text)

####### Schreibt einen Screenshot des elements in das Logfile
def screenshot_von_element_anlegen(element):
    if loglvl == 0 or loglvl == 1:
        return
    count = 1
    element_ordner_pfad = LogFileParentFolder+"Screenshots/Elements/"
    if not path.exists(element_ordner_pfad):
        os.makedirs(element_ordner_pfad)
    pfad = element_ordner_pfad + str(count)+"_e.png"
    while path.exists(pfad):
        count = count + 1
        pfad = element_ordner_pfad + str(count)+"_e.png"
    if element is None:
        text = "\nEs konnte kein Screenschot für von dem Element erzeugt werden, da das Element leer war"
        append_file(text)
        return
    try:
        element.screenshot(pfad)
        text = "\n\n![Bild von selektiertem Element - Screenshots/Elements/"+str(count)+"_e.png](Screenshots/Elements/"+str(count)+"_e.png)"
        append_file(text)
    except:
        text = "\nFehler beim erzeugen des Screenshots für das Element"
        append_file(text)

##### Schreibt eine Fehlermeldung in das Testfalldurchführungs-Log
##### Neue Zeilen werden durch das HTML-Tag "<br>" ersetzt, damit die Formatierung der Nachricht beibehalten wird
def fehler_nachricht_anlegen(bezeichnung, nachricht):
    if loglvl == 0:
        return
    # Zeilenumbrüche innerhalb des Strings werden mit HTML Tags für neue Zeilen ersetzt
    nachricht = nachricht.replace("\n","<br>")
    append_file("\n!!! ERROR:" + bezeichnung)
    append_file("    " + nachricht)


##### Schreibt eine Warnmeldung in das Testfalldurchführungs-Log
##### Neue Zeilen werden durch das HTML-Tag "<br>" ersetzt, damit die Formatierung der Nachricht beibehalten wird
def warnung_anlegen(nachricht):
    if loglvl == 0:
        return
    # Zeilenumbrüche innerhalb des Strings werden mit HTML Tags für neue Zeilen ersetzt
    nachricht = nachricht.replace("\n","<br>")
    append_file("\n!!! WARNING:Warnung")
    append_file("    " + nachricht)


##### Schreibt eine Notiz in das Testfalldurchführungs-Log
##### Neue Zeilen werden durch das HTML-Tag "<br>" ersetzt, damit die Formatierung der Nachricht beibehalten wird
def notiz_anlegen(nachricht):
    if loglvl == 0 or loglvl == 1:
        return
    # Zeilenumbrüche innerhalb des Strings werden mit HTML Tags für neue Zeilen ersetzt
    nachricht = nachricht.replace("\n","<br>")
    append_file("\n!!! note:Hinweis")
    append_file("    " + nachricht)


##### Schreibt eine Erfolgsmeldung in das Testfalldurchführungs-Log
##### Neue Zeilen werden durch das HTML-Tag "<br>" ersetzt, damit die Formatierung der Nachricht beibehalten wird
def erfolg_nachricht_anlegen(nachricht):
    if loglvl == 0:
        return
    # Zeilenumbrüche innerhalb des Strings werden mit HTML Tags für neue Zeilen ersetzt
    nachricht = nachricht.replace("\n","<br>")
    append_file("\n!!! Tip:Erfolgreich")
    append_file("    " + nachricht)

####### zum Loggen von erhaltenen Exception Meldungen #######
def exception_log(funktion, fehlermeldung):
    ### Ersetzung, damit die Markdeep Formatierung bestehen bleibt
    if len(fehlermeldung) <= 10:
        #fehlermeldung = "Message: Es wurde keine Exceptionmeldung zurückgegeben"
        fehlermeldung = fehlermeldung
    # Zeilenumbrüche innerhalb des Strings werden mit HTML Tags für neue Zeilen ersetzt
    fehlermeldung = fehlermeldung.replace("\n","<br>")
    ueberschrift_anlegen(3,"Fehler in Funktion")
    fliesstext_eintrag("In der Funktion **" + funktion + "** ist ein Fehler aufgetreten. Die folgende Fehlermeldung wurde erzeugt")
    fehler_nachricht_anlegen("Exception", fehlermeldung)

####### zum Loggen von einem übergebenen Element #######
def log_element(element):
    list_of_attributes = []
    list_of_attributes.append("Wert,value")
    list_of_attributes.append("Titel,title")
    list_of_attributes.append("Aria,aria")
    list_of_attributes.append("Klasse,class")
    list_of_attributes.append("Typ,type")
    list_of_attributes.append("ID, id")
    fliesstext_eintrag("Zu dem übergebenen Element wurden die folgenden Attribute ermittelt.")
    if element is not None:
        table = []
        table.append("Attribut,Wert")
        # Position des Elements
        try:
            table.append("Position," + "x:" + str(element.location["x"]) + "<br>y:" + str(element.location["y"]))
        except:
            table.append("Position," + "Attr. nicht vorhanden")

        # Tag Name des Elements
        try:
            table.append("Tag Name," + element.tag_name)
        except:
            table.append("Tag Name," + "Attr. nicht vorhanden")
        # Text des Elements
        try:
            table.append("Text," + element.text)
        except:
            table.append("Text," + "Attr. nicht vorhanden")
        ### Liste von vorab definierten Attributen ausgeben
        for x in range(len(list_of_attributes)):
            werte = str(list_of_attributes[x]).split(",")
            try:
                table.append(werte[0] + "," + str(element.get_attribute(werte[1])))
            except:
                table.append("Wert," + "Attr. nicht vorhanden")
        # Wird das Element aktuell angezeigt?
        try:
            table.append("Wird angezeigt?," + str(element.is_displayed()))
        except:
            table.append("Wird angezeigt?," + "Attr. nicht vorhanden")
        # Ist das Element aktuell aktiviert
        try:
            table.append("Aktiviert?," + str(element.is_enabled()))
        except:
            table.append("Aktiviert?," + "Attr. nicht vorhanden")
        # Ist das aktuelle Elemente selektiert (primär für den Status von Checkboxen nützlich)
        try:
            table.append("Selektiert?," + str(element.is_selected()))
        except:
            table.append("Selektiert?," + "Attr. nicht vorhanden")
        tabelle_anlegen(table)
    else:
        warnung_anlegen("Zu dem übergebenen Element konnten keine Informationen ermittelt werden. Das Element war leer.")
############### Ergänzt einen übergebenen String im LogFile zur Testfalldurchführung
def append_file(line):
    if loglvl == 0:
        return
    try:
        with open(LogFilePath, "a", encoding="UTF-8") as myfile:
            # \n damit nach jeder übergebenen Zeile ein Umbruch eingefügt wird
            myfile.write(line + "\n")
        # Schließt die Datei nach dem einfügen der Zeile
        myfile.close()
    except:
        print("Fehler beim Schreiben in das Log-File")


############### Ergänzt einen übergebenen String im LogFile zur Übersicht
def append_overview_file(line):
    try:
        with open(LogOverviewFilePath, "a", encoding="UTF-8") as myfile:
            # \n damit nach jeder übergebenen Zeile ein Umbruch eingefügt wird
            myfile.write(line + "\n")
        # Schließt die Datei nach dem einfügen der Zeile
        myfile.close()
    except:
        print("Fehler beim Schreiben in das Log-File")
###############
