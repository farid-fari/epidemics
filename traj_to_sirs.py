''' Permet de convertir les données de trajectométrie en un modèle SIR.

Introduit la fonction to_sirs, pouvant prendre un certain temps à s'éxecuter. '''

import sys
import time
import random
import networkx as nx
import numpy as np
from neo4j.v1 import GraphDatabase
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

    return acc

class NeoSirs:
    ''' Convertit une matrice de déplacements en un modèle SIRS figé
    !!! Requiert un serveur neo4j correctement configuré '''

    def __init__(self, m, d=[4, 2], uri="bolt://localhost:7687"):
        ''' m (np.array): la matrice des déplacements '''

        self.driver = GraphDatabase.driver(uri, auth=("neo4j", "password"))

        with self.driver.session() as ses:
            # On vide la BDD
            ses.run("MATCH (n) DETACH DELETE n")

            for i in range(98):
                ses.run("CREATE (p:Personne {id: {i}, state: 0, age: 0})", {"i": i})

            for i, a in enumerate(m):
                for j, b in enumerate(a):
                # i correspond au secteur d'arrivée (ligne)
                # j correspond au secteur de départ (colonne)
                    if i != j and b != 0:
                        # On augmente arbitrairement la proba
                        # A revoir plus tard
                        ses.run("MATCH (p:Personne {id: {i}}),(q:Personne {id:{j}})"
                                "CREATE (p)-[r:Lien {p: {k}}]->(q)",
                                {"i": i, "j": j, "k": 97*b})

            # Infection du patient zero
            z = random.randint(0, 97)
            ses.run("MATCH (p:Personne {id: {z}}) SET p.state = 1", {"z": z})

            #TESTETSTETSTET
            ses.run("Match (p:Personne), (q:Personne)"
                    "WHERE id(p) < id(q) CREATE (p)-[r:Lien {p: 0.01}]->(q)")
        self.d = d

    def step(self, turns=1):
        ''' Avancer de turns tours '''

        with self.driver.session() as ses:
            for n in ses.run("MATCH (p:Personne)-[r:Lien]->(q) "
                             "WHERE p.state > 0 "
                             "RETURN p, q, r.p").records():
                if n['p']['age'] < self.d[0]:
                    if n['q']['state'] == 0 and random.random() < n['r.p']:
                        ses.run("MATCH (p:Personne {id: {i}}) SET p.state = 1",
                                {"i": n['q']['id']})
                        ses.run("MATCH (p:Personne {id: {i}}), (q:Personne {id: {j}}) "
                                "CREATE (p)-[:Infection]->(q)",
                                {"i": n['p']['id'], "j": n["q"]["id"]})

        if turns > 1:
            self.step(turns-1)

sect = [Secteur(i) for i in MAP[:1]]
for k in [t for t in TIMES if (str(t).zfill(4))[-2:] == '00' and t == 1000]:
    c = depl_matrix(sect, k)
    s = NeoSirs(c)
    s.step()

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
