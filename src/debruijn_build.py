import numpy as np
import graph as g
import sys

import utils as ut

class Node:
    def __init__(self, id, kmer):
        self.id = id
        self.kmer = kmer
        self.successors = []
        self.predecessors = []
        self.times = 1


def getSeq(path):
    with open(path, "r") as fichier:
        sequence = ""
        idx = 0

        for ligne in fichier:
            idx +=1 
            ligne = ligne.strip()

            if ligne.startswith("@"):
                continue
            else :
                sequence += ligne
        return sequence 
    

def debruijn_build(f, k, outf):
    nodes = {}
    node_counter = 0            

    s_read = getSeq(f)
    l_read = len(s_read)

    # Création de la liste des k-mères
    for i in range(l_read):
        klen = i + k
        seq = s_read[i:klen]
        if(klen <= l_read and '\n' not in seq):
            if seq in nodes:
                nodes[seq].times += 1
            else:
                node_counter += 1
                nodes[seq] = Node(node_counter, seq)
            if i > 0:
                prev = s_read[i - 1: i - 1 + k]
                nodes[prev].successors.append(nodes[seq])
                nodes[seq].predecessors.append(nodes[prev])

    # Normalisation
    norm = []
    done_nodes = set()
    
    for node in nodes.values():
        if node not in done_nodes: # Itération sur les noeuds
            complement = node.kmer[::-1].translate(str.maketrans('ATCG', 'TAGC'))
            complement_node = nodes.get(complement)

            if complement_node: # Ajouter à la liste des noeuds traités
                done_nodes.add(node)
                done_nodes.add(complement_node)

                # On garde priorise le noeud avec l'id le plus bas
                node.id = min(node.id, complement_node.id)
                node.times += complement_node.times

                # On ajoute au noeud les successeurs et prédecesseurs du noeud normalisé
                node.successors.extend(complement_node.successors)
                node.predecessors.extend(complement_node.predecessors)

                # On update les liens des prédecesseurs et successeurs avec le nouveau noeud
                for successor in complement_node.successors:
                    if successor != node:
                        successor.predecessors.append(node)
                for predecessor in complement_node.predecessors:
                    if predecessor != node:
                        predecessor.successors.append(node)
            norm.append(node)

    return norm


def main():
    if len(sys.argv) < 2:
        print("Usage : debruijn_build.py path k outf")
        exit(1)
    f = sys.argv[1]
    k = int(sys.argv[2])
    outf = sys.argv[3]

    norm = debruijn_build(f,k,None)
    fichier = ut.create(outf)

    ut.write(fichier, "{} {}\n".format(len(norm), k))
    for node in norm:
        node.successors = list(set(node.successors))
        node.predecessors = list(set(node.predecessors))
        successors = ",".join(str(successor.id) for successor in node.successors)
        predecessors = ",".join(str(predecessor.id) for predecessor in node.predecessors)
        ut.write(fichier, "{} {} {} {} {}\n".format(node.id, node.kmer, node.times, successors, predecessors))
    fichier.close()


main()