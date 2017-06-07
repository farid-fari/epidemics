''' Compare l'entropie calculée au nombre d'infectés. '''

from math import log
from scipy.special import binom
import matplotlib.pyplot as plt
from sirs import Sirs

s = Sirs(n=200, p=0.05, graph=0.1)
x = list(range(1, 200))
y = []
for _ in x:
    # Valeur théorique de l'entropie du système
    y.append(log(binom(s.n, s.infected[-1])))
    s.increment()

plt.plot(x, y, 'y')
plt.show()
