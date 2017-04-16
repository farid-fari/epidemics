'''Construit un résultat moyen au modèle SIRS pour des paramètres donnés

Introduit la fonction plot_avg pour tracer un graphe moyen'''

import random as rand
import sqlite3 as sq
import networkx as nx
import matplotlib.pyplot as plt
import jgraph


def plot_avg(n=100, d=[4, 2], p=0.05, turns=100, density=0.1, sample=600, verbose=False):
	'''Trace un graphe moyen du modèle SIRS après un nombre défini de tours.

		n (int): nombre de personnes
		d[0] (int): duration de l'infection en tours
		d[1] (int): duration de l'immunité en tours
		p (float): probabilité d'infection
		turns (int): nombre de tours à simuler
		density (float): probabilité que deux noeuds soient connectés'''

	# On crée le tableau en mémoire puisqu'il est temporaire
	connection = sq.connect(':memory:')
	c = connection.cursor()
	c.execute('CREATE TABLE Statistics (SimId integer, Turn integer, Infected integer, Removed integer)')
	# La base de données permet le calcul rapide et efficace de moyennes sur un grand nombre de tours et de graphes

	# n = nombre de personnes, d = duration de l'infection et de l'inactivite, p = probabilite d'infection, turns = nombre de tours à simuler

	# Voir sirs.py pour le reste des commentaires
	people = list(range(n))
	for k in list(range(sample)):
		if verbose:
			print(k)
		graph = nx.DiGraph()
		# Inutile ici de gérer le nombre d'infections par patient
		graph.add_nodes_from(people, state=0, age=0)
		graph.node[rand.randint(0, n - 1)]['state'] = 1
		# Plutot que de compter dans des tableaux, on ajoutera directement les chiffres à la BDD

		for i in people:
			for j in people:
				if i != j and rand.random() < density:
					# Inutile de gérer les couleurs
					graph.add_edge(i, j)

		for m in range(turns):
			counter = 0
			remcounter = 0
			# Le nom k est déjà utilisé
			for node in [item for item in graph.nodes(data=True) if item[1]['state'] >= 1]:
				if node[1]['state'] == 1:
					counter += 1
					if node[1]['age'] < d[0]:
						node[1]['age'] += 1
						for other in graph[node[0]]:
							if not graph.node[other]['state']:
								if rand.random() < p:
									graph.node[other]['state'] = 1
									graph.node[other]['age'] = 0 # par sureté (non nécessaire)
									# De plus, on le compte (inutile de recolorer l'edge)
									counter += 1
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
			# On enregistre succesivement les valeurs
			c.execute('INSERT INTO Statistics VALUES(?, ?, ?, ?)', (k, m, counter, remcounter))
		if not k % 20:
			connection.commit()

	connection.commit() # Par sureté

	x = []
	infected = []
	removed = []

	# On veut tracer des moyennes par tour
	for k in c.execute('SELECT Turn, AVG(Infected), AVG(Removed) FROM Statistics GROUP BY Turn'):
		x.append(k[0])
		infected.append(k[1])
		removed.append(k[2])

	connection.close()

	plt.figure(num=1, figsize=(15, 6))
	plt.suptitle("Moyenne des infectés et retirés en fonction du tour")
	plt.title(str(sample) + " itérations", style='italic')
	plt.xlabel("Tour")
	plt.grid()
	plt.bar(x, infected, color=(204/255, 71/255, 120/255))
	plt.bar(x, removed, color=(13/255, 8/255, 135/255))
	plt.show()

if __name__ == "__main__":
	plot_avg()
