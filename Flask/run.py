from flask import Flask, render_template, request

print(__name__)
app = Flask(__name__)

class Item():
    def __init__(self,name, amount):
        self.name = name
        self.amount = amount

class neuerEintrag():
    def __init__(self,waehrung,groesse):
        self.waehrung = waehrung
        self.groesse = groesse

@app.route('/')
def hello_world():
    items = [
        Item("Apfel",5),
        Item("Birne",3),
        Item("Computer",2)
    ]

    weitereItems = [
        {"name": "Apfel", "amount": 5},
        {"name": "Birne", "amount": 3},
        {"name": "Computer", "amount": 2},
    ]
    return render_template("start.html", name="Max Mustermann", items=weitereItems)

@app.route("/test")
def test():
    args = request.args
    print(args.get("name"))
    name = args.get("name")
    return render_template("test.html", name=name)

@app.route("/currency")
def currency():
    args = request.args
    waehrung = float(args.get("waehrung"))
    d = {}

    if waehrung != None or waehrung == "":

        schritte = int(args.get("schritte")) + 1

        for i in range(1,int(schritte)):

            berechneteWaehrung = i * waehrung

            d[i] = berechneteWaehrung

        print(d)
    else:
        print("Nix vorhanden")

    return render_template("currency.html", waehrung=waehrung, waehrungsListe=d)
