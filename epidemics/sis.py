''' Illustre un comportement typique d'une épidémie dans un réseau de type SIS.

Introduit la fonction plot pour tracer un graphe de modèle SIS.'''

import random as rand
import networkx as nx
import matplotlib.pyplot
import matplotlib as mtpl

def plot(n=30, d=3, p=0.1, turns=30, density=0.2, graph=None, verbose=False):
	'''Trace le graphe du modèle SIS après un nombre de tours défini.

		n (int): nombre de personnes
		d (int): duration de l'infection en tours
		p (float): probabilité d'infection
		turns (int): nombre de tours à simuler
		density (float): probabilité que deux noeuds soient connectés
		graph (nx.Graph): un éventuel graphe imposé
		verbose (bool): si l'on doit afficher les événements'''

	if graph is None:
		people = list(range(n))
		graph = nx.DiGraph()

		# state = 0=S et 1=I, age = nombre de tours infecté, infections = nombre de cycle d'infection
		graph.add_nodes_from(people, state=0, age=0, infections=0)

		# Creation de connections aléatoires
		for i in people:
			for j in people:
				# La variable density donne la probabilité d'existence de liens
				if i != j and rand.random() < density:
					# color = 0 neutre, 1 tentative d'infection, 2 infection transmise
					# vector = 0.01 simple connection, 0.05 si essai de transmission,  1 sinon: sert dans l'affichage en ressorts
					graph.add_edge(i, j, color=0, vector=0.01)
	else:
		# On initialise le nombre de personnes
		n = graph.number_of_nodes()

		# On initialise les attributs nécessaires
		for node in graph.nodes(data=True):
			node[1]['state'] = 0
			node[1]['age'] = 0
			node[1]['infections'] = 0
		for edge in graph.edges(data=True):
			edge[2]['color'] = 0
			edge[2]['vector'] = 0.01

	# On infecte un patient zero en on l'affiche
	graph.node[rand.randint(0, n - 1)]['state'] = 1
	if verbose:
		print("z -", [t[0] for t in graph.nodes(data=True) if t[1]['state']][0])

	# On retient le nombre d'infectés à chaque tour
	infected = [1]

	for m in range(turns):
		# Afin d'éviter de faire une boucle de comptage, on compte les infectés au fur et à mesure
		counter = 0
		# Evite de traiter les patients infectés le tour meme: on filtre dès le début
		for node in [k for k in graph.nodes(data=True) if k[1]['state'] == 1]:
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
							graph.edge[node[0]][other]['color'] = 2
							graph.edge[node[0]][other]['vector'] = 1
							if verbose:
								print(m, "-", node[0], "i", other)
						else:
							graph.edge[node[0]][other]['color'] = 1
							graph.edge[node[0]][other]['vector'] = 0.05
							if verbose:
								print(m, "-", node[0], "t", other)
			else:
				# En fin de compte, il n'est pas infecté
				counter -= 1

				# Remise à zero des statistiques
				node[1]['state'] = 0
				node[1]['age'] = 0
				if verbose:
					print(m, "-", node[0], "r")
		# On enregistre succesivement les valeurs pour les tracer plus tard
		infected.append(counter)

	mtpl.pyplot.figure(num=1, figsize=(15, 6))
	mtpl.pyplot.subplot(1, 2, 1)

	nx.draw_networkx(
				graph,
				pos=nx.spring_layout(graph, weight='vector', pos=nx.circular_layout(graph)),
				with_labels=verbose,
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
				width=0.1)

	mtpl.pyplot.title("Etat final du réseau")
	mtpl.pyplot.plot(-1, -1, marker='o', color=(240/255, 249/255, 33/255))
	mtpl.pyplot.plot(-1, -1.2, marker='o', color=(204/255, 71/255, 120/255))
	mtpl.pyplot.text(-.95, -1.03, "Susceptible", fontsize=9)
	mtpl.pyplot.text(-.95, -1.23, "Infecté", fontsize=9)

	mtpl.pyplot.subplot(1, 2, 2)
	mtpl.pyplot.title("Infectés en fonction du tour")
	mtpl.pyplot.xlabel("Tour")
	mtpl.pyplot.grid()
	mtpl.pyplot.bar(list(range(turns + 1)), infected, color=(204/255, 71/255, 120/255))

	mtpl.pyplot.show()

if __name__ == "__main__":
	plot()
