####################################################################
# Diese Datei erstellt die Benutzeroberflaeche fuer das
# Testkundenanlagetool
####################################################################

###########################
# zu erledigende Importe
###########################
import tkinter
from tkinter import ttk

###########################
# Funktionen
# 1. ende()
###########################

#Funktion zum Beenden des Fensters
def ende():
    main.destroy()

###########################
# Erstellen des Fensters
###########################

#Hauptfenster wird initialisiert
main = tkinter.Tk()
main.geometry('600x400')

#Elemente werden hinzugefügt
ueberschrift_hauptfenster = tkinter.Label(main, text = "Testkundenanlagetool")
ueberschrift_hauptfenster.grid(row = 0, column = 0, pady = 20, columnspan = 5)

zweite_ueberschrift_hauptfenster = tkinter.Label(main, text = "Eingabedaten")
zweite_ueberschrift_hauptfenster.grid(row = 1, column = 0)


labelInstitut = tkinter.Label(main, text = "Institut")
labelInstitut.grid(row = 2, column = 0, pady = 10)

comboBox_Institut = ttk.Combobox(main, values = ["421", "310", "307"])
comboBox_Institut.grid(row = 2, column = 1, pady = 10)


labelAnzahl = tkinter.Label(main, text = "Anzahl")
labelAnzahl.grid(row = 3, column = 0, pady = 10)

textfeld_Anzahl = tkinter.Entry()
textfeld_Anzahl.grid(row = 3, column = 1, pady = 10)


label_personenart = tkinter.Label(main, text = "Personenart")
label_personenart.grid(row = 4, column = 0, pady = 10)

comboBox_personenart = ttk.Combobox(main, values = ["P-Person", "J-Person", "N-Person"])
comboBox_personenart.grid(row = 4, column = 1, pady = 10)

label_personenart = tkinter.Label(main, text = "Personendaten")
label_personenart.grid(row = 4, column = 3, pady = 10)

comboBox_personenart = ttk.Combobox(main, values = ["Wohnanschrift", "Telefonnummer", "E-Mail-Adresse"])
comboBox_personenart.grid(row = 4, column = 4, pady = 10)


label_personenart = tkinter.Label(main, text = "Konten")
label_personenart.grid(row = 5, column = 0)

comboBox_personenart = ttk.Combobox(main, values = ["Girokonten", "Festgeld", "S-Flex"])
comboBox_personenart.grid(row = 5, column = 1)

label_personenart = tkinter.Label(main, text = "Zusatzprodukte")
label_personenart.grid(row = 5, column = 3)

comboBox_personenart = ttk.Combobox(main, values = ["Dauerauftrag", "Dispo", "SparkassenCard"])
comboBox_personenart.grid(row = 5, column = 4)


checkBox_Daten = ttk.Checkbutton(main, text = "Alle Daten anzeigen")
checkBox_Daten.grid(row = 6, column = 1, pady = 10)


bKonvertieren = tkinter.Button(main, text = "Konvertieren")
bKonvertieren.grid(row = 7, column = 0, pady = 10)

bLoeschen = tkinter.Button(main, text = "Daten löschen")
bLoeschen.grid(row = 7, column = 1, pady = 10)

bEnde = tkinter.Button(main, text = "Beenden", command = ende)
bEnde.grid(row = 7, column = 2, pady = 10)


#Initialisieren der Oberflaeche
main.mainloop()