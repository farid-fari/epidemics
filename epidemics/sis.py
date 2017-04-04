import random as rand
import networkx as nx
import matplotlib.pyplot
import matplotlib as mtpl

mtpl.pyplot.cla()

n = 50
d = 3
p = 0.1

people = list(range(n))

graph = nx.MultiDiGraph()

graph.add_nodes_from(people, state=0, age=0, infections=0)

graph.node[rand.randint(0, n - 1)]['state'] = 1

# On affiche le patient zero
print("z", [t[0] for t in graph.nodes(data=True) if t[1]['state']][0])

# Creation de connections aléatoires
for i in people:
    for j in people:
        if i != j and rand.random() < .1:
            graph.add_edge(i, j, color=0)

for m in range(30):
    for node in graph.nodes(data=True):
        # On ne s'interesse qu'aux patients infectés
        if node[1]['state'] == 1:
            if node[1]['age'] < d:
                node[1]['age'] += 1
                for other in graph[node[0]]:
                    if not graph.node[other]['state']:
                        if rand.random() < p:
                            graph.node[other]['state'] = 1
                            graph.node[other]['infections'] += 1
                            graph.add_edge(node[0], other, color=2)
                            print(m, node[0], "t", other)
                        else:
                            graph.add_edge(node[0], other, color=1)
                            print(m, node[0], "m", other)
            else:
                node[1]['state'] = 0
                node[1]['age'] = 0
                print(m, node[0], "r")

nx.draw_shell(
    graph,
    arrows=False,
    node_color=[k[1]['state'] for k in graph.nodes(data=True)],
    cmap=mtpl.cm.get_cmap(name="cool"),
    vmin=0,
    vmax=2,
    edge_color=[t[2]['color'] for t in graph.edges(data=True)],
    edge_cmap=mtpl.cm.get_cmap(name="hsv"),
    edge_vmin=0,
    edge_vmax=2,
    with_labels=True,
    linewidths=0.2,
    width=10 / n)

mtpl.pyplot.show()
