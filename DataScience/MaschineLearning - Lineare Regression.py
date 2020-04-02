import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

df = pd.read_csv("../Kursmaterialien/data/names.csv")

#print(df.head())

df1 = df[df["Name"] == "Anna"]
df2 = df1[df1["Gender"] == "F"]
df3 = df2[df2["State"] == "CA"]

#print(df3)

count = df3["Count"]
year = df3["Year"]

countL = []
yearL = []

for x in count:
    countL.append([x])

for x in year:
    yearL.append([x])

plt.plot(year,count)


model = LinearRegression()
model.fit(yearL,countL)

predicted = model.predict(yearL)

plt.plot(year,predicted)
plt.show()