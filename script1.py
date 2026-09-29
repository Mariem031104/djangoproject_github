pays_visites = [
    "Tunisie",
    "France",
    "Italie",
    "Tunisie",
    "France",
    "Tunisie",
    "Espagne",
    "Italie"
]

# Compter le nombre de visites par pays
visites = {}

for pays in pays_visites:
    if pays in visites:
        visites[pays] += 1
    else:
        visites[pays] = 1

print("Nombre de visites par pays :", visites)

# Pays le plus visité
pays_plus_visite = max(visites, key=visites.get)

print("Le pays le plus visité est :", pays_plus_visite)