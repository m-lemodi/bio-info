class graph:
    def __init__(self, liste):
        self.liste = liste
    
    def display(self):
        for el in self.liste:
            print("seq mere : ", el.seq_mere, " multiplicité : ", el.multiplicité)
        print(len(self.liste))


    def getListe(self):
        return self.liste
    
    def getNoeudIndx(self, idx):
        return self.liste[idx]
    
    def removeNoeud(self, n):
        for no in self.liste:
            if no.seq_mere == n.seq_mere:
                self.liste.remove(n)

    def getListeSeq(self):
        res = []
        for n in self.liste:
            res.append(n.seq_mere)
        return res
    
    def getNoeud(self, seq):
        for n in self.liste:
            if n.seq_mere == seq:
                return n    
        return None
    

class Noeud :

    def __init__(self, seq_mere, indx,multiplicité, predecesseur, successeurs) :
        self.seq_mere = seq_mere
        self.indx = indx
        self.multiplicité = multiplicité
        self.predecesseur = predecesseur
        self.successeurs = successeurs
