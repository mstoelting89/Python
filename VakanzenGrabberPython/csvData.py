##############################################################################################################################################
#
#   Klasse zum Speichern der Daten in einer CSV Datei
#
##############################################################################################################################################

import csv

class CSV_Daten():

    def __init__(self,name):
        self.name = name
        self.file = open(name + ".csv", "a")

    def csvSchreiben(self,value):
        writer = csv.writer(self.file, lineterminator='\n', delimiter=';')
        writer.writerow(value)

    def csvClose(self):
        self.file.close()



