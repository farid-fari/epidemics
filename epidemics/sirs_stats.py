'''Construit un résultat moyen au modèle SIRS pour des paramètres donnés.

Introduit la fonction plot_avg pour tracer des statistiques moyennes sur un graphe.'''

import random as rand
import sqlite3 as sq
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sb

def plot_avg(n=60, d=[4, 2], p=0.05, turns=100, sample=600, graph=0.3, verbose=False):
    '''Trace un graphe moyen du modèle SIRS après un nombre défini de tours.

        n (int): nombre de personnes
        d[0] (int): duration de l'infection en tours
        d[1] (int): duration de l'immunité en tours
            s'il vaut 0, on aura un modèle SIS
            s'il est >= à turns, c'est un modèle SIR
        p (float): probabilité d'infection
        turns (int): nombre de tours à simuler
        graph (nx.Graph ou int ou float): un éventuel graphe imposé,
            ou bien une densité pour qu'un graphe soit généré
        verbose (bool): si l'on doit afficher les tours'''

    # On crée le tableau en mémoire puisqu'il est temporaire
    connection = sq.connect(':memory:')
    c = connection.cursor()
    c.execute('CREATE TABLE Statistics '
              '(SimId integer, Turn integer, Infected integer, Removed integer)')
    # La base de données permet le calcul rapide et efficace de moyennes sur
    # un grand nombre de tours et de graphes

    # On initialise le graphe aléatoire si nécessaire
    if isinstance(graph, float) and isinstance(graph, int):
        graph = nx.gnp_random_graph(n, graph, directed=True)

    n = graph.number_of_nodes() # Dans le cas ou on ne l'a pas donné

    # On initialise les attributs
    for node in graph.nodes(data=True):
        node[1]['state'] = 0
        node[1]['age'] = 0
    for edge in graph.edges(data=True):
        edge[2]['color'] = 0
        if edge[0] == edge[1]:
            graph.remove_edge(edge)
            # On retire les loopbacks

    # On infecte toujours le meme individu en premier
    graph.node[rand.randint(0, n - 1)]['state'] = 1

    # Voir sirs.py pour des commentaires détaillés
    for k in range(sample):
        if verbose:
            print(k)
        # Réinitialisation du graphe
        g = graph

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
                            if not g.node[other]['state'] and rand.random() < p:
                                g.node[other]['state'] = 1
                                g.node[other]['age'] = 0 # par sureté (non nécessaire)
                                # De plus, on le compte (inutile de recolorer l'edge)
                                counter += 1
                    else:
                        # En fin de compte, il n'est pas infecté, mais retiré/susceptible
                        counter -= 1

                        if d[1]:
                            # Passage en mode retiré
                            node[1]['state'] = 2
                            node[1]['age'] = 0
                            remcounter += 1
                        else:
                            # Passage en mode susceptible
                            node[1]['state'] = 0
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

    c.close()
    connection.close()

    plt.figure(num=1, figsize=(15, 6))
    mod = "SIS"
    if d[1]:
        mod = "SIRS"
    if d[1] >= turns:
        mod = "SIR"
    plt.suptitle(f"Résultats moyens du modèle {mod} sur {sample} itérations")

    with sb.axes_style('darkgrid'):
        plt.subplot(1, 2, 1)
    plt.title("Moyenne des infectés et retirés en fonction du tour")
    plt.xlabel("Tour")
    plt.bar(x, infected, color=(204/255, 71/255, 120/255))
    plt.bar(x, removed, color=(13/255, 8/255, 135/255))

    with sb.axes_style('darkgrid'):
        plt.subplot(1, 2, 2)
    # Nombre dérivé en fonction du nombre
    plt.title("Portrait de phase du nombre d'infectés moyen")
    plt.xlabel("Nombre d'infectés")
    plt.ylabel("Variation du nombre d'infectés")
    derivI = [0] + [infected[i] - infected[i-1] for i in range(1, len(infected))]
    plt.plot(infected, derivI, marker="o", color=(204/255, 71/255, 120/255, 0.6))
    if mod != "SIS":
        derivR = [0] + [removed[i] - removed[i-1] for i in range(1, len(removed))]
        plt.plot(removed, derivR, marker="o", color=(13/255, 8/255, 135/255, 0.6))

    plt.show()

if __name__ == "__main__":
    plot_avg(verbose=True)
