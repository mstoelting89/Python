import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("../Kursmaterialien/data/names.csv")

#print(df.head())

df1 = df[df["Name"] == "Anna"]
df2 = df1[df1["Gender"] == "F"]
df3 = df2[df2["State"] == "CA"]

#print(df3)

count = df3["Count"]
year = df3["Year"]

#print(count)

plt.plot(year,count)
plt.show()