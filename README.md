# Epidemics

Etude de réseaux aléatoires selon les modèles d'arbre, `SIR`, `SIS` et `SIRS`. Permet d'avoir la représentation graphique de l'état du réseau après un nombre fini de tours, ainsi qu'une animation.

Inspiré de [*Networks, Crowds and Markets*](https://www.cs.cornell.edu/home/kleinber/networks-book/) de **David Easley** et **Jon Kleinberg**.

## Exemple

Exemple de résultat obtenu avec `sirs.py` avec pour paramètres `n=60, d=[4, 2], p=0.05, turns=100, graph=0.3`:

![exemple](epidemics/example_SIR.png?raw=true)

# Trajectométrie

Une étude des déplacements dans l'objectif de faire une étude sur le comportement d'épidémies dans une population.

## Exemple

Exemple de résultat obtenu avec `repartition.py` pour paramètres `secteur=102`:

![exemple](trajectometry/example_traj.png?raw=true)

# Trajectométrie

Une étude des déplacements dans l'objectif de faire une étude sur le comportement d'épidémies dans une population.

# Social

Une librairie permettant l'étude d'un réseau de participants consommant deux produits et interagissant en s'influencant réciproquement.

Introduit les classes `Network` et `Player`.

Basé sur [Competitive Diffusion in Social Networks: Quality or Seeding?](https://arxiv.org/pdf/1503.01220.pdf)

# Dépendances

Le code est écrit pour **Python 3.6.1** (au moins **3.6** pour les literal string). Il est nécessaire d'installer les librairies `networkx`, `matplotlib`, `seaborn` et `numpy` afin de pouvoir éxecuter les scripts Python.

La partie trajectométrie requiert la présence de `trajecto.csv`, une liste de données contenant des informations selon un format décrit dans `convert.py`.