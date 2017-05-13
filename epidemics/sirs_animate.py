''' Illustre les oscillations possibles dans certains réseaux avec le modèle SIRS.

Introduit la fonction plot pour tracer un réseau SIRS.'''

import random as rand
import networkx as nx
import matplotlib.pyplot
import matplotlib as mtpl

def plot(n=60, d=[4, 2], p=0.05, turns=100, density=0.3, graph=None):
    '''Trace un graphe du modèle SIRS après un nombre défini de tours.

        n (int): nombre de personnes
        d[0] (int): duration de l'infection en tours
        d[1] (int): duration de l'immunité en tours
        p (float): probabilité d'infection
        turns (int): nombre de tours à simuler
        density (float): probabilité que deux noeuds soient connectés
        graph (nx.Graph): un éventuel graphe imposé'''

    if graph is None:
        graph = nx.gnp_random_graph(n, density, directed=True)
    else:
        # On initialise le nombre de personnes
        n = graph.number_of_nodes()

    # On initialise les attributs
    for node in graph.nodes(data=True):
        # state = 0=S et 1=I, age = nombre de tours infecté
        node[1]['state'] = 0
        # age = nombre de tours infecté
        node[1]['age'] = 0
    for edge in graph.edges(data=True):
        # color = 0 neutre, 1 tentative d'infection, 2 infection transmise
        edge[2]['color'] = 0
        # vector = 0.01 simple connection, 0.05 si essai de transmission,  1 sinon: sert dans l'affichage en ressorts
        edge[2]['vector'] = 0.01

    # On infecte un patient zero en on l'affiche
    graph.node[rand.randint(0, n - 1)]['state'] = 1

    pos = nx.spring_layout(graph, weight='vector', pos=nx.circular_layout(graph))

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

                                # De plus, on le compte
                                counter += 1

                                # Pour la coloration
                                graph.edge[node[0]][other]['color'] = 2
                                # Servira de ressort dans le graphe
                                graph.edge[node[0]][other]['vector'] = 1
                            else:
                                graph.edge[node[0]][other]['color'] = 1
                                graph.edge[node[0]][other]['vector'] = 0.05
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

        mtpl.pyplot.cla()
        mtpl.pyplot.figure(num=1, figsize=(7, 6))

        nx.draw_networkx(
                    graph,
                    pos=pos,
                    with_labels=False,
                    arrows=False,
                    node_color=[2 - k[1]['state'] for k in graph.nodes(data=True)],
                    cmap=mtpl.cm.get_cmap(name="plasma"),
                    vmin=0,
                    vmax=2,
                    edge_color=[2 - t[2]['color'] for t in graph.edges(data=True)],
                    edge_cmap=mtpl.cm.get_cmap(name="gray"),
                    edge_vmin=0,
                    edge_vmax=2.3,
                    node_size=5000/n+200,
                    width=0.2)

        mtpl.pyplot.title(f"Etat final du réseau (t={m})")
        mtpl.pyplot.plot(-1, -1, marker='o', color=(240/255, 249/255, 33/255))
        mtpl.pyplot.plot(-1, -1.2, marker='o', color=(204/255, 71/255, 120/255))
        mtpl.pyplot.plot(-1, -1.4, marker='o', color=(13/255, 8/255, 135/255))
        mtpl.pyplot.text(-.95, -1.03, "Susceptible", fontsize=9)
        mtpl.pyplot.text(-.95, -1.23, "Infecté", fontsize=9)
        mtpl.pyplot.text(-.95, -1.43, "Retiré", fontsize=9)

        mtpl.pyplot.savefig(f"animate/{m}.png")
        print(m)

if __name__ == "__main__":
    plot()
