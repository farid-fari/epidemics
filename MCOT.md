# Analyse stochastique d'épidémies

## 1. Positionnement thématique
| Mot-clés       | *(anglais)*         | Thèmes                              |
| -------------- | ------------------- | ----------------------------------- |
| épidémies      | epidemics           | Modélisations stochastiques         |
| modèle SIR     | SIR model           | Mathématiques discrètes             |
| infections     | infections          | Simulation informatique             |
| immunité       | immunity            |                                     |
| trajectométrie | trajectory analysis |                                     |

## 2. Bibliographie commentée

#### 1. Introduction - SIR et trajectométrie

L'épidémiologie est la branche des mathématiques appliquées s'intéressant à la modélisation de la propagation d'un épidémie dans une population structurée. L'étude d'épidémies est faite selon deux principaux axes: l'approche déterministe qui relève des équations différentielles, et l'approche stochastique qui se base sur l'étude de graphes et de chaines de Markov.
La plupart des modèles utilisés peuvent etre étudiés avec les deux approches, et le plus commun est le modèle compartimental SIR, inventé par Kermack et McKendrick [1]. Il s'agit de diviser la population en trois catégories: les personnes *susceptibles* de contracter l'épidémie, celles qui sont *infectées* et celles qui sont *retirées* (mortes ou immunisées).
De ce modèle découlent la plupart des autre modèles étudiés, qui font entrer en jeu d'autres facteurs (périodes réfractaires ou incubatoires, par exemple). [2]

Dans les épidémies se propageant de manière rapide et peu prédictible, l'étude des déplacements et des liens formés par ces derniers devient primordiale. [2][3] Cette étude se nomme trajectométrie, et se fait souvent à partir d'enquêtes de déplacement réalisées au sein d'une région. [4] Les résultats permettent de modéliser les amas de population et leurs déplacements par un graphe ou par des paramètres, dépendant du modèle choisi.

#### 2. Approche déterministe

Le modèle déterministe traduit des estimations ou mesures statistiques sur une épidémie en un système d'équations différentielles. [4] Dépendant de la complexité du système obtenu, il peut être résolu entièrement, ou bien approximé informatiquement. On peut alors obtenir des états stables, où l'épidémie stagnera, mais aussi des expressions de forme fermée du nombre d'infectés, précieuses pour un travail de prévention ou de prédiction. [4][5]

Bien qu'elle présente une plus grande précision, l'approche déterministe a du mal à prendre en compte les déplacements et connections entre les individus: la population est assimilée à une masse homogène, et n'est donc plus structurée. [2][5]

#### 3. Approche stochastique

##### 3.1. Chaines de Markov

Les chaines de Markov permettent de modéliser de manière simple l'évolution d'un modèle SIR, notamment à grande échelle.
Contrairement aux modèles déterministes, on suppose que le temps s'écoule selon des instants discrets, et que le nombre d'individus infectés suit une évolution stochastique selon un nombre d'états fini. Ce modèle permet d'atteindre des résultats intéressants, comme l'établissement d'un état stable ou bien d'un équilibre après un temps infini. [6]

##### 3.2. Simulations et graphes

Comme il s'agit d'un modèle stochastique appliqué à un graphe souvent complexe, l'étude approfondie et précise du modèle SIR repose le plus souvent sur des simulations informatiques. [4]
L'étude des synchronisations dans un réseau, proche de l'étude des modèles neuronaux, est un sujet en vogue: lorsque les conditions sont rassemblées, une propagation chaotique peut s'organiser en "vagues" grâce aux déplacements et à la structure du réseau; apparaissant et disparaissant de manière synchronisée dans différentes régions. [2][3]

#### 4. Stopper une épidémie

La recherche d'un seuil épidémique est un domaine très exploré: existe-t-il une fonction permettant de dire si une épidémie va persister ou non à partir de ses caractéristiques? [1][6][8]
Déterminer une telle fonction permetterait d'identifier les moyens les plus efficaces de stopper une épidémie, à partir de la recherche d'extremums. Dans certains modèles, un seuil épidémique est établi et prouvé, dans d'autres il est démontré qu'il n'existe pas de tel seuil. [2][9]
La question reste cependant à controverse, la recherche de seuil étant encore très peu précise et certaine. [9]
Une autre méthode consiste à ajouter certains facteurs au modèle, non pris en compte dans le modèle SIR traditionel, tels que les vaccinations ou les mises en quarantaine. [2][10] Cette approche plus qualitative et expérimentale vise à identifier la manière la plus efficace de dépenser une quantité finie de ressources afin d'éteindre une épidémie.

*(563 mots)*

## 3. Problématique(s) retenues

Comment modéliser, prévoire et minimiser la propagation d'une épidémie dans une région?

## 4. Objectif(s) du travail

L'étude précise d'une propagation sur un graphe avec une infection quelconques étant trop compliquée, nous avons divisé le problème en trois objectifs abordables:

- Comment *freiner* une épidémie quelconque dans un réseau donné?
- *Etude stochastique* à l'aide de chaines de Markov au sein d'une population quelconque
- *Etude déterministe* au sein d'une population quelconque

## 5. Liste de réferences bibliographiques

*(ébauche temporaire...)*

[1] -  Kermack, William O., and Anderson G. McKendrick. **"A contribution to the mathematical theory of epidemics."** *Proceedings of the Royal Society of London A: mathematical, physical and engineering sciences*. Vol. 115. No. 772. The Royal Society, 1927.

    invention du modele SIR

[2] -  Easley, David, and Jon Kleinberg. **Networks, crowds, and markets: Reasoning about a highly connected world**. Cambridge University Press, 2010: 567-604

    livre qui reprend le sujet en detail

[3] - Mari, Lorenzo, et al. **"Modelling cholera epidemics: the role of waterways, human mobility and sanitation."** Journal of the Royal Society Interface 9.67 (2012): 376-388.

    importance de la trajectoire + oscillations possibles avec déplacements

[4] - Balenghien, Thomas. **"Effet du confiage d'animaux dans la propagation d'une maladie contagieuse au sein d'un réseau structuré de troupeaux: exemple de la péripneumonie contagieuse bovine dans les troupeaux éthiopiens."** (2002).

    mémoire étudiant Bic - voir surtout la partie II (p25)
    simulations numériques (I), matrices d'échanges (II) etc...

[5] - Anselme, Bruno. **Biomathématiques: Outils, méthodes et exemples**. Dunod, 2015.

    approche déterministe dévelopée, ainsi qu'un seuil

[6] - Falconet, Hugo, and Antoine Jego. **"Modéliser la propagation d’une épidémie."** (2015).

    résume bien l'ensemble des modèles en francais, approche maths fondamentale

[7] - Grassly, Nicholas C., Christophe Fraser, and Geoffrey P. Garnett. **"Host immunity and synchronized epidemics of syphilis across the United States."** *Nature* 433.7024 (2005): 417-421.

    analyse plus concrète des oscillations

[8] - David (2013, Fevrier 25). **Propagation d'épidémies et graphes aléatoires**. Obtenu sur [sciencetonnante.wordpress.com/2013/02/25/propagation-depidemies-et-graphes-aleatoires/](https://sciencetonnante.wordpress.com/2013/02/25/propagation-depidemies-et-graphes-aleatoires/)

    tour du domaine

[9] - Wang, Wei, et al. **"Predicting the epidemic threshold of the susceptible-infected-recovered model."** *Scientific reports* 6 (2016).

    méthodes de prédiction de seuil + incertitudes liées à ces prédictions

[10] - Hethcote, Herbert, Ma Zhien, and Liao Shengbing. "Effects of quarantine in six endemic models for infectious diseases." Mathematical Biosciences 180.1 (2002): 141-160.

    mises en quarantaine
