''' Permet de convertir les données de trajectométrie en un modèle SIR.

Introduit la fonction to_sirs, pouvant prendre un certain temps à s'éxecuter. '''

import time
import networkx as nx
import numpy as np
from epidemics.sirs import Sirs
from trajectometry.interface import MAP, TIMES, Secteur
from trajectometry.transition import passage

def to_sirs(heure):
    ''' Convertit les données de trajectométrie en modèle SIRS.

    heure (int): l'heure à laquelle on veut faire le modèle

    Retourne: s (epidemics.Sirs) un modèle SIRS'''

    g = nx.DiGraph()
    g.add_nodes_from(MAP[:-2])
    s = Sirs(graph=g)

    sect = [Secteur(i) for i in MAP[:5]]
    acc = np.zeros((98, 98))
    for i, j in enumerate(sect):
        t = time.time()
        print(MAP[i], end='')
        m, _ = passage(MAP[i], heure, memo=j)
        acc += m
        print(' - ', round(time.time()-t, 1), 's')
    acc /= 97
    print(acc)
    #return Sirs(len(MAP), g)

to_sirs(2000)
