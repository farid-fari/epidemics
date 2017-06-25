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
                # On augmente arbitrairement la proba
                # A revoir plus tard
                g.add_edge(MAP[i], MAP[j], p=b)

    return Sirs(graph=g)

sect = [Secteur(i) for i in MAP]
for k in [t for t in TIMES if (str(t).zfill(4))[-2:] == '00']:
    c = depl_matrix(sect, k)
    s = to_sirs(c)
    s.increment_avg(100, 300)
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
