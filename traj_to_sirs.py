# -*- coding: UTF-8 -*-
''' Se sert de LemonGraph pour gerer les graphes. '''

import os
import random
import time
import numpy as np
import LemonGraph as lg
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
        print str(j.code) + ' - ' + str(heure)
        m, _ = passage(MAP[i], heure, memo=j)
        acc += m
        print ' -  ' + str(round(time.time()-t, 1)) +  's'

    acc /= len(secteurs)

    return acc

class Sirs:
    ''' Modele SIRS avec LG. '''

    def __init__(self, dbpath, m):
        ''' m (np.array): la matrice des déplacements
            dbpath (str): l'endroit ou va la BDD '''
        if os.path.exists(dbpath):
            # Pour etre plus efficace
            os.unlink(dbpath)
        self.g = lg.Graph(dbpath)
        with self.g.transaction(write=True) as txn:
            self.nodes = []
            for i in range(0, 98):
                self.nodes.append(txn.node(type='sect', value=MAP[i]))
                self.nodes[-1]['state'] = 0
            for i, a in enumerate(m):
                for j, b in enumerate(a):
                    # i correspond au secteur d'arrivée (ligne)
                    # j correspond au secteur de départ (colonne)
                    if i != j and b != 0:
                        # On augmente arbitrairement la proba
                        # A revoir plus tard
                        txn.edge(src=self.nodes[i], tgt=self.nodes[j], value=97*b)
        # Patient zero
        z = random.choice(self.nodes)
        z['state'] = 1

    def step(self, i=1):
        with self.g.transaction(write=False) as txn:
            for e in txn.query('n(state=1)->e()->n()'):
                print e
        if i > 1:
            step(i-1)

sect = [Secteur(i) for i in MAP[:1]]

for k in [t for t in TIMES if (str(t).zfill(4))[-2:] == '00']:
    c = depl_matrix(sect, k)
    s = Sirs('test' + str(k) +'.db', c)
    s.step()
