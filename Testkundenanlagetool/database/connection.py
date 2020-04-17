####################################################################
#Verbindung zur Datenbank wird hergestellt
#####################################################################
import pyodbc

conn = pyodbc.connect(
            r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};'
            r'DBQ=C:\Users\mstoelting\Documents\Programmierung\Python\Testkundenanlagetool\database\testDatenbank.accdb;')

#class DatabaseConnection():

#    def __init__(self):
#        conn = pyodbc.connect(
#            r'Driver={Microsoft Access Driver (*.mbd, *.accdb)};'
#            r'DBQ=testDatenbank.accdb;')