import pandas as pd

#siehe doku!

df = pd.read_csv("../Kursmaterialien/data/astronauts.csv")

#print(df.head())

#print(len(df))

#print(df["Name"])

entry = df.iloc[0]

print(entry["Name"])

#print(df.iloc[4:8])

ausgabe = df[df["Year"] < 1994]

df.sort_values("Name")
print(df["Name"])

