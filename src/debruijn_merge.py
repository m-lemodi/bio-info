import numpy as np
import graphM as g
import sys

import utils as ut


def createGraphByPath(fichier):
    res = []
    ligne = fichier.readline() #premier ligne
    var = ligne.split()
    k = var[1]
    ligne = fichier.readline() #premier ligne


    while ligne:
        
        splitLigne = ligne.split()
        indx = splitLigne[0]
        seq = splitLigne[1]
        mult = splitLigne[2]
        pred, suc = None,None
        if (len(splitLigne) == 5):
            pred = splitLigne[3]
            suc = splitLigne[4]
        else:
            if(ligne[len(indx) + len(seq) + len(mult) + 3] == ' '):
                suc = splitLigne[3]
            else:
                pred = splitLigne[3]

        if (pred != None):
            pred = pred.split(',')
            for i in range(len(pred)):
                pred[i] = int(pred[i])
        if suc != None:
            suc = suc.split(',')
            for i in range(len(suc)):
                suc[i] = int(suc[i])

        if mult != None:
            mult = mult.split(',')
            for i in range(len(mult)):
                mult[i] = int(mult[i])


        noeud = g.Noeud(seq, int(indx), mult, pred, suc)
        res.append(noeud)
        ligne = fichier.readline()  


    return g.graph(res, int(k))
    

def graphMerge(graph):
    N = len(graph.getListe())
    k = graph.k
    print()
    for noeud in graph.getListe():

        seq1 = noeud.seq_mere
        seq1_noc = g.normalisation(seq1)
        indx1 = graph.getIndx(noeud)
        l = len(seq1)

        if noeud.successeurs != None and len(noeud.successeurs) == 1: #Dir 1
            voisinIndx = int(noeud.successeurs[0])
            voisin = graph.getListe()[voisinIndx]

            seq2 = voisin.seq_mere
            seq2_noc = g.normalisation(seq2)
            indx2 = graph.getIndx(voisin)

            if seq1[l - (k-1):] == seq2[:k-1]: #FF
                if (voisin.predecesseur != None and len(voisin.predecesseur) == 1 and int(voisin.predecesseur[0]) == noeud.indx):
                    graph.fusionFF(noeud, voisin)
                    break
                
            if seq1[l - (k-1):] == seq2_noc[:k-1]: #FR
                if (voisin.successeurs != None and len(voisin.successeurs) == 1 and int(voisin.successeurs[0]) == noeud.indx):
                    graph.fusionFR(noeud, voisin)
                    break

        if noeud.predecesseur != None and len(noeud.predecesseur) == 1: #Dir 2
            voisinIndx = int(noeud.predecesseur[0])
            voisin = graph.getListe()[voisinIndx]

            seq2 = voisin.seq_mere
            seq2_noc = g.normalisation(seq2)
            indx2 = graph.getIndx(voisin)

            if seq1_noc[l - (k-1):] == seq2[:k-1]: #RF
                if (voisin.predecesseur != None and len(voisin.predecesseur) == 1 and int(voisin.predecesseur[0]) == noeud.indx):
                    graph.fusionRF(noeud, voisin)
                    break

            if  seq1_noc[l - (k-1):] == seq2_noc[:k-1]: #RR
                if (voisin.successeurs != None and len(voisin.successeurs) == 1 and int(voisin.successeurs[0]) == noeud.indx):
                    graph.fusionRR(noeud, voisin)
                    break

 
    if len(graph.getListe()) != N:
        return graphMerge(graph)
    return graph


def main():
    f = sys.argv[1]
    outf = sys.argv[2]

    fichier = ut.openF(f)

    graphO = createGraphByPath(fichier)
    graph = graphMerge(graphO)


    l = graph.getListe()
    N = graph.size()
    k = graph.k

    fichier = ut.create(outf)

    ut.write(fichier, "{} {}\n".format(N, k))
    for id in range(N):
        pre = " " if  l[id].predecesseur == None else  l[id].displayP()
        suc = " " if  l[id].successeurs == None else  l[id].displayS()
        mult = l[id].displayM()
        ut.write(fichier ,"{} ".format(id) + l[id].seq_mere + " " + mult + " " + pre + " " +  suc + "\n")
    fichier.close()

main()