'''Permet de visualiser pour un secteur donné les répartitions.

Introduit la fonction plot qui trace cette répartition.'''

import seaborn as sb
import numpy as np
import matplotlib as mtpl
import matplotlib.pyplot as plt
if __name__ == "__main__":
    from interface import Secteur, MAP, TIMES
else:
    from .interface import Secteur, MAP, TIMES

def plot(secteur):
    # Permet d'avoir des étiquettes raisonnables dans le graphe final
    map_labels = ["101", "", "", "", "", "", "", "", "", "110", "", "", "", "", "", "", "", "",
                  "", "120", "", "", "", "", "", "", "", "", "", "130", "", "", "", "", "", "",
                  "", "", "", "140", "", "", "", "201", "", "", "", "", "301", "", "", "", "",
                  "", "", "", "", "310", "", "", "", "", "401", "", "", "501", "", "", "", "",
                  "", "", "", "", "510", "", "", "", "", "", "", "", "", "", "601", "", "603",
                  "701", "801", "", "", "", "", "", "901", "", "", "990"]

    times_labels = ["00", "", "", "", "01", "", "", "", "02", "", "", "", "03", "", "", "", "04",
                    "", "", "", "05", "", "", "", "06", "", "", "", "07", "", "", "", "08", "",
                    "", "", "09", "", "", "", "10", "", "", "", "11", "", "", "", "12", "", "",
                    "", "13", "", "", "", "14", "", "", "", "15", "", "", "", "16", "", "", "",
                    "17", "", "", "", "18", "", "", "", "19", "", "", "", "20", "", "", "", "21",
                    "", "", "", "22", "", "", "", "23", "", "", "",]

    sect = Secteur(secteur)

    data = np.zeros((98, 96))
    dp = 1 / sect.nombre
    for person in sect:
        for heure, endroit in enumerate(person.positions):
            data[MAP.index(endroit)][heure] += dp

    data = np.ma.masked_equal(data, 0)
    data[MAP.index(secteur)].mask = np.ones(96, dtype=bool)

    plt.figure(num=1, figsize=(15, 6))
    with sb.axes_style('dark'):
        plt.subplot(1, 2, 1)

    plt.title(f"Répartition de la population du secteur {secteur}")
    sb.heatmap(np.ma.filled(data, 0), xticklabels=times_labels, yticklabels=map_labels,
               mask=data.mask, cmap=mtpl.cm.get_cmap(name="YlOrRd"))
    plt.yticks(rotation=0)
    plt.ylabel('Heure')
    plt.xlabel('Secteur')

    with sb.axes_style('darkgrid'):
        plt.subplot(1, 2, 2)

    plt.title(f"Proportion de la population du secteur {secteur} présente dans son secteur")
    plt.xlabel('Heure')
    plt.plot(TIMES, data.data[MAP.index(secteur)])

    plt.show()

if __name__ == "__main__":
    plot(102)
