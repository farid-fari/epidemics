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
                                {"i": i, "j": j, "k": b})

            # Infection du patient zero
            z = random.randint(0, 97)
            ses.run("MATCH (p:Personne {id: {z}}) SET p.state = 1", {"z": z})

            #TESTETSTETSTET
            ses.run("Match (p:Personne), (q:Personne)"
                    "WHERE id(p) < id(q) CREATE (p)-[r:Lien {p: 0.1}]->(q)")
        self.d = d
        self.turn = 0
        self.infected, self.removed = [], []

    def step(self, turns=1):
        ''' Avancer de turns tours '''

        c, r = 0, 0

        with self.driver.session() as ses:
            for n in ses.run("MATCH (p:Personne)-[r:Lien]->(q) "
                             "WHERE p.state > 0 "
                             "RETURN p, q, r.p").records():
                if n['p']['state'] == 1:
                    if n['p']['age'] < self.d[0]:
                        if n['q']['state'] == 0 and random.random() < n['r.p']:
                            ses.run("MATCH (p:Personne {id: {i}}) SET p.state = 1",
                                    {"i": n['q']['id']})
                            ses.run("MATCH (p:Personne {id: {i}}), (q:Personne {id: {j}}) "
                                    "CREATE (p)-[:Infection]->(q)",
                                    {"i": n['p']['id'], "j": n["q"]["id"]})
                            ses.run("MATCH (p:Personne {id: {i}}) SET p.age = {p}",
                                    {"i": n['p']['id'], "p": n['p']['age']+1})
                            c += 1
                    else:
                        ses.run("MATCH (p:Personne {id: {i}}) SET p.state = 2 AND p.age = 0",
                                {"i": n['p']['id']})
                        r += 1
                else:
                    # state = 2
                    if n['p']['age'] < self.d[1]:
                        ses.run("MATCH (p:Personne {id: {i}}) SET p.age = {p}",
                                {"i": n['p']['id'], "p": n['p']['age']+1})

                    else:
                        ses.run("MATCH (p:Personne {id: {i}}) SET p.state = 2 AND p.age = 0",
                                {"i": n['p']['id']})

        self.turn += 1
        if turns > 1:
            self.step(turns-1)

sect = [Secteur(i) for i in MAP[:1]]
for k in [t for t in TIMES if (str(t).zfill(4))[-2:] == '00' and t == 1000]:
    c = depl_matrix(sect, k)
    s = NeoSirs(c)
    s.step(20)
