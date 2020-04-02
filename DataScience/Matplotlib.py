import matplotlib.pyplot as plt

#siehe Doku!!
plt.plot([1,2,3],[4,5,6],color="#ffff00", linestyle="dashed", marker="o", label="Umsatz")
plt.plot([1,2,3],[6,5,4],color="red", linestyle="dashed", label="Personen")
plt.legend()
plt.show()

#Kreisdiagramm erstellen

plt.pie([1,2,3])
plt.show()

#Balkendiagram

plt.bar([1,2,3],[4,5,6])
plt.show()

#Punktediagramm

plt.scatter([1,2,3],[4,5,6])
plt.show()