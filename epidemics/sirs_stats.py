''' Construit une base de données de statistiques concernant le modèle SIRS '''

# Sera implementé dans une version future
#import threading
import random as rand
import sqlite3 as sq

import networkx as nx

connection = sq.connect('sirs.db')
c = connection.cursor()
c.execute('CREATE TABLE IF NOT EXISTS Statistics (SimId integer, Turn integer, Infected integer, Removed integer)')

# n = nombre de personnes, d = duration de l'infection et de l'inactivite, p = probabilite d'infection, turns = nombre de tours à simuler
# NE PAS CHANGER SANS REMETTRE LA BDD A ZERO
n = 100
d = [4, 2]
p = 0.1
# On peut changer cependant turns, puisque la BDD enregistre le tour
turns = 200

# Voir sirs.py pour le reste des commentaires)
people = list(range(n))
# Le programme tourne indéfiniment jusqu'à être interrompu
for k in list(range(1000)):
    # On utilise un try afin de pouvoir interrompre le programme avec un KeyboardInterrupt
    try:
        nextid = c.execute('SELECT MAX(SimId) FROM Statistics').fetchone()[0]
        if nextid is None:
            nextid = 0
        else:
            nextid = nextid + 1
        print(k, nextid)

        graph = nx.MultiDiGraph()
        # Inutile ici de gérer le nombre d'infections par patient
        graph.add_nodes_from(people, state=0, age=0)
        graph.node[rand.randint(0, n - 1)]['state'] = 1
        # Plutot que de compter dans des tableaux, on ajoutera directement les chiffres à la BDD

        for i in people:
            for j in people:
                if i != j and rand.random() < .1:
                    # Inutile de gérer les couleurs
                    graph.add_edge(i, j)

        for m in range(turns):

            counter = 0
            remcounter = 0

            for node in graph.nodes(data=True):
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
            c.execute('INSERT INTO Statistics VALUES(?, ?, ?, ?)', (nextid, m, counter, remcounter))
        if not k % 10:
            connection.commit()
    except KeyboardInterrupt:
        print("cancelled")
        connection.commit()
        connection.close()
        exit()

print('done')
connection.commit()
connection.close()
# Voir query.sql pour avoir une idée des visualisations intéressantes à en tirer
