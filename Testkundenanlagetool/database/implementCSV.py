#####################################################################
#
# Klasse zum Laden der Daten aus einer csv datei
#
#####################################################################
import numpy as np
import pandas as pd



class implementCSV():
    ############################################################
    # Constructor zum Laden der Übergebenen CSV
    ############################################################
    def __init__(self,filename):
        data = pd.read_csv(filename)
        print(data)

csv_lesen = implementCSV('Personenarten.csv')
