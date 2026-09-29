list=["France" ,"Espagne"  ,"Italie"]
visites = {}
for p in list:
    if p in visites:
        visites[p] += 1
    else:
        visites[p] = 1

print("Nombre de visites par pays :", visites)

pays_plus_visite = max(visites, key=visites.get)

print("Le pays le plus visité est :", pays_plus_visite)

purchases = [
    {“product”: “Computer”, ‘price’: 1200, “quantity”: 2},
    {“product”: “Mouse”, ‘price’: 25, “quantity”: 5},
    {“product”: “Keyboard”, ‘price’: 45, “quantity”: 3},
    {“product”: “Monitor”, ‘price’: 300, “quantity”: 2},
    {“product”: “Mouse”, ‘price’: 25, “quantity”: 2},
]
for price in purchases

