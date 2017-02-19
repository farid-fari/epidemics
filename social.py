""" Introduit les classes necessaires a l'etude du marketing dans un reseau social

social.Player(initialstate) est un participant d'un Network
social.Network(players, qualities, isolationutility) est un reseau de participants, capables d'evoluer"""

import math
import random
import networkx as nx
import matplotlib.pyplot
import matplotlib as mtpl


class Player:
    """ Un participant dans un reseau social, et consommateur

    Methodes:
        optimize: optimise la consommation du joueur en fonction des informations donnees"""

    def __init__(self, initalstate):
        """Cree un participant en vue de l'insertion dans un Network

        Args:
            initialstate (float): la valeur initiale de la consommation en produit a"""
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
    """Un reseau de participants, capables d'interagir

    Methodes:
        utility: calcule l'utilite d'un joueur
        display: visualiser le graphe
        step: optimiser tous les joueurs"""

    def __init__(self, players, qualities, isolationutility, graph=None):
        """Cree un reseau de joueurs specifies avec des regles specifiees

        Args:
            players (list of Player): la liste des participants dans le Network
            qualities (dict of float): les qualites des produits a et b initiales
            isolationutility (dict of float): les coefficients dans la formule d'utilite en isolation
        """
        self.size = len(players)
        self.players = players  # joueurs
        self.qualities = qualities  # dictionnaire des qualites de "a" et de "b"
        # dictionnaire des coefficients dans la formule d'utilite en isolation
        self.isolationutility = isolationutility
        if isolationutility["a"] < isolationutility["b"]:
            raise Exception(
                "b plus grand que a dans la formule d'utilite en isolation")
            # Condition necessaire afin que le gain en isolation soit positif
        if isolationutility["a"] + 1 > 2 * isolationutility["b"]:
            raise Exception(
                "2b plus petit que 1+a dans la formule d'utilite en isolation")
            # Condition necessaire afin que l'ajustement donne une consommation
            # entre 0 et 1
        self.isol = lambda x: (qualities["a"] + qualities["b"]) * (isolationutility["a"] / 2 - isolationutility["b"] * (
            1 / 4 + x**2)) + (qualities["a"] - qualities["b"]) * (isolationutility["a"] - isolationutility["b"]) * x

        # Generation graphe de relations entre les n personnes
        if graph is None:
            self.graph = [[0 for _ in players]
                          for _ in players]
            for i in range(self.size):
                for j in range(self.size):
                    if j != i:
                        self.graph[i][j] = random.randint(0, 1000)
                surplus = sum(self.graph[i])
                if surplus != 0:
                    for j in range(self.size):
                        self.graph[i][j] = round(
                            self.graph[i][j] / (surplus), 4)
                        # ajuste la somme des influences pour qu'elle vaille 1
                        # avec une precision 10E-3
        else:
            self.graph = graph

    def utility(self, playerid):
        """Permet de calculer l'utilite obtenue par un joueur

        Args:
            playerid (int): indice d'un joueur dans Network.players"""
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
                         node_size=[100 / self.size * graph.node[k]['pay']
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
        avega = sum([player.consumption["a"] + .5
                     for player in self.players]) / self.size
        avegb = sum([player.consumption["b"] + .5
                     for player in self.players]) / self.size
        # Les moyennes sont calculees avec les xi pour donner une valeur
        # parlante
        mtpl.pyplot.text(-1.5, 1.3, "{'a':" + str(round(avega, 2)) +
                         ", 'b':" + str(round(avegb, 2)) + "}")
        mtpl.pyplot.show()

    def step(self):
        """Fait evoluer chaque joueur en executant son .optimize() dans l'etat actual du jeu"""
        curstate = []
        for i, player in enumerate(self.players):
            curstate.append([{"consumption": other.consumption["a"], "influence": self.graph[
                i][j]} for j, other in enumerate(self.players)])
        for i, player in enumerate(self.players):
            player.optimize(curstate[i], self.isolationutility, self.qualities)
            