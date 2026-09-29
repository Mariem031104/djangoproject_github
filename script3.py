phrase = input("Entrez une phrase : ")

# a. Séparer la phrase en mots
mots = phrase.split()

# b. Afficher la liste avec str.format()
print("Liste des mots : {}".format(mots))

# c. Ajouter "incroyable"
mots.append("incroyable")

# d. Remplacer "puissant" par "facile"
if "puissant" in mots:
    position = mots.index("puissant")
    mots[position] = "facile"

# e. Afficher le nombre total de mots avec f-string
print(f"Nombre total de mots : {len(mots)}")

# f. Transformer la liste en phrase avec des tirets
nouvelle_phrase = "-".join(mots)

# g. Afficher avec str.format()
print("Nouvelle phrase : {}".format(nouvelle_phrase))

# h. Afficher chaque mot en majuscule
print("Mots en majuscule :")

for mot in mots:
    print("{}".format(mot.upper()))