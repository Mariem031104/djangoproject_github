produit = "clavier"
prix = 150.5
stock = 20
print (produit);
print (prix);
print (stock);
print(f"Produit est {produit} et prix est {prix} " )
print(f"Produit est {produit} et prix avec remise {prix * (1-0.2) } euros " )

prix_ttc = [150.5, 200.0, 300.0,400.0,500.0]
prix_ht= []
for prix in prix_ttc:
    prix_ht.append(round(prix / 1.9, 3))

print(prix_ht)
prix_ht_1 = (round(prix / 1.9, 3) for prix in prix_ttc)
print(prix_ht_1)

prix_ht_1 = [round(prix / 1.9, 3) for prix in prix_ttc if prix > 150]
print(prix_ht_1)

articles = ["clavier" , "souris" ,"ecran"]

catalogue = {
    article: prix for article, prix in zip(articles, prix_ttc)
}
#print (catalogue)

def calcul(prix, tva):
    return round(prix / (1 + tva), 3)

def calculer(prix, tva=0.19):
    return round(prix / (1 + tva), 3)

print(calculer(150.5))

def facturer(client,*lignes):
    total = sum(lignes)
    return(total)

print (facturer("Dupont",150.5,200.0,300.0))

class Livre:
    def __init__(self,titre,auteur,prix):
        self.titre = titre
        self.auteur = auteur
        self .prix= prix

    def __str__(self):
        return f"{self.titre} par {self.auteur} , prix : {self.prix} euros "
        
    def afficher(self):
        return f"{self.titre} par {self.auteur} , prix : {self.prix} euros "

    def __eq__(self, value):
        return self.titre == other.titre and self.auteur == other.auteur and self.prix == other.prix
        
l1= Livre("Le petit prince", "antonie", 15.5)
print (l1.afficher())
print (l1)


l3 = l1
print (l3)
print (l1 = l3)
