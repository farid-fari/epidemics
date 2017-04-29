''' Permet de visualiser pour un secteur donné les répartitions. '''

import sqlite3 as sq
import seaborn as sb
import numpy as np
import matplotlib as mtpl
import matplotlib.pyplot as plt
from interface import Secteur, MAP, TIMES

secteur = 102

map_labels = ["101", "", "", "", "", "", "", "", "", "110", "", "", "", "", "", "", "", "", "", "120",
       "", "", "", "", "", "", "", "", "", "130", "", "", "", "", "", "", "", "", "", "140",
       "", "", "", "201", "", "", "", "", "301", "", "", "", "", "", "", "", "", "310", "", "",
       "", "", "401", "", "", "501", "", "", "", "", "", "", "", "", "510", "", "", "", "", "",
       "", "", "", "", "601", "", "603", "701", "801", "", "", "", "", "", "901", "", "", "990"]

times_labels = ["00", "", "", "", "01", "", "", "", "02", "", "", "", "03", "", "", "", "04", "", "", "", "05",
         "", "", "", "06", "", "", "", "07", "", "", "", "08", "", "", "", "09", "", "", "", "10",
         "", "", "", "11", "", "", "", "12", "", "", "", "13", "", "", "", "14",
         "", "", "", "15", "", "", "", "16", "", "", "", "17", "", "", "", "18", "", "", "",
         "19", "", "", "", "20", "", "", "", "21", "", "", "", "22", "", "", "",
         "23", "", "", "",]

conn = sq.connect('trajecto_nouv.db')
curs = conn.cursor()

sect = Secteur(curs, secteur)

data = np.zeros((98, 96))
dp = 1 / sect.nombre
for _, person in sect:
    for heure, endroit in enumerate(person.positions):
        data[MAP.index(endroit)][heure] += dp

data = np.ma.masked_equal(data, 0)
data[MAP.index(secteur)].mask = np.ones(96, dtype=bool)

plt.figure(num=1, figsize=(15, 6))
plt.subplot(1, 2, 1)

plt.title("Répartition de la population du secteur " + str(secteur))
sb.heatmap(np.ma.filled(data, 0), xticklabels=times_labels, yticklabels=map_labels, mask=data.mask, cmap=mtpl.cm.get_cmap(name="YlOrRd"))
plt.yticks(rotation=0)

plt.subplot(1, 2, 2)

plt.title("Proportion de la population du secteur " + str(secteur) + " présent dans son secteur")
plt.plot(TIMES, data.data[MAP.index(secteur)])

plt.show()

curs.close()
conn.close()
