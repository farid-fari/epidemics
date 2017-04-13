''' Illustre les oscillations possibles dans certains réseaux avec le modèle SIRS.

Prend pour arguments sur ligne de commande:
    n (int): nombre de personnes
    d[0] (int): duration de l'infection en tours
    d[1] (int): duration de l'immunité en tours
    p (int): probabilité d'infection
    turns (int): nombre de tours à simuler
    density (int): probabilité que deux noeuds soient connectés'''

import sys
import random as rand
import networkx as nx
import matplotlib.pyplot
import matplotlib as mtpl

mtpl.pyplot.cla()

# n = nombre de personnes, d = duration de l'infection et de l'inactivite, p = probabilite d'infection, turns = nombre de tours à simuler
n = 100
d = [4, 2]
p = 0.05
turns = 100
density = 0.1
if len(sys.argv) >= 2:
    n = int(sys.argv[1])
if len(sys.argv) >= 3:
    d = int(sys.argv[2])
if len(sys.argv) >= 4:
    d = int(sys.argv[3])
if len(sys.argv) >= 5:
    p = float(sys.argv[4])
if len(sys.argv) >= 6:
    turns = int(sys.argv[5])
if len(sys.argv) >= 7:
    density = float(sys.argv[6])

# On crée le graphe avec les personnes en question
people = list(range(n))
graph = nx.MultiDiGraph()
# state = 0=S, 1=I, 2=R, age = nombre de tours infecte, infections = nombre de cycle d'infection
graph.add_nodes_from(people, state=0, age=0, infections=0)

# On infecte un patient zero en on l'affiche
graph.node[rand.randint(0, n - 1)]['state'] = 1
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
    for node in graph.nodes(data=True):
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

                            print(m, node[0], "i", other)
                        else:
                            graph.edge[node[0]][other][0]['color'] = 1

                            print(m, node[0], "t", other)
            else:
                # En fin de compte, il n'est pas infecté, mais retiré
                counter -= 1
                remcounter += 1

                # Passage en mode retiré
                node[1]['state'] = 2
                node[1]['age'] = 0

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

nx.draw_shell(
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
    width=10 / n)

matplotlib.pyplot.suptitle("Etat final du réseau")
mtpl.pyplot.plot(-1, -1, marker='o', color=(240/255, 249/255, 33/255))
mtpl.pyplot.plot(-1, -1.2, marker='o', color=(204/255, 71/255, 120/255))
mtpl.pyplot.plot(-1, -1.4, marker='o', color=(13/255, 8/255, 135/255))
mtpl.pyplot.text(-.95, -1.04, "Susceptible", fontsize=9)
mtpl.pyplot.text(-.95, -1.24, "Infecté", fontsize=9)
mtpl.pyplot.text(-.95, -1.44, "Retiré", fontsize=9)

mtpl.pyplot.figure(2)
mtpl.pyplot.suptitle("Infectés et retirés en fonction du tour")
mtpl.pyplot.xlabel("Tour")
mtpl.pyplot.grid()
mtpl.pyplot.bar(list(range(turns + 1)), infected, color='b')
mtpl.pyplot.bar(list(range(turns + 1)), removed, color='r')

mtpl.pyplot.show()