groesse = input("Bitte gebe deine Körpergröße in m an: ")
gewicht = input("Bitte gebe dein Gewicht in kg an: ")

bmi = float(gewicht) / (float(groesse)*float(groesse))

print("Dein BMI lautet: " + str(bmi))
