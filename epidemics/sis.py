import random as rand
import networkx as nx
import matplotlib.pyplot
import matplotlib as mtpl
import scipy
import threading

mtpl.pyplot.cla()

n = 100
d = 3

people = list(range(n))

probas = scipy.linspace(0,1,1000)
y = [0 for _ in range(1000)]

def compute(i, p):
    global y
    sumoftries = 0
    for _ in range(100):
        graph = nx.MultiDiGraph()
        graph.add_nodes_from(people, state=0, age=0, infections=0)        
        graph.node[rand.randint(0, n - 1)]['state'] = 1
        connections = [[0 for _ in people] for _ in people]        
        for i in people:
            for j in people:
                if i != j and rand.random() < .1:
                    connections[i][j] = 1
                    graph.add_edge(i, j, color=0)
        
        for m in range(300):
            for node in graph.nodes(data=True):
                if node[1]['state'] == 1:
                    if node[1]['age'] < d:
                        node[1]['age'] += 1
                        for other in graph[node[0]]:
                            if not graph.node[other]['state']:
                                if rand.random() < p:
                                    graph.node[other]['state'] = 1
                                    graph.node[other]['infections'] += 1
                    else:
                        node[1]['state'] = 0
                        node[1]['age'] = 0

        sumoftries += sum([k[1]['infections'] for k in graph.nodes(data=True)])/300
    y[i] = sumoftries/100/n
    print(p, y[i])

threads = []
for i in range(1000):
    while len(threads) >= 4:
        for th in threads:
            if not th.is_alive():
                threads.remove(th)
    t = threading.Thread(target=compute, args=(i, probas[i]))
    threads.append(t)
    t.start()

deriv = [0] + [y[i+1]-y[i-1] for i in range(1,999)] + [0]

mtpl.pyplot.plot(probas, y, color='r')
mtpl.pyplot.plot(probas, deriv, color='g')
mtpl.pyplot.grid()
mtpl.pyplot.show()
