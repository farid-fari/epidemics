import random as rand
import networkx as nx
import matplotlib.pyplot
import matplotlib as mtpl

mtpl.pyplot.cla()

n = 100
k = 30
p = 0.033
print("r0 =", p*k)

people = list(range(n))

sick = [0]*n
full = [1]*n
sick[rand.randint(0, n-1)] = 1

graph = nx.Graph()
graph.add_nodes_from(people)

previous = [p for p in people if sick[p]]

u = []

for m in range(10):
    next_wave = []
    u.append(len(previous))
    for i in previous:
        j = 0
        while j < k:
            if sick == full:
                j = k
            t = rand.randint(0, n-1)
            if not sick[t]:
                j += 1
                if rand.random() < p:
                    graph.add_edge(i, t, trans=1)
                    sick[t] = 1
                    next_wave.append(t)
                else:
                    graph.add_edge(i, t, trans=0)
    previous = next_wave

nx.draw_circular(graph,
                 node_color=sick,
                 cmap=mtpl.cm.get_cmap(name="autumn"),
                 vmin=0,
                 vmax=1,
                 with_labels=True,
                 edge_color=[1-graph.edge[t[0]][t[1]]['trans'] for t in graph.edges()],
                 edge_cmap=mtpl.cm.get_cmap(name="winter"),
                 edge_vmin=0,
                 edge_vmax=1,
                 linewidths=0.2,
                 width=80/n)

mtpl.pyplot.show()

print("infected: ", u, "\ntotal: ", sum(u), sep="")
