purchases = [
    {"product": "Computer", "price": 1200, "quantity": 2},
    {"product": "Mouse", "price": 25, "quantity": 5},
    {"product": "Keyboard", "price": 45, "quantity": 3},
    {"product": "Monitor", "price": 300, "quantity": 2},
    {"product": "Mouse", "price": 25, "quantity": 2}
]

# a. Montant total dépensé
total = 0

for achat in purchases:
    total += achat["price"] * achat["quantity"]

print("Montant total dépensé :", total)


# b. Nombre total acheté pour chaque produit
quantites = {}

for achat in purchases:
    produit = achat["product"]
    quantite = achat["quantity"]

    if produit in quantites:
        quantites[produit] += quantite
    else:
        quantites[produit] = quantite

print("Quantité par produit :", quantites)


# c. Produit le plus acheté
produit_plus_achete = max(quantites, key=quantites.get)

print("Produit le plus acheté :", produit_plus_achete)


# d. Valeur totale des ventes par produit
ventes = {}

for achat in purchases:
    produit = achat["product"]
    montant = achat["price"] * achat["quantity"]

    if produit in ventes:
        ventes[produit] += montant
    else:
        ventes[produit] = montant

print("Valeur totale des ventes :", ventes)