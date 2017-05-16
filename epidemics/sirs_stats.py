'''Construit un résultat moyen au modèle SIRS pour des paramètres donnés

Introduit la fonction plot_avg pour tracer des statistiques moyennes sur un graphe.'''

import random as rand
import sqlite3 as sq
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sb

def plot_avg(n=60, d=[4, 2], p=0.05, turns=100, density=0.3, sample=600, graph=None, verbose=False):
    '''Trace un graphe moyen du modèle SIRS après un nombre défini de tours.

        n (int): nombre de personnes
        d[0] (int): duration de l'infection en tours
        d[1] (int): duration de l'immunité en tours
        p (float): probabilité d'infection
        turns (int): nombre de tours à simuler
        graph (nx.Graph): un éventuel graphe imposé
        density (float): probabilité que deux noeuds soient connectés
        verbose (bool): si l'on doit afficher les tours'''

    # On crée le tableau en mémoire puisqu'il est temporaire
    connection = sq.connect(':memory:')
    c = connection.cursor()
    c.execute('CREATE TABLE Statistics '
              '(SimId integer, Turn integer, Infected integer, Removed integer)')
    # La base de données permet le calcul rapide et efficace de moyennes sur
    # un grand nombre de tours et de graphes

    # On initialise le nombre de personnes
    if not graph is None:
        n = graph.number_of_nodes()

    # Voir sirs.py pour des commentaires détaillés
    for k in list(range(sample)):
        if verbose:
            print(k)

        if graph is None:
            g = nx.gnp_random_graph(n, density, directed=True)
        else:
            g = graph

        # On initialise les attributs
        for node in g.nodes(data=True):
            node[1]['state'] = 0
            node[1]['age'] = 0
        for edge in g.edges(data=True):
            edge[2]['color'] = 0
            if edge[0] == edge[1]:
                g.remove_edge(edge)

        g.node[rand.randint(0, n - 1)]['state'] = 1
        # Plutot que de compter dans des tableaux, on ajoutera directement les chiffres à la BDD
        for m in range(turns):
            counter = 0
            remcounter = 0
            # Le nom k est déjà utilisé
            for node in [item for item in g.nodes(data=True) if item[1]['state'] >= 1]:
                if node[1]['state'] == 1:
                    counter += 1
                    if node[1]['age'] < d[0]:
                        node[1]['age'] += 1
                        for other in g[node[0]]:
                            if not g.node[other]['state']:
                                if rand.random() < p:
                                    g.node[other]['state'] = 1
                                    g.node[other]['age'] = 0 # par sureté (non nécessaire)
                                    # De plus, on le compte (inutile de recolorer l'edge)
                                    counter += 1
                    else:
                        # En fin de compte, il n'est pas infecté, mais retiré
                        counter -= 1
                        remcounter += 1

                        # Passage en mode retiré
                        node[1]['state'] = 2
                        node[1]['age'] = 0

                elif node[1]['state'] == 2:
                    if node[1]['age'] < d[1]:
                        # On ne compte que celles qu'on ne va pas retirer
                        remcounter += 1
                        node[1]['age'] += 1
                    else:
                        # Remise à zero des statistiques
                        node[1]['state'] = 0
                        node[1]['age'] = 0
            # On enregistre succesivement les valeurs
            c.execute('INSERT INTO Statistics VALUES(?, ?, ?, ?)', (k, m, counter, remcounter))
        if not k % 20:
            connection.commit()

    connection.commit() # Par sureté

    x = []
    infected = []
    removed = []

    # On veut tracer des moyennes par tour
    for k in c.execute('SELECT Turn, AVG(Infected), AVG(Removed) FROM Statistics GROUP BY Turn'):
        x.append(k[0])
        infected.append(k[1])
        removed.append(k[2])

    connection.close()

    plt.figure(num=1, figsize=(15, 6))
    plt.suptitle(f"Résultats moyens sur {sample} itérations")

    with sb.axes_style('darkgrid'):
        plt.subplot(1, 2, 1)
    plt.title("Moyenne des infectés et retirés en fonction du tour")
    plt.xlabel("Tour")
    plt.bar(x, infected, color=(204/255, 71/255, 120/255))
    plt.bar(x, removed, color=(13/255, 8/255, 135/255))

    with sb.axes_style('darkgrid'):
        plt.subplot(1, 2, 2)
    plt.title("Portrait de phase moyen du nombre d'infectés")
    plt.xlabel("Nombre d'infectés")
    plt.ylabel("Variation du nombre d'infectés")
    derivI = [0] + [infected[i] - infected[i-1] for i in range(1, len(infected))]
    plt.plot(infected, derivI, marker="o", color=(204/255, 71/255, 120/255))

    plt.show()

if __name__ == "__main__":
    plot_avg(verbose=True)
