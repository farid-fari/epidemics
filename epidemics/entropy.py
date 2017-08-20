''' Compare l'entropie calculée au nombre d'infectés. '''

from math import log
from scipy.special import binom
import matplotlib.pyplot as plt
from sirs import Sirs

s = Sirs(d=[40, 20], p=0.01)
s.increment_avg(200, 800)
# Valeur théorique de l'entropie du système
y = [log(binom(s.n, i)) for i in s.infected]
plt.figure(num=2)
plt.plot(list(range(len(y))), y, 'y')
plt.title(f'Entropie en fonction du tour (n={s.n}, p={s.p}, t={s.turn-1})')
s.plot()
