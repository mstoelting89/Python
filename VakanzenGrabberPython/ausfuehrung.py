import VakanzenGrabber
import datentreiber
##############################################################################################################################################
#
#   Aufrufen der Funktion VarkanzenGrabben
#
##############################################################################################################################################

##################################################
# Laden der Excel-Datei Datentreiber, um die
# Daten zu ziehen
##################################################
data = datentreiber.datentreiber("Data/Datentreiber.xlsx")

##################################################
# Durchlaufen der Seiten mit den Daten aus dem
# Datentreiber
##################################################
for i in range(0,len(data.excelOeffnen(0))):

    ###################################
    # Instanzierung der Klasse
    ###################################                 URL                             SUCHBEGRIFF                 SEITENTITEL
    vakanzenGrabben = VakanzenGrabber.VakanzenGrabber(str(data.excelOeffnen(0)[i]), str(data.excelOeffnen(1)[i]), str(data.excelOeffnen(2)[i]))

    ###################################
    # Wenn die Hauptseite erfolgreich
    # aufgerufen wurde, wird die
    # Methode naechste_seite ausgeführt
    ###################################
    if vakanzenGrabben.vakanzenGrabbenHauptseite() == True:
        vakanzenGrabben.naechste_seite()

