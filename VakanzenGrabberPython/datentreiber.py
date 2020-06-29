##############################################################################################################################################
#
#   Klasse zum Laden der Daten aus einem Datentreiber
#
##############################################################################################################################################
import pandas as pd
import xlrd
import numpy as np

class datentreiber():

    ###################################
    # Übergabe des Dateipfades
    ###################################
    def __init__(self,path):
        self.path = path

    ###################################
    # Datei wird geöffnet und die Daten
    # aus der übergebenen Spalte werden
    # in ein Array gespeichert
    ###################################
    def excelOeffnen(self,spalte):
        book = xlrd.open_workbook(self.path, encoding_override="utf-8")
        sheet = book.sheet_by_index(0)

        data = []
        for i in range(1, sheet.nrows):
            data.append(sheet.cell(i, int(spalte)).value)

        return data


