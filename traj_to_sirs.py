''' Permet de convertir les données de trajectométrie en un modèle SIR.

Introduit la fonction to_sirs, pouvant prendre un certain temps à s'éxecuter. '''

import sys
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
        print(f'{j.code} - {heure}', end='')
        sys.stdout.flush()
        m, _ = passage(MAP[i], heure, memo=j)
        acc += m
        print(f' -  {round(time.time()-t, 1)}s')

    acc /= len(secteurs)

    # Déboggage éventuel
    # for i in range(98):
    #     for j in range(98):
    #         if acc[i][j]:
    #             print((i, j), acc[i][j])

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

sect = [Secteur(i) for i in MAP]
for k in [t for t in TIMES if (str(t).zfill(4))[-2:] == '00']:
    c = depl_matrix(sect, k)
    s = to_sirs(c)
    s.p = 0.9
    s.increment_avg(100, 300)
    s.plot()

# Heures produisant un résulat non nul (p=0.9):
# 400 = oscillations amorties
# 700 = oscillations infinies!!
# 800 - oscillations intenses et amorties
# 900 - idem
# 1000 - idem mais non amorti
# 1100 - oscilations peu itenses!!!
# 1200 - oscillations trees tres tres intenses!!
# 1300 - moyennement intense, amorti
# 1400 - comme 1200
# 1500 - comme 1300
# 1600 - comme 1200
# 1700 - comme 800
# 1800 - comme 1200
# 1900 - oscillations tres régulières
# 2000 - idem
# 2100 - oscillations s'amortiaant très régulièrement
