class Livre:
    def __init__(self, titre ,auteur ,annee, dispo=True):
          self.titre = titre
          self.titre = titre
          self.annee = annee
          self.dispo = dispo

    def emprunter(self):
     if self.dispo:
          self.dispo= False
          return "livre emprunté"
     return "indisponible" 

    def retourner (self):
        self.dispo = True
        return"livre retourné"

    def __str__(self):
      return f"titre: {self.titre}"

class Roman( Livre):
    def __init__(self, titre ,auteur ,annee, genre ,dispo=True):
             super().__init__( titre ,auteur ,annee, dispo)
             self.genre = genre

    def __str__(self) :
             strl = super().__str__()
             return strl + f", genre : {self.genre}"

class Bibliotheque:
    def __init__(self):
                self.livres = []

    def ajouter_livre(self , livre):
          self.livres.append(livre)

    def lister_livre(self):
          return [livre for livre in self.livres]
    
    def emprunter_livre(self, titre):
        for livre in self.livres:
                if livre.titre == titre :
                      return livre.emprunter()
        return "livre introuvable"

b=Bibliotheque()
l1 =  Livre("miserables","hugo",1999,False)
b.ajouter_livre(l1)
for description in b.lister_livre():
      print(description)

print(b.emprunter_livre("Les misérables"))




    
