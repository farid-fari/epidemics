''' Permet de convertir les données de trajectométrie en un modèle SIR.

Introduit la fonction to_sirs, pouvant prendre un certain temps à s'éxecuter. '''

import time
import networkx as nx
import numpy as np
from epidemics.sirs import Sirs
from trajectometry.interface import MAP, TIMES, Secteur
from trajectometry.transition import passage

def to_sirs(secteurs, heure):
    ''' Convertit les données de trajectométrie en modèle SIRS.

    secteurs (Secteur list): la liste des secteurs préchargés
    heure (int): l'heure à laquelle on veut faire le modèle

    Retourne: acc (np.array) les déplacements durant l'heure donnée '''

    g = nx.DiGraph()
    g.add_nodes_from(MAP[:-2])

    acc = np.zeros((98, 98))
    for i, j in enumerate(secteurs):
        t = time.time()
        print(j.code, ' - ', heure, end='')
        m, _ = passage(MAP[i], heure, memo=j)
        acc += m
        print(' - ', round(time.time()-t, 1), 's')
    acc /= 97
    return acc

sect = [Secteur(i) for i in MAP[:1]]
for k in TIMES:
    to_sirs(sect, k)
