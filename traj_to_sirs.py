''' Permet de convertir les données de trajectométrie en un modèle SIR.

Introduit la fonction to_sirs, pouvant prendre un certain temps à s'éxecuter. '''

import sys
import time
import networkx as nx
import numpy as np
from epidemics.sirs import Sirs
from trajectometry.interface import MAP, TIMES, Secteur
from trajectometry.transition import passage

def depl_matrix(secteurs, heure, verbose=False):
    ''' Convertit les données de trajectométrie en modèle SIRS.

    secteurs (Secteur list): la liste des secteurs préchargés
    heure (int): l'heure à laquelle on veut faire le modèle
    verbose (bool): s'il faut faire du bruit

    retourne: acc (np.array) les déplacements durant l'heure donnée '''

    acc = np.zeros((98, 98))
    for i, j in enumerate(secteurs):
        if verbose:
            t = time.time()
            print(f'{j.code} - {heure}', end='')
            sys.stdout.flush()
        m, _ = passage(MAP[i], heure, memo=j)
        acc += m
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
                g.add_edge(MAP[i], MAP[j], p=b)
    if prev:
        prev.graph = g
        return prev
    return Sirs(d=[8, 3], graph=g)

sect = [Secteur(i) for i in MAP]
s = None

for day in range(5):
    # Seulement les heures piles
    for k in [t for t in TIMES if (str(t).zfill(4))[-2:] == '00']:
        print(f'{day}-- {str(k).zfill(4)[:2]} --')
        c = depl_matrix(sect, k)
        s = to_sirs(c, prev=s)
        s.increment(2)

s.plot()

# Heures produisant un résulat non nul (p=97*b):
# 400: oscillations rapidement atténuées
# 500: courbe decroissante stable
# 1100: entretient constant
# 1200: oscillations amorties
# 1300: régime d'oscillations faibles
# 1400: oscillations chaotiques
# 1500: entretien constant
# 1600: idem
# 1700: oscillations intenses
# 1800: idem
# 1900: idem
