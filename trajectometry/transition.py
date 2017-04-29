''' Construit la matrice de transition d'un état à un autre. '''

import sqlite3 as sq
import numpy as np
from interface import Secteur, MAP, TIMES

def passage(sect, tf, ti=None, memo=None):
    '''Rend M(tf|ti) pour un secteur donné.

    tf (int): le temps final
    tf (int): le temps initial
    sect (int): le secteur en question

    memo (interface.Secteur): un secteur déjà chargé

    return: M(tf|ti) (np.ndarray)'''

    try:
        nt = TIMES.index(tf)
    except ValueError:
        # L'instant doit figurer sous la forme HHMM dans le tableau TIMES
        raise IndexError('Temps final inexistant.')
    try:
        if ti is None:
            if nt > 0:
                ot = nt - 1
            else:
                ot = len(TIMES) - 1
        else:
            ot = TIMES.index(ti)
    except ValueError:
        # L'instant doit figurer sous la forme HHMM dans le tableau TIMES
        raise IndexError('Temps initial inexistant.')

    # Temps ti+1
    if ot == len(TIMES) - 1:
        # On fait le tour car on a atteint la fin
        nextt = 0
    else:
        nextt = ot + 1
    print(TIMES[ot], TIMES[nextt])

    # Mémoisation: on ne charge le secteur que s'il n'a jamais été chargé
    if memo is None:
        conn = sq.connect('trajecto_nouv.db')
        curs = conn.cursor()
        secteur = Secteur(curs, sect)
        curs.close()
        conn.close()
    else:
        secteur = memo

    # On calculera d'abord M(ti+1|ti) ainsi que P(ti) et P(ti+1)
    m = np.zeros((98, 98))
    posinit = np.zeros(98)
    posfin = np.zeros(98)

    # Pour chaque personne on ajoute 1 aux bonnes cases
    for _, personne in secteur:
        depl = (personne.positions[ot], personne.positions[nextt])
        depl = [MAP.index(d) for d in depl]

        posinit[depl[0]] += 1
        posfin[depl[1]] += 1
        m[depl[1]][depl[0]] += 1

    for i in range(98):
        if posinit[i]:
            # On divise la colonne par le nombre de personnes y ayant contribué
            m[:, i] /= posinit[i]

    if nt - ot == 0:
        return np.identity(98), (posinit, posinit)
    if nt - ot == 1:
        return m, (posinit, posfin)
    else:
        x, (_, y) = passage(sect, TIMES[nt], TIMES[nextt], secteur)
        return np.dot(x, m), (posinit, y)

if __name__ == "__main__":
    # On affiche la matrice partielle pour du deboggage
    mt, (ini, fin) = passage(103, 2045, 2000)
    print(mt)
    # On vérifie la justesse
    print(np.array_equal(fin, np.dot(mt, ini)))