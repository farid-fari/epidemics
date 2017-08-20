''' Permet de convertir les données de trajectométrie en un modèle SIR.

Introduit la fonction to_sirs, pouvant prendre un certain temps à s'éxecuter. '''

import sys
import time
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from epidemics.sirs import Sirs
from trajectometry.interface import MAP, TIMES, Secteur
from trajectometry.transition import passage

def depl_matrix(secteurs, heure, verbose=False):
    ''' Donne une matrice de probabilité de présence d'un individu d'un secteur
    dans un autre. M[i][j]: proba qu'un individu de i soit au secteur j à l'heure.

    secteurs (Secteur list): la liste des secteurs préchargés
    heure (int): l'heure à laquelle on veut calculer la matrice
    verbose (bool): s'il faut faire du bruit

    retourne: n (np.array) la matrice spécifiée '''

    acc = np.zeros((97, 98))
    for i, j in enumerate(secteurs[:-1]):
        if verbose:
            t = time.time()
            print(f'{j.code} - {heure}', end='')
            sys.stdout.flush()

        # La proba correspond aux positions des gens à l'heure, le tout
        # divisé par le nombre de personnes
        _, (_, m) = passage(MAP[i], heure, memo=j)
        acc[i] = m / sum(m)

        if verbose:
            print(f' -  {round(time.time()-t, 1)}s')
    return acc

def to_sirs(m, prev=None):
    ''' Convertit une matrice de déplacements en un modèle SIR figé

    m (np.array): la matrice des déplacements
    prev (Sirs): un éventuel modèle à mettre à jour

    retourne: s (epidemics.Sirs) le modèle SIRS obtenu '''

    if prev is None:
        g = nx.DiGraph()
        g.add_nodes_from(MAP)
    else:
        g = prev.graph

    for i, a in enumerate(m):
        for j, b in enumerate(a):
            # i correspond au secteur d'arrivée (ligne)
            # j correspond au secteur de départ (colonne)
            if i != j:
                # On chosira en fonction:
                #   - p=1 pour avoir un modèle simple (ajouter une condition avec b)
                #   - p=b(*λ) pour avoir un modèle plus réaliste
                if b:
                    g.add_edge(MAP[i], MAP[j], p=1)
                else:
                    g.add_edge(MAP[i], MAP[j], p=0)
    if prev:
        prev.graph = g
        return prev
    return Sirs(d=[4, 2], graph=g)

t = time.time()
print('Chargement des secteurs...', end='')
sect = [Secteur(i) for i in MAP]
print(f'{round(time.time()-t, 1)}s')
s = None
x, y = [], []

for day in range(1):
    # Seulement les heures piles
    for k in [t for t in TIMES if (str(t).zfill(4))[-2:] == '00']:
        print(f'{day}j {str(k).zfill(4)[:2]}h -- R0≈', end=' ')
        c = depl_matrix(sect, k)
        s = to_sirs(c, prev=s)
        # On simule deux tours par jour
        s.increment(2)
        s.updatemod()
        x.append(day*2400+k)
        y.append(s.r0)
        print(s.r0)

s.plot()
plt.plot(x, y, 'g')
plt.plot([0, max(x)], [1, 1], 'r')
plt.show()
