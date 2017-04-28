''' Construit la matrice de transition d'un état à un autre. '''

import sqlite3 as sq
import numpy as np
from interface import Secteur, MAP, TIMES

def passage(t, sect):
    '''Rend M(t+1|t) pour un secteur donné.

    t (int): le temps initial
    sect (int): le secteur en question

    return: M(t+1|t) (np.ndarray)'''
    conn = sq.connect('trajecto_nouv.db')
    curs = conn.cursor()
    secteur = Secteur(curs, sect)

    try:
        ot = TIMES.index(t)
    except IndexError:
        raise IndexError('Temps inexistant.')

    m = np.zeros((98, 98))
    posinit = np.zeros(98)
    posfin = np.zeros(98)

    # Curseur auxiliaire
    for _, personne in secteur.people.items():
        depl = personne.positions[ot:ot+2]
        depl = [MAP.index(d) for d in depl]

        posinit[depl[0]] += 1
        posfin[depl[1]] += 1
        m[depl[1]][depl[0]] += 1

    for i in range(98):
        if posinit[i]:
            # On divise la colonne par le nombre de personnes y ayant contribué
            m[:, i] /= posinit[i]
    curs.close()
    conn.close()
    return m

if __name__ == "__main__":
    print(passage(0, 101))
