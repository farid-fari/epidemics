'''Illustre le modèle d'un arbre de propagation d'une épidémie.

Introduit la fonction plot pour tracer l'arbre pour un nombre défini de tours.'''

import random as rand
import networkx as nx
import matplotlib.pyplot
import matplotlib as mtpl

def plot(n=7, p=0.5, k=2, verbose=False):
	'''Trace le graphe du modèle d'arbres dans une population.

		n (int): nombre de tours
		p (float): probabilité d'infection
		k (int): nombre d'intéractions pour une personne donnée
		verbose (bool): si l'on doit afficher les événements'''

	if verbose:
		print("r0 =", p*k)

	if k**n >= 175:
		print("Vous allez générer", k**n - 1, "nodes, cela risque d'être long...")

	people = list(range(int((k**n - 1)/(k - 1))))
	# Ici, un simple graph suffira, puisque les connections sont simples
	graph = nx.Graph()
	graph.add_nodes_from(people, state=0)
	graph.node[0]['state'] = 1

	# On propage pour chaque prochaine couche sauf la dernière
	for m in range(n-1):
		nextitems = int((k**(m+1) - 1)/(k-1))
		# Pour chaque élément de la couche
		for i in range(int((k**m - 1)/(k-1)), int((k**(m+1) - 1)/(k-1))):
			if graph.node[i]['state']:
				for plus in range(k):
					if rand.random() < p:
						graph.node[nextitems + plus]['state'] = 1
						graph.add_edge(i, nextitems + plus)
			nextitems += k

	mtpl.pyplot.figure(num=1, figsize=(15, 6))
	nx.draw_networkx(graph,
					 pos=_tree_layout(n, k),
					 node_color=[2 - k[1]['state'] for k in graph.nodes(data=True)],
					 cmap=mtpl.cm.get_cmap(name="plasma"),
					 vmin=0,
					 vmax=2,
					 edge_color='r',
					 linewidths=0.2,
					 width=0.7,
					 with_labels=(k**(n-1) <= 30))

	mtpl.pyplot.title("Etat final du réseau")
	mtpl.pyplot.plot(-1, -1, marker='o', color=(240/255, 249/255, 33/255))
	mtpl.pyplot.plot(-1, -1.2, marker='o', color=(204/255, 71/255, 120/255))
	mtpl.pyplot.text(-.95, -1.03, "Susceptible", fontsize=9)
	mtpl.pyplot.text(-.95, -1.23, "Infecté", fontsize=9)
	mtpl.pyplot.text(-1, -.9, "R0 = "+str(p*k))

	mtpl.pyplot.show()

def _tree_layout(n, k):
	pos = []
	# les x vont de -1 à 1
	x = -1
	dx = 2 / n
	for m in list(range(n)):
		# les y vont de -1 à 1
		y = -1
		dy = 2 / (k**m)
		for _ in range(k**m):
			pos.append((x, y + dy / 2))
			y += dy
		x += dx
	return pos

if __name__ == "__main__":
	plot()
