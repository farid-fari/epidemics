""" Introduit les classes necessaires a l'etude du marketing dans un reseau social

social.Player(initialstate) est un participant d'un Network
social.Network(players, qualities, isolationutility) est un reseau de participants, capables d'evoluer"""

import math
import random
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib as mtpl


class Player:
    """ Un participant dans un reseau social, et consommateur """

    def __init__(self, initalstate):
        self.consumption = {"a": initalstate - .5, "b": .5 - initalstate}
        # initialstate correspond a xi, on la convertit en yi et -yi pour des
        # raisons pratiques

    def optimize(self, players, isolationutility, qualities):
        """ Optimise la consommation pour la meilleure utilite en fin de tour

        Prend pour arguments players, liste des voisins ainsi que leur influence et consommation
                             isolationutility, les coefficients a et b dans la formule d'utilite en isolation
                             qualities, les qualites des produits a  et b
        Requiert a>=b et a+1<=2b pour fonctionner correctement (consommation finale entre -.5 et .5)"""
        factor = 0
        for person in players:
            # correspond a un produit matriciel
            factor += person["influence"] * (person["consumption"])
        self.consumption["a"] = (1 / (2 * isolationutility["b"])) * (factor + (qualities["a"] - qualities["b"]) / (qualities[
            "a"] + qualities["b"]) * (.5 + (isolationutility["a"] - isolationutility["b"])))
        # cf formule (2)
        self.consumption["b"] = -self.consumption["a"]


class Network:
    """ Un reseau de players, capables d'interagir

    Offre les methodes utility pour calculer l'utilite d'un joueur
                       display pour visualiser le graphe
                       step pour que tous les joueurs s'optimisent"""

    def __init__(self, players, qualities, isolationutility):
        self.size = len(players)
        self.players = players  # joueurs
        self.qualities = qualities  # dictionnaire des qualites de "a" et de "b"
        # dictionnaire des coefficients dans la formule d'utilite en isolation
        self.isolationutility = isolationutility
        if isolationutility["a"] < isolationutility["b"]:
            raise Exception(
                "b plus grand que a dans la formule d'utilite en isolation")
        if isolationutility["a"] + 1 > 2 * isolationutility["b"]:
            raise Exception(
                "2b plus petit que 1+a dans la formule d'utilite en isolation")
        self.isol = lambda x: (qualities["a"] + qualities["b"]) * (isolationutility["a"] / 2 - isolationutility["b"] * (
            1 / 4 + x**2)) + (qualities["a"] - qualities["b"]) * (isolationutility["a"] - isolationutility["b"]) * x

        # graphe de relations entre les n personnes
        self.graph = [[0 for _ in list(range(self.size))]
                      for _ in list(range(self.size))]
        for i in range(self.size):
            for j in range(self.size):
                if j != i:
                    self.graph[i][j] = random.randint(0, 1000)
            surplus = sum(self.graph[i])
            if surplus != 0:
                for j in range(self.size):
                    self.graph[i][j] = round(
                        self.graph[i][j] / (surplus), 4)

    def utility(self, playerid):
        """Permet de calculer l'utilite obtenue par un joueur

        Prend en argument playerid, son indice dans Network.players"""
        total = 0
        thisplayer = self.players[playerid]
        for k, other in enumerate(self.players):
            if k != playerid:
                total += self.qualities["a"] * (.5 + thisplayer.consumption["a"]) * (.5 + other.consumption[
                    "a"]) + self.qualities["b"] * (.5 + thisplayer.consumption["b"]) * (.5 + other.consumption["b"])
            else:
                total += self.isol(thisplayer.consumption["a"])
        return total

    def display(self):
        """Affiche un pyplot du Network, ainsi que les moyennes de consommation en a et b"""
        graph = nx.Graph()
        for k in list(range(self.size)):
            graph.add_node(k, pay=self.utility(k))
        for i in range(self.size):
            for j in range(i):
                graph.add_edge(i, j, strength=(
                    self.graph[i][j] + self.graph[j][i]) / 2)

        nx.draw_circular(graph,
                         with_labels=True,
                         node_size=[1500 / self.size * graph.node[k]['pay']
                                    for k in graph.nodes()],
                         node_color=[player.consumption[
                             "a"] + .5 for player in self.players],
                         cmap=mtpl.cm.get_cmap(name="winter"),
                         vmin=0,
                         vmax=1,
                         edge_color=[1 / (1 + math.exp(-7 * ((self.size) * graph.edge[k[0]][k[1]]['strength'] - 1)))
                                     for k in graph.edges()],
                         edge_cmap=mtpl.cm.get_cmap(name="Greys"),
                         edge_vmin=0,
                         edge_vmax=1,
                         linewidths=0.3,
                         width=20 / self.size)
        avega = sum([player.consumption["a"]
                     for player in self.players]) / self.size
        avegb = sum([player.consumption["b"]
                     for player in self.players]) / self.size
        plt.text(-1.5, 1.3, "{'a':" + str(round(avega, 2)) +
                 ", 'b':" + str(round(avegb, 2)) + "}")
        plt.show()

    def step(self):
        """Fait evoluer chaque joueur en le faisant executer son .optimize() avec l'etat actual du jeu"""
        curstate = []
        for i, player in enumerate(self.players):
            curstate.append([{"consumption": other.consumption["a"], "influence": self.graph[
                i][j]} for j, other in enumerate(self.players)])
        for i, player in enumerate(self.players):
            player.optimize(curstate[i], self.isolationutility, self.qualities)
