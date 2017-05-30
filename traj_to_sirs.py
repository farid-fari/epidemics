''' Permet de convertir les données de trajectométrie en un modèle SIR.

Introduit la fonction to_sirs, pouvant prendre un certain temps à s'éxecuter. '''

import time
import networkx as nx
import numpy as np
from epidemics.sirs import Sirs
from trajectometry.interface import MAP, TIMES, Secteur
from trajectometry.transition import passage

def depl_matrix(secteurs, heure):
    ''' Convertit les données de trajectométrie en modèle SIRS.

    secteurs (Secteur list): la liste des secteurs préchargés
    heure (int): l'heure à laquelle on veut faire le modèle

    retourne: acc (np.array) les déplacements durant l'heure donnée '''

    acc = np.zeros((98, 98))
    for i, j in enumerate(secteurs):
        t = time.time()
        print(j.code, ' - ', heure, end='')
        m, _ = passage(MAP[i], heure, memo=j)
        acc += m
        print(' - ', round(time.time()-t, 1), 's')
    acc /= 97
    return acc

def to_sirs(m):
    ''' Convertit une matrice de déplacements en un modèle SIR figé

    m (np.array): la matrice des déplacements

    retourne: s (epidemics.Sirs) le modèle SIRS obtenu '''

    g = nx.DiGraph()
    g.add_nodes_from(MAP[:-2])

    for i, a in enumerate(m):
        for j, b in enumerate(a):
            # i correspond au secteur d'arrivée (ligne)
            # j correspond au secteur de départ (colonne)
            if i != j and b != 0:
                g.add_edge(MAP[i], MAP[j])
    return Sirs(graph=g)

sect = [Secteur(i) for i in MAP[:1]]
for k in TIMES:
    c = depl_matrix(sect, k)
    s = to_sirs(c)
    s.increment(100)
    s.plot()
