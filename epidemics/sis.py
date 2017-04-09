''' Illustre un comportement typique d'une épidémie dans un réseau de type SIS. '''

import random as rand
import networkx as nx
import matplotlib.pyplot
import matplotlib as mtpl

mtpl.pyplot.cla()

# n = nombre de personnes, d = duration de l'infection en tours, p = probabilite d'infection, turns = nombre de tours à simuler
n = 50
d = 300
p = 0.1
turns = 30

# On crée le graphe avec les personnes en question
people = list(range(n))
graph = nx.MultiDiGraph()
# state = 0=S et 1=I, age = nombre de tours infecté, infections = nombre de cycle d'infection
graph.add_nodes_from(people, state=0, age=0, infections=0)

# On infecte un patient zero en on l'affiche
graph.node[rand.randint(0, n - 1)]['state'] = 1
print("z -", [t[0] for t in graph.nodes(data=True) if t[1]['state']][0])
# la première infection ne compte pas comme une vraie infection dans les stats

# On retient le nombre d'infectés à chaque tour
infected = [1]

# Creation de connections aléatoires
for i in people:
    for j in people:
        # La probabilité 0.1 génère de jolis graphes, pas trop liés
        if i != j and rand.random() < .1:
            # color = 0 neutre, 1 tentative d'infection, 2 infection transmise
            graph.add_edge(i, j, color=0)

for m in range(turns):
    # Afin d'éviter de faire une boucle de comptage, on compte les infectés au fur et à mesure
    counter = 0
    for node in graph.nodes(data=True):
        # On ne s'interesse qu'aux patients infectés
        if node[1]['state'] == 1:
            counter += 1
            if node[1]['age'] < d:
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
                            graph.add_edge(node[0], other, color=2)

                            print(m, "-", node[0], "i", other)
                        else:
                            graph.add_edge(node[0], other, color=1)

                            print(m, "-", node[0], "t", other)
            else:
                # En fin de compte, il n'est pas infecté
                counter -= 1

                # Remise à zero des statistiques
                node[1]['state'] = 0
                node[1]['age'] = 0

                print(m, "-", node[0], "r")
    # On enregistre succesivement les valeurs pour les tracer plus tard
    infected.append(counter)

# On utilise les mêmes échelles de couleurs que les autres modèles
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

mtpl.pyplot.suptitle("Etat final du réseau")
mtpl.pyplot.plot(-1, -1, marker='o', color=(240/255, 249/255, 33/255))
mtpl.pyplot.plot(-1, -1.2, marker='o', color=(204/255, 71/255, 120/255))
mtpl.pyplot.text(-.95, -1.04, "Susceptible", fontsize=9)
mtpl.pyplot.text(-.95, -1.24, "Infecté", fontsize=9)

mtpl.pyplot.figure(2)
mtpl.pyplot.suptitle("Infectés en fonction du tour")
mtpl.pyplot.xlabel("Tour")
mtpl.pyplot.grid()
mtpl.pyplot.bar(list(range(turns + 1)), infected)

mtpl.pyplot.show()
