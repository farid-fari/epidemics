''' Illustre les oscillations possibles dans certains réseaux avec le modèle SIRS.

Introduit la fonction plot pour tracer un réseau SIRS.'''

import random as rand
import networkx as nx
import matplotlib.pyplot
import matplotlib as mtpl

def plot(n=60, d=[4, 2], p=0.05, turns=200, density=0.3, verbose=False):
    '''Trace un graphe du modèle SIRS après un nombre défini de tours.

    n (int): nombre de personnes
    d[0] (int): duration de l'infection en tours
    d[1] (int): duration de l'immunité en tours
    p (int): probabilité d'infection
    turns (int): nombre de tours à simuler
    density (int): probabilité que deux noeuds soient connectés
    verbose (bool): si l'on doit afficher les événements'''

    people = list(range(n))
    graph = nx.MultiDiGraph()
    # state = 0=S, 1=I, 2=R, age = nombre de tours infecte, infections = nombre de cycle d'infection
    graph.add_nodes_from(people, state=0, age=0, infections=0)

    # On infecte un patient zero en on l'affiche
    graph.node[rand.randint(0, n - 1)]['state'] = 1
    if verbose:
        print("z", [t[0] for t in graph.nodes(data=True) if t[1]['state']][0])
    # la première infection ne compte pas comme une vraie infection dans les stats

    # On retient le nombre d'infectés et de retirés à chaque tour
    infected = [1]
    removed = [0]

    # Création de connections aléatoires
    for i in people:
        for j in people:
            # La probabilité 0.1 génère de jolis graphes, pas trop liés
            if i != j and rand.random() < density:
                # color = 0 neutre, 1 tentative d'infection, 2 infection transmise
                graph.add_edge(i, j, color=0)

    for m in range(turns):
        # Afin d'éviter de faire une boucle de comptage, on compte les infectés et retirés au fur et à mesure
        counter = 0
        remcounter = 0
        # Evite de traiter des patient infectés dès ce tour-ci
        for node in [k for k in graph.nodes(data=True) if k[1]['state'] >= 1]:
            # On ne s'interesse qu'aux patients infectés
            if node[1]['state'] == 1:
                counter += 1
                if node[1]['age'] < d[0]:
                    node[1]['age'] += 1
                    for other in graph[node[0]]:
                        # Si l'autre est dans l'état S
                        if not graph.node[other]['state']:
                            if rand.random() < p:
                                # On met les stats au mode infecté
                                graph.node[other]['state'] = 1
                                graph.node[other]['age'] = 0 # par sureté (non nécessaire)
                                graph.node[other]['infections'] += 1
                                # De plus, on le compte
                                counter += 1
                                # Pour la coloration
                                graph.edge[node[0]][other][0]['color'] = 2
                                if verbose:
                                    print(m, node[0], "i", other)
                            else:
                                graph.edge[node[0]][other][0]['color'] = 1
                                if verbose:
                                    print(m, node[0], "t", other)
                else:
                    # En fin de compte, il n'est pas infecté, mais retiré
                    counter -= 1
                    remcounter += 1

                    # Passage en mode retiré
                    node[1]['state'] = 2
                    node[1]['age'] = 0
                    if verbose:
                        print(m, node[0], "r")
            elif node[1]['state'] == 2:
                if node[1]['age'] < d[1]:
                    # On ne compte que celles qu'on ne va pas retirer
                    remcounter += 1
                    node[1]['age'] += 1
                else:
                    # Remise à zero des statistiques
                    node[1]['state'] = 0
                    node[1]['age'] = 0
        # On enregistre succesivement les valeurs pour les tracer plus tard
        infected.append(counter)
        removed.append(remcounter)

    mtpl.pyplot.cla()

    nx.draw_spring(
        graph,
        arrows=False,
        node_color=[2 - k[1]['state'] for k in graph.nodes(data=True)],
        cmap=mtpl.cm.get_cmap(name="plasma"),
        vmin=0,
        vmax=2,
        edge_color=[2 - t[2]['color'] for t in graph.edges(data=True)],
        edge_cmap=mtpl.cm.get_cmap(name="gray"),
        edge_vmin=0,
        edge_vmax=2.3,
        linewidths=0.2,
        width=10/n)

    matplotlib.pyplot.suptitle("Etat final du réseau")
    mtpl.pyplot.plot(-1, -1, marker='o', color=(240/255, 249/255, 33/255))
    mtpl.pyplot.plot(-1, -1.2, marker='o', color=(204/255, 71/255, 120/255))
    mtpl.pyplot.plot(-1, -1.4, marker='o', color=(13/255, 8/255, 135/255))
    mtpl.pyplot.text(-.95, -1.03, "Susceptible", fontsize=9)
    mtpl.pyplot.text(-.95, -1.23, "Infecté", fontsize=9)
    mtpl.pyplot.text(-.95, -1.43, "Retiré", fontsize=9)

    mtpl.pyplot.figure(2)
    mtpl.pyplot.suptitle("Infectés et retirés en fonction du tour")
    mtpl.pyplot.xlabel("Tour")
    mtpl.pyplot.grid()
    mtpl.pyplot.bar(list(range(turns + 1)), infected, color=(204/255, 71/255, 120/255))
    mtpl.pyplot.bar(list(range(turns + 1)), removed, color=(13/255, 8/255, 135/255))

    mtpl.pyplot.show()

if __name__ == "__main__":
    plot()
