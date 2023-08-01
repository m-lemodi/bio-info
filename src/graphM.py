
def normalisation(seq):
    res = list(seq)
    for idx in range(len(res)):
        if (res[idx] == 'A'):
            res[idx] = 'T'
            continue
        if (res[idx] == 'T'):
            res[idx] = 'A'
            continue
        if (res[idx] == 'C'):
            res[idx] = 'G'
            continue
        if (res[idx] == 'G'):
            res[idx] = 'C'
            continue
    return ("".join(res))[::-1]


class graph:
    def __init__(self, liste, k):
        self.liste = liste
        self.k = k
    
    def display(self):
        for el in self.liste:
            if el != None:
                print("seq mere : ", el.seq_mere, " multiplicité : ", el.multiplicité, "indx : ", el.indx )

    def size(self):
        res = 0
        for el in self.liste:
            if el != None:
                res += 1
        return res

    def getListe(self):
        return self.liste
    
    def getNoeudIndx(self, idx):
        return self.liste[idx]
    
    def removeNoeud(self, n):
        indx = self.getIndx(n) 
        for i in range(indx + 1, len(self.liste)):
            self.liste[i].indx -= 1
        for i in range(len(self.liste)):
            suc, pre = self.liste[i].successeurs, self.liste[i].predecesseur
            if suc != None:
                for x in range(len(suc)):
                    if suc[x] > indx:
                        suc[x] -=1
            if pre != None:
                for x in range(len(pre)):
                    if pre[x] >= indx:
                        pre[x] -=1

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

    def getIndx(self, n):
        for indx in range(len(self.liste)):
            if self.liste[indx].seq_mere == n.seq_mere:
                return indx
      


    def fusionFF(self,n1,n2) :
        seq1 = n1.seq_mere
        indx1 = self.getIndx(n1)

        seq2 = n2.seq_mere

        self.liste[indx1].seq_mere = seq1 + seq2[self.k-1:]
        print("ff", seq1, seq2)
        for m in n2.multiplicité:
            self.liste[indx1].multiplicité.append(m)
        n1.successeurs = n2.successeurs
        self.removeNoeud(n2)
        

    def fusionFR(self,n1,n2) :
        seq1 = n1.seq_mere
        indx1 = self.getIndx(n1)

        seq2 = n2.seq_mere
        seq2_noc = normalisation(seq2)
        print("FR", seq1, seq2_noc)
        self.liste[indx1].seq_mere = seq1 + seq2_noc[self.k-1:]
        for m in n2.multiplicité:
            self.liste[indx1].multiplicité.append(m)
        self.removeNoeud(n2)


    def fusionRR(self,n1,n2) :
        self.fusionFF(n2,n1)

    def fusionRF(self,n1,n2) :
        seq1 = n1.seq_mere
        seq1_noc = normalisation(seq1)
        indx1 = self.getIndx(n1)

        seq2 = n2.seq_mere

        print("RF", seq1_noc, seq2)
        self.liste[indx1].seq_mere = seq1_noc + seq2[self.k-1:]
        for m in n2.multiplicité:
            self.liste[indx1].multiplicité.append(m)       
        self.removeNoeud(n2)    

    
    def fusion(self, n1, n2):

        seq1 = n1.seq_mere
        seq1_noc = normalisation(seq1)
        indx1 = self.getIndx(n1)

        seq2 = n2.seq_mere
        seq2_noc = normalisation(seq2)
        indx2 = self.getIndx(n2)

        l = len(seq1)
        if seq1[l - (self.k-1):] == seq2[:self.k-1]: #FF
            self.liste[indx1].seq_mere = seq1 + seq2[self.k-1:]
            print("ff", seq1, seq2)
            for m in n2.multiplicité:
                self.liste[indx1].multiplicité.append(m)
            n1.successeurs = n2.successeurs
            self.removeNoeud(n2)

        if  seq1_noc[l - (self.k-1):] == seq2_noc[:self.k-1]: #RR
            self.fusion(n2,n1)

        if  seq1[l - (self.k-1):] == seq2_noc[:self.k-1]: #FR
            print("FR", seq1, seq2_noc)
            self.liste[indx1].seq_mere = seq1 + seq2_noc[self.k-1:]
            for m in n2.multiplicité:
                self.liste[indx1].multiplicité.append(m)
            self.removeNoeud(n2)


        if  seq1_noc[l - (self.k-1):] == seq2[:self.k-1]: #RF
            print("RF", seq1_noc, seq2)
            self.liste[indx1].seq_mere = seq1_noc + seq2[self.k-1:]
            for m in n2.multiplicité:
                self.liste[indx1].multiplicité.append(m)       
            self.removeNoeud(n2)    

class Noeud :

    def __init__(self, seq_mere, indx,multiplicité, predecesseur, successeurs) :
        self.seq_mere = seq_mere
        self.indx = indx
        self.multiplicité = multiplicité
        self.predecesseur = predecesseur
        self.successeurs = successeurs

    def displayP(self):
        res = ""
        l = len(self.predecesseur)
        for i in range(l):
            res+= str(self.predecesseur[i])
            if (i != l-1):
                res+=","
        return res

    def displayS(self):
        res = ""
        l = len(self.successeurs)
        for i in range(l):
            res+= str(self.successeurs[i])
            if (i != l-1):
                res+=","
        return res

    def displayM(self):
        res = ""
        l = len(self.multiplicité)
        for i in range(l):
            res+= str(self.multiplicité[i])
            if (i != l-1):
                res+=","
        return res