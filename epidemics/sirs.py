''' Illustre les oscillations possibles dans certains réseaux avec le modèle SIRS.

Introduit la fonction plot pour tracer un réseau SIRS, mais aussi SIR ou SIS avec
des paramètres bien choisis. '''

import copy
import random as rand
import sqlite3 as sq
import networkx as nx
import matplotlib as mtpl
import matplotlib.pyplot as plt
import seaborn as sb
import numpy as np

class Sirs:
    ''' Classe permettant de simuler les modèles SIR, SIRS et SIS. '''

    def __init__(self, n=60, d=[4, 2], p=0.05, graph=0.3):
        ''' n (int): nombre de personnes
            d[0] (int): duration de l'infection en tours
            d[1] (int): duration de l'immunité en tours
                s'il vaut 0, on aura un modèle SIS
                s'il est >= à turns, c'est un modèle SIR
            p (float): probabilité d'infection
            graph (nx.Graph ou int ou float): un éventuel graphe imposé,
                ou bien une densité pour qu'un graphe soit généré '''

        if isinstance(graph, (float, int)):
            # On a alors passé une densité pour la génération d'un graphe
            self.graph = nx.gnp_random_graph(n, graph, directed=True)
        else:
            self.graph = graph
        # On initialise le nombre de personnes et le tour actuel
        self.n = self.graph.number_of_nodes()
        self.turn = 1

        # On initialise les attributs
        for node in self.graph.nodes(data=True):
            # state = 0=S et 1=I, age = nombre de tours infecté
            node[1]['state'] = 0
            # age = nombre de tours infecté
            node[1]['age'] = 0
            node[1]['infections'] = 0
        for edge in self.graph.edges(data=True):
            # color = 0 neutre, 1 tentative d'infection, 2 infection transmise
            edge[2]['color'] = 0
            # sert dans l'affichage en ressorts
            # vector = 0.01 simple connection, 0.05 si essai de transmission, 1 sinon
            edge[2]['vector'] = 0.01

        self.infected = [1]
        self.removed = [0]
        # On infecte un patient zero
        _, z = rand.choice(list(self.graph.node.items()))
        z['state'] = 1
        #self.graph.node[rand.randint(0, self.n - 1)]['state'] = 1

        self.d = d
        self.p = p
        self.mod = "SIS"
        self.updatemod()

    def updatemod(self):
        ''' Met à jour le nom de modèle. '''
        self.mod = "SIS"
        if self.d[1]:
            self.mod = "SIRS"
        if self.d[1] >= self.turn:
            self.mod = "SIR"

    def plot(self):
        '''Trace l'état actuel avec évolution, portrait de phase, ...'''

        plt.figure(num=1, figsize=(15, 12))
        self.updatemod()
        plt.suptitle(f"Etat final du modèle {self.mod} après {self.turn} tours")
        with sb.axes_style('dark'):
            plt.subplot(2, 2, 1)
            # Pour l'affichage des noeuds, inutile d'avoir des axes
            plt.axis("off")

        # On génère les emplacements afin de pouvoir calculer la heatmap
        pos = nx.spring_layout(self.graph, weight='vector', pos=nx.circular_layout(self.graph))
        xa = np.array([x[0]
                       for i, x in enumerate(list(pos.values())) if self.graph.node[i]['state']])
        ya = np.array([x[1]
                       for i, x in enumerate(list(pos.values())) if self.graph.node[i]['state']])
        # La heatmap a peu d'intéret et est peu stable pour peu de valeurs
        if xa.size > 2:
            sb.kdeplot(xa, ya, shade=True, cmap="Purples", legend=False, shade_lowest=False)

        nx.draw_networkx(
            self.graph,
            pos=pos,
            with_labels=False, # Possibilité de mettre en argument
            arrows=False,
            node_color=[2 - k[1]['state'] for k in self.graph.nodes(data=True)],
            cmap=mtpl.cm.get_cmap(name="plasma"),
            vmin=0,
            vmax=2,
            edge_color=[2 - t[2]['color'] for t in self.graph.edges(data=True)],
            edge_cmap=mtpl.cm.get_cmap(name="gray"),
            edge_vmin=0,
            edge_vmax=2.3,
            node_size=5000/(self.n)+200,
            width=0.2)

        plt.title("Etat final du réseau")
        plt.plot(-1, -1, marker='o', color=(240/255, 249/255, 33/255))
        plt.plot(-1, -1.2, marker='o', color=(204/255, 71/255, 120/255))
        plt.text(-.95, -1.03, "Susceptible", fontsize=9)
        plt.text(-.95, -1.23, "Infecté", fontsize=9)
        if self.mod != "SIS":
            plt.plot(-1, -1.4, marker='o', color=(13/255, 8/255, 135/255))
            plt.text(-.95, -1.43, "Retiré", fontsize=9)

        with sb.axes_style('darkgrid'):
            plt.subplot(2, 2, 2)
        plt.title("Infectés et retirés en fonction du tour")
        plt.xlabel("Tour")

        plt.bar(list(range(1, self.turn + 1)),
                self.infected, color=(204/255, 71/255, 120/255))
        if self.mod != "SIS":
            plt.bar(list(range(1, self.turn + 1)),
                    self.removed, color=(13/255, 8/255, 135/255, 0.8))

        with sb.axes_style('darkgrid'):
            plt.subplot(2, 1, 2)
        # Portrait de phase: nombre dérivé en fonction du nombre
        plt.title("Portrait de phase de l'épidémie")
        plt.xlabel("Nombre d'individus")
        plt.ylabel("Variation du nombre d'individus")

        derivI = [0] + [self.infected[i] - self.infected[i-1] for i in range(1, len(self.infected))]
        plt.plot(self.infected, derivI, marker="o", color=(204/255, 71/255, 120/255, 0.6))
        if self.mod != "SIS":
            derivR = [0] + [self.removed[i] - self.removed[i-1]
                            for i in range(1, len(self.removed))]
            plt.plot(self.removed, derivR, marker="o", color=(13/255, 8/255, 135/255, 0.6))

        plt.show()

    def increment(self, turns=1):
        ''' Simule n tours de l'épidémie.
            turns (int): nombre de tours à simuler '''
        for _ in range(turns):
            # Afin d'éviter de faire une boucle de comptage,
            # on compte les infectés et retirés au fur et à mesure
            counter = 0
            remcounter = 0
            # Evite de traiter des patient infectés dès ce tour-ci
            for node in [k for k in self.graph.nodes(data=True) if k[1]['state'] >= 1]:
                # On ne s'interesse qu'aux patients infectés
                if node[1]['state'] == 1:
                    counter += 1
                    if node[1]['age'] < self.d[0]:
                        node[1]['age'] += 1
                        for other in self.graph[node[0]]:
                            # Si l'autre est dans l'état S
                            if not self.graph.node[other]['state']:
                                if rand.random() < self.p:
                                    # On met les stats au mode infecté
                                    self.graph.node[other]['state'] = 1
                                    self.graph.node[other]['age'] = 0 # par sureté (non nécessaire)
                                    self.graph.node[other]['infections'] += 1

                                    # De plus, on le compte
                                    counter += 1

                                    # Pour la coloration
                                    self.graph.edge[node[0]][other]['color'] = 2
                                    # Servira de ressort dans le graphe
                                    self.graph.edge[node[0]][other]['vector'] = 1
                                else:
                                    self.graph.edge[node[0]][other]['color'] = 1
                                    self.graph.edge[node[0]][other]['vector'] = 0.05
                    else:
                        # En fin de compte, il n'est pas infecté, mais retiré/susceptible
                        counter -= 1

                        if self.d[1]:
                            # Passage en mode retiré
                            node[1]['state'] = 2
                            node[1]['age'] = 0
                            remcounter += 1
                        else:
                            # Passage en mode susceptible
                            node[1]['state'] = 0
                            node[1]['age'] = 0
                elif node[1]['state'] == 2:
                    if node[1]['age'] < self.d[1]:
                        # On ne compte que celles qu'on ne va pas retirer
                        remcounter += 1
                        node[1]['age'] += 1
                    else:
                        # Remise à zero des statistiques
                        node[1]['state'] = 0
                        node[1]['age'] = 0
            # On enregistre succesivement les valeurs pour les tracer plus tard
            self.infected.append(counter)
            self.removed.append(remcounter)
            self.turn += 1

    def increment_avg(self, turns=50, sample=600):
        ''' Calcule l'évolution moyenne sur n tours à partir du tour actuel
            sample (int): nombre d'essais à réaliser

        '''

        # On crée le tableau en mémoire puisqu'il est temporaire
        connection = sq.connect(':memory:')
        c = connection.cursor()
        c.execute('CREATE TABLE Statistics '
                  '(SimId integer, Turn integer, Infected integer, Removed integer)')
        # La base de données permet le calcul rapide et efficace de moyennes sur
        # un grand nombre de tours et de graphes

        # On applique les itérations pour chaque simulation
        for m in range(sample):
            # Attention aux structures mutables
            g = copy.deepcopy(self)
            for i in range(g.turn, g.turn + turns):
                g.increment()
                c.execute('INSERT INTO Statistics VALUES(?, ?, ?, ?)',
                          (m, i, g.infected[-1], g.removed[-1]))

        connection.commit()
        # On veut tracer des moyennes par tour
        for k in c.execute('SELECT Turn, AVG(Infected), AVG(Removed) FROM Statistics'
                           ' GROUP BY Turn ORDER BY Turn ASC'):
            self.infected.append(k[1])
            self.removed.append(k[2])

        c.close()
        connection.close()

        # Les noeuds sont finalement incrémentés aléatoirement
        g = copy.deepcopy(self)
        g.increment(turns)
        self.graph = g.graph
        self.turn = g.turn

if __name__ == "__main__":
    s = Sirs()
    s.increment_avg(100, 1000)
    s.plot()
