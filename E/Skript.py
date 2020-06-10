import datetime
import pytest
import Classes.gui_automation
import Classes.Logging
import sys
import os
import csv
import atexit
##### Am Ende jeden Testfalls wird diese Funktion ausgeführt
##### Dieser Aufruf über "atexit" dient ausschließlich dazu, dass im Fehlerfall
##### der Testabschluss in jedem Fall durchgeführt wird.
atexit.register(Classes.gui_automation.test_abschliessen)

class Basic_Test:
	pass
class Test_URL(Basic_Test):
	def test_runner(self, config_param):
		Classes.gui_automation.read_config()
		# Liste mit Dateien die Testabläufe enthalten
		# ";"-separiert
		testliste = config_param["tests"].strip().split(";")
		# Für den Test zu verwendender Browser
		# 	Chrome 				- chrome
		#	Firefox 			- ff
		# 	Internet Explorer 	- ie
		browser = config_param["browser"].lower()
		# Headless-Modus
		# 	1	- Ja
		# 	0 	- Nein
		headless = config_param["headless"]
		# Zielordner für die Ablage der Ergebnisse der Testdurchführung
		zielordner = config_param["zielordner"]
		# Zielordner für die Ablage der Ergebnisse der Testdurchführung
		loglevel = config_param["loglvl"]
		# Zieladresse für den Beginn der Testdurchführung - Diese Seite wird beim erzeugen des Webdrivers aufgerufen
		url = config_param["url"]
		# Ordner zum bilden der Testliste
		testfall_ordner = config_param["folder"]
		# Ordner zum bilden der Testliste
		unterordner = True
		# Testlisten-Datei
		testliste_datei = config_param["testliste"]
		if config_param["subfolder"] == "0":
			unterordner = False
		# Ordner zum bilden der Testliste
		jenkins_job_name = config_param["jobname"]
		#
		#
		# Testliste erstellen auf Basis des testfall_ordners
		if testfall_ordner != "":
			testliste = Classes.gui_automation.testfallliste_erzeugen(testfall_ordner, unterordner)
			if testliste is None:
				pytest.fail("Fehler - Die Testliste konnte nicht erzeugt werden")
				return
		# Testliste erstellen auf Basis des übergebene Testfallliste erstellt
		if testliste_datei != "":
			testliste = Classes.gui_automation.testfallliste_aus_datei_erzeugen(testliste_datei)
			if testliste is None:
				pytest.fail("Fehler - Die Testliste konnte nicht erzeugt werden, da ein Fehler in der Testlisten-Datei ist."
							"Möglicher Fehler -> Testfalldatei aus der Liste ist nicht vorhanden")
				return

		# Prüfen welcher Browser übergeben wurde
		tempbrowser = browser.lower()
		if tempbrowser != "chrome" and tempbrowser != "ch" and tempbrowser != "firefox" and tempbrowser != "ff":
			pytest.fail("Fehler - Wählen Sie einen unterstützen Browser")
		if testliste == "":
			pytest.fail("Fehler - Übergebene Sie Testfälle zur Durchführung")
		#
		#
		# Testliste prüfen, ob alle Testabläufe auch physisch vorhanden sind
		testliste_fehlerhaft = False
		for i in range(len(testliste)):
			if not os.path.exists(testliste[i]):
				print("Testablauf wurde nicht gefunden - " + testliste[i])
				testliste_fehlerhaft = True
		if testliste_fehlerhaft:
			pytest.fail("Es wurden Fehler innerhalb der Testliste identifiziert. Testabläufe waren nicht vorhanden.")
			return
		results = Classes.gui_automation.testfaelle_ausfuehren(self, url, testliste, zielordner, browser, headless, loglevel, jenkins_job_name)
		#
		# Setzt ggf. den Lauf des Jobs auf Fehlerhaft, sobald mindestens eine Testfalldurchführung nicht erfolgreich war
		Classes.gui_automation.ausgabe_jenkins(results)


def main():
	print("")
if __name__=="__main__":
   main()