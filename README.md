# Epidemics

Etude de réseaux aléatoires selon les modèles d'arbre, `SIR`, `SIS` et `SIRS`. Permet d'avoir la représentation graphique de l'état du réseau après un nombre fini de tours.

Inspiré de [*Networks, Crowds and Markets*](https://www.cs.cornell.edu/home/kleinber/networks-book/) de **David Easley** et **Jon Kleinberg**.

## Exemple

Exemple de résultat obtenu avec `sir.py` pour paramètres `n=60, d=3, p=0.2, turns=10, density=0.1`:

![example](epidemics/example_SIR.png?raw=true)

# Social

Une librairie permettant l'étude d'un réseau de participants consommant deux produits et interagissant en s'influencant réciproquement.

Introduit les classes `Network` et `Player`.

Basé sur [Competitive Diffusion in Social Networks: Quality or Seeding?](https://arxiv.org/pdf/1503.01220.pdf)

# Dépendances

Le code est écrit pour **Python 3.6**. Il est nécessaire d'installer les librairies `networkx`, `matplotlib` et `scipy` afin de pouvoir éxecuter les scripts Python.