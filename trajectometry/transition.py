# -*- coding: UTF-8 -*-
'''Construit la matrice de transition d'un état à un autre.

Introduit la fonction passage pour calculer cette matrice.'''

import numpy as np
if __name__ == "__main__":
    from interface import Secteur, MAP, TIMES
else:
    from .interface import Secteur, MAP, TIMES

def passage(sect, tf, ti=None, memo=None, verbose=False):
    '''Rend M(tf|ti) pour un secteur donné.

    tf (int): le temps final
    tf (int): le temps initial
    sect (int): le secteur en question
    memo (interface.Secteur): un secteur déjà chargé
    verbose (bool): si l'on doit afficher les temps chargés

    return: M(tf|ti) (np.ndarray), (P(ti), P(tf)) (np.ndarray array)'''

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
    # On affiche les temps
    if verbose:
        print(TIMES[ot], "->", TIMES[nextt])

    # Mémoisation: on ne charge le secteur que s'il n'a jamais été chargé
    if memo is None:
        secteur = Secteur(sect)
    else:
        secteur = memo

    # On calculera d'abord M(ti+1|ti) ainsi que P(ti) et P(ti+1)
    m = np.zeros((98, 98))
    posinit = np.zeros(98)
    posfin = np.zeros(98)

    # Pour chaque personne on ajoute 1 aux bonnes cases
    for personne in secteur:
        depl = (personne.positions[ot], personne.positions[nextt])
        depl = [MAP.index(d) for d in depl]

        posinit[depl[0]] += 1
        posfin[depl[1]] += 1
        m[depl[1]][depl[0]] += 1

    for i in range(98):
        if posinit[i]:
            # On divise la colonne par le nombre de personnes y ayant contribué
            m[:, i] /= posinit[i]

    # On procède par récurrence
    if nt - ot == 0:
        return np.identity(98), (posinit, posinit)
    if nt - ot == 1:
        return m, (posinit, posfin)
    # else
    x, (_, y) = passage(sect, TIMES[nt], TIMES[nextt], secteur, verbose=verbose)
    return np.dot(x, m), (posinit, y)

if __name__ == "__main__":
    # On affiche la matrice partielle pour du deboggage
    mt, (ini, fin) = passage(102, 2100, 2000, verbose=True)
    print(mt)
    # On vérifie la justesse
    print(np.allclose(fin, np.dot(mt, ini)))
