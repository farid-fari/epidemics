''' Permet de visionner les données génerées par sirs_stats.py '''

import sqlite3 as sq
import matplotlib.pyplot as plt

connection = sq.connect('sirs.db')
c = connection.cursor()

x = []
infected = []
removed = []
for k in c.execute('SELECT Turn,AVG(Infected),AVG(Removed) FROM Statistics GROUP BY Turn'):
    x.append(k[0])
    infected.append(k[1])
    removed.append(k[2])

plt.plot(x, infected, 'g')
plt.plot(x, removed, 'r')
plt.show()
