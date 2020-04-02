import os

filename = os.path.join(os.path.dirname(__file__),"names")

files = os.listdir(filename)

print(files)
counter = 0
counterName = 0
searchName = "Max"
for file in files:
    filePath = os.path.join(os.path.dirname(__file__),"names", file)
    with open(filePath,"r", encoding="utf-8") as datei:
        for line in datei:
           l = line.strip().split(" ")

           firstname = l[0]

           if firstname == searchName:
               print(line)
               counterName = counterName + 1

print(counterName)
