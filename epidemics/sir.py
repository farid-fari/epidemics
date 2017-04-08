''' Illustre un comportement typique d'une épidémie dans un réseau de type SIR. '''

import random as rand
import networkx as nx
import matplotlib.pyplot
import matplotlib as mtpl

mtpl.pyplot.cla()

# n = nombre de personnes, d = duration de l'infection en tours, p = probabilite d'infection, turns = nombre de tours à simuler
n = 50
d = 3
p = 0.1
turns = 50

people = list(range(n))
graph = nx.MultiDiGraph()
# state = 0=S et 1=I, age = nombre de tours infecté
graph.add_nodes_from(people, state=0, age=0)

# On infecte un patient zero en on l'affiche
graph.node[rand.randint(0, n - 1)]['state'] = 1
print("z", [t[0] for t in graph.nodes(data=True) if t[1]['state']][0])
# Pour le tracage du graphe des infectés et retirés
infected = [1]
removed = [0]

for i in people:
    for j in people:
        if i != j and rand.random() < .1:
            # color = 0 neutre, 1 tentative d'infection, 2 infection transmise
            graph.add_edge(i, j, color=0)

for m in range(turns):
    # On compte dynamiquement les infectés et retirés afin de ne pas multiplier les boucles
    counter = 0
    # On accumule les retirés
    remcounter = removed[-1]
    for node in graph.nodes(data=True):
        if node[1]['state'] == 1:
            counter += 1
            if node[1]['age'] < d:
                node[1]['age'] += 1
                for other in graph[node[0]]:
                    if not graph.node[other]['state']:
                        if rand.random() < p:
                            # On enregistre les informations comme étant infecté
                            graph.node[other]['state'] = 1
                            graph.edge[node[0]][other][0]['color'] = 2
                            # On compte le nouvel infecté
                            counter += 1

                            print(m, node[0], "i", other)
                        else:
                            graph.edge[node[0]][other][0]['color'] = 1
                            print(m, node[0], "t", other)
            else:
                # On l'a compté en trop
                counter -= 1
                remcounter += 1
                node[1]['state'] = 2
                print(m, node[0], "d")
    # On enregistre ce qu'on a compté
    infected.append(counter)
    removed.append(remcounter)

nx.draw_shell(
    graph,
    arrows=False,
    node_color=[1 - k[1]['state'] for k in graph.nodes(data=True)],
    cmap=mtpl.cm.get_cmap(name="plasma"),
    vmin=0,
    vmax=1,
    edge_color=[t[2]['color'] for t in graph.edges(data=True)],
    edge_cmap=mtpl.cm.get_cmap(name="YlOrRd"),
    edge_vmin=0,
    edge_vmax=2,
    linewidths=0.2,
    width=10 / n)

mtpl.pyplot.suptitle("Etat final du réseau")

# Seconde figure pour les infectés et retirés
mtpl.pyplot.figure(2)
mtpl.pyplot.suptitle("Infectés en fonction du tour")
mtpl.pyplot.xlabel("Tour")
mtpl.pyplot.grid()
mtpl.pyplot.bar(list(range(turns + 1)), infected, color='b')
mtpl.pyplot.bar(list(range(turns + 1)), removed, color='r')

mtpl.pyplot.show()
