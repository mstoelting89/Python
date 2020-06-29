##############################################################################################################################################
#
#   Klasse zum Speichern der Daten in einer Log Datei
#
##############################################################################################################################################
import datetime

class logData():

    def __init__(self,name):
        self.name = name
        self.file = open(name+".txt","w")

    def logSchreiben(self,value):
        timestamp = str(datetime.datetime.now())
        self.file.write(timestamp + ": " + value)
        self.file.write("\n")

    def close(self):
        self.file.close()
