#%matplotlib inline
import pandas as pd

import matplotlib.pyplot as plt


df = pd.read_excel("../Kursmaterialien/18 - DataScience - Stack/daten.xlsx")

print(df.head())

year = df["Jahr"]
sales = df["Umsatz"]

plt.plot(year,sales)
plt.show()