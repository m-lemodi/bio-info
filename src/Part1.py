import numpy as np
import graph as g
import sys

import utils as ut

path = "../examples/reads_abeta42_l23_seed31_N5000_mu0.fasta"
path_norm = "../examples/reads_abeta42_l23_seed31_N5000_mu0_norc.fasta"
def getSeq(path, saut=False):
    with open(path, "r") as fichier:
        sequence = ""
        identifiant = ""

        for ligne in fichier:
            ligne = ligne.strip()

            if ligne.startswith("@"):
                identifiant += ligne # Récupération de l'identifiant sans le ">"
            else :
                if (saut):
                    ligneSaut = ligne + '\n'
                    if (len(ligneSaut) != 1):
                        sequence += ligneSaut # Ajout de la séquence à la variable "sequence"
                else:
                    sequence += ligne
        return sequence 
    

def debruijn_build(f, k, outf):
    s = getSeq(f)
    l = len(s)
    s_read = getSeq(f, True)
    l_read = len(s_read)

    #liste k-mere
    k_mere = []
    for i in range(l_read):
            if(i+k <= l_read and '\n' not in s_read[i:k+i]):
                k_mere.append(s_read[i:k+i])

    #liste multiplicate 
    multiplicite = {}
    for seq_mere in k_mere :
        multiplicite[seq_mere] = 0

    

    for seq_mere in k_mere :
        if (seq_mere in s):
            multiplicite[seq_mere] += 1

    k_mere_uniques = []
    for seq_mere in k_mere:
        if seq_mere not in k_mere_uniques:
            k_mere_uniques.append(seq_mere)
        
    graph = createGraph(k_mere_uniques, multiplicite)

    for noeud in graph.getListe():
        seq = noeud.seq_mere
        seq_noc = normalisation(seq)

        if seq_noc in graph.getListeSeq():
            noeudDuplica = graph.getNoeud(seq_noc)
            noeud.multiplicité += noeudDuplica.multiplicité
            graph.removeNoeud(noeudDuplica)



    return graph


def createGraph(k_mere , multiplicite):
    graph = []
    for idx in range(len(k_mere)):
        graph.append(g.Noeud(k_mere[idx],idx,multiplicite[k_mere[idx]], None, None))
    for idx in range(len(graph)):
        if not(idx - 1  < 0):
            graph[idx].predecesseur = graph[idx -1]
        if (idx + 1  < len(graph)):
            graph[idx].successeurs = graph[idx + 1]
    return g.graph(graph)


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



def main():
    f = sys.argv[1]
    k = int(sys.argv[2])
    outf = sys.argv[3]


    graph = (debruijn_build(f,k,outf))
    #graph.display()

    fichier = ut.create(outf)

    l = graph.getListe()
    N = len(l)

    ut.write(fichier, "{} {}\n".format(N, k))
    for id in range(N):
        pre = " " if  l[id].predecesseur == None else  l[id].predecesseur.indx
        suc = " " if  l[id].successeurs == None else  l[id].successeurs.indx
        ut.write(fichier ,"{} ".format(id) + l[id].seq_mere + " {} {} {}\n".format(l[id].multiplicité, pre, suc))
    fichier.close()


main()