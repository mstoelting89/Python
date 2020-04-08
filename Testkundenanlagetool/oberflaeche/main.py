####################################################################
# Diese Datei erstellt die Benutzeroberflaeche fuer das
# Testkundenanlagetool
####################################################################

###########################
# zu erledigende Importe
###########################
import tkinter

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
main.geometry('400x300')

ueberschrift_hauptfenster = tkinter.Label(main, text = "Testkundenanlagetool")
ueberschrift_hauptfenster.grid(row = 0, column = 0, pady = 20)

zweite_ueberschrift_hauptfenster = tkinter.Label(main, text = "Weiterer Text")
zweite_ueberschrift_hauptfenster.grid(row = 1, column = 1)

dritte_ueberschrift_hauptfenster = tkinter.Label(main, text = "dritter Weiterer Text")
dritte_ueberschrift_hauptfenster.grid(row = 1, column = 2)

vierte_ueberschrift_hauptfenster = tkinter.Label(main, text = "vierter Weiterer Text")
vierte_ueberschrift_hauptfenster.grid(row = 2, column = 1)

#Beenden - Button
bEnde = tkinter.Button(main, text = "Beenden", command = ende)
bEnde.grid(row = 4, column = 2)

#Initialisieren der Oberflaeche
main.mainloop()