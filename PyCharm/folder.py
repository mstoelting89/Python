import os

print(__file__)
print(os.path.dirname(__file__))
pfad = os.path.dirname(__file__)

with open(pfad + "/datei.txt", "r") as file:
    for line in file:
        print(line)

print(os.listdir("."))

