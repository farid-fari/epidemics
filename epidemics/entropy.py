''' Compare l'entropie calculée au nombre d'infectés. '''

from math import log
from scipy.special import binom
import matplotlib.pyplot as plt
from sirs import Sirs

s = Sirs()
s.increment_avg(100, 600)
# Valeur théorique de l'entropie du système
y = [log(binom(s.n, i)) for i in s.infected]
s.plot()
plt.plot(list(range(len(y))), y, 'y')
plt.title(f'Entropie en fonction du tour (n={s.n}, p={s.p}, t={s.turn})')
plt.show()
