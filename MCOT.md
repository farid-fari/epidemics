# Analyse stochastique d'épidémies

## 1. Positionnement thématique
| Mot-clés       | *(anglais)*         | Thèmes                              |
| -------------- | ------------------- | ----------------------------------- |
| épidémies      | epidemics           | Modélisations stochastiques         |
| modèle SIR     | SIR model           | Mathématiques discrètes (*graphes*) |
| infections     | infections          | Simulation informatique             |
| immunité       | immunity            |                                     |
| trajectométrie | trajectory analysis |                                     |

## 2. Bibliographie commentée

#### 1. Introduction - modèle SIR (*161w*)

L'épidémiologie est la branche des mathématiques appliquées s'intéressant à la modélisation d' une population donnée et la propagation d'un agent infectieux en son sein. Effectuer une "étude épidémique", c'est tenter de simuler le plus fidèlement possible la propagation d'une épidémie donnée au sein de la population étudiée, qu'elle soit humaine, animale ou informatique, afin d'anticiper au mieux une épidémie réelle. **60w**

L'étude d'épidémies est faite selon deux principaux axes: l'approche déterministe qui relève des équations différentielles, et l'approche stochastique qui se base sur l'étude de graphes et de chaines de Markov. La plupart des modèles utilisés peuvent etre étudiés avec les deux approches, et le plus connu est le modèle SIR [1]. Il s'agit de diviser la population en trois catégories: les personnes *susceptibles* de contracter l'épidémie, celles qui sont *infectées* et celles qui sont *retirées* (mortes ou immunisées). De ce modèle découlent la plupart des autre modèles étudiés, qui font entrer en jeu d'autres facteurs (immunité temporaire ou période d'incubation, par exemple). [2] **101w**

#### 2. Trajectométrie (+ Bic) (*79w*)

Dans les épidémies se propageant de manière rapide et peu prédictible, l'étude des déplacements devient primordiale. [3] L'étude des déplacements au sein d'une région est nommée trajectométrie, et se fait souvent à partir d'enquêtes de déplacement réalisées au sein d'une région, permettant de modéliser les déplacements par un graphe, auquel on peut appliquer le modèle SIR. Il est démontré que le nombre d'individus atteints par une épidémie sur un modèle SIR dépend fortement de la distance parcourue par les individus. [3]

L'étude des mouvements peut aussi se faire par l'étude de chaines de Markov *[...]*

#### 3. Stopper une épidémie (*118w*)

La recherche d'un seuil épidémique est un domaine très exploré: existe-t-il une fonction permettant de dire si une épidémie va persister ou non à partir de ses paramètres et d'un seuil? [7] Déterminer une telle fonction permetterait d'identifier les moyens les plus efficaces de stopper une épidémie. Dans certains modèles, un seuil épidémique est établi et prouvé, dans d'autres il est démontré qu'il n'existe pas de tel seuil. [2] [9] La question reste cependant à controverse, la recherche de seuil étant encore très peu précise et certaine. [9]

D'autres pistes dans la recherche de manières de stopper un épidémie consiste à ajouter certains facteurs non pris en compte dans le modèle SIR traditionel, tels que les vaccinations ou les mises en quarantaine. [2] [10] *[...]*

#### 4. Extensions du modèle SIR (*85w*)

Une des études les plus faites récemment est celle des synchronisations dans un réseau: lorsque les conditions sont rassemblées, une épidémie peut survivre par "vagues", en apparaissant et disparaissant dans différentes régions [2]. C'est par exemple le cas de certaines MST, comme la syphilis aux Etats-Unis [5].

Les phénomènes dits de "petit monde" sont aussi importants dans l'étude d'une épidémie: les hommes se relieraient en vaste cliques, qui sont particulièrement vulnérables envers certaines épidémies. [7] Le modèle notable est celui de *Watts-Strogatz* [8], qui est l'archétype du "petit monde".

##### +reseaux scale free (important)

*(443 mots)*

## 3. Problématique(s) retenues

Comment modéliser la propagation d'une épidémie dans une région?

## 4. Objectif(s) du travail

L'étude générale de propagation sur tout graphe et toute infection étant trop compliqué, nous avons divisé le problème en deux optiques envisageables:

- Comment **freiner** une épidémie dans un réseau donné?
- Etude stochastique au sein d'un noeud quelconque (chaines de Markov, ...)
- Etude du modèle déterministe

## 5. Liste de réferences bibliographiques
*(ébauche temporaire...)*

[1] -  Kermack, William O., and Anderson G. McKendrick. **"A contribution to the mathematical theory of epidemics."** *Proceedings of the Royal Society of London A: mathematical, physical and engineering sciences*. Vol. 115. No. 772. The Royal Society, 1927.

    invention du modele SIR

[2] -  Easley, David, and Jon Kleinberg. **Networks, crowds, and markets: Reasoning about a highly connected world**. Cambridge University Press, 2010: 567-604

    livre qui reprend le sujet en detail

[3] - Downton, F. (1972). **The Area under the Infectives Trajectory of the General Stochastic Epidemic**. *Journal of Applied Probability*, 9(2), 414-417. doi:10.2307/3212809

    importance de la trajectoire

[5] - Falconet, Hugo, and Antoine Jego. **"Modéliser la propagation d’une épidémie."** (2015).

    résume bien l'ensemble des modèles en francais, approche maths fondamentale

[6] - Grassly, Nicholas C., Christophe Fraser, and Geoffrey P. Garnett. **"Host immunity and synchronized epidemics of syphilis across the United States."** *Nature* 433.7024 (2005): 417-421.

    analyse plus concrète des oscillations

[7] - David (2013, Fevrier 25). **Propagation d'épidémies et graphes aléatoires**. Obtenu sur [sciencetonnante.wordpress.com/2013/02/25/propagation-depidemies-et-graphes-aleatoires/](https://sciencetonnante.wordpress.com/2013/02/25/propagation-depidemies-et-graphes-aleatoires/)

    tour du domaine

[8] - Watts, Duncan J., and Steven H. Strogatz. **"Collective dynamics of ‘small-world’ networks."** *Nature* 393.6684 (1998): 440-442.

    modèle de petit monde

[9] - Wang, Wei, et al. **"Predicting the epidemic threshold of the susceptible-infected-recovered model."** *Scientific reports* 6 (2016).

    méthodes de prédiction de seuil + incertitudes liées à ces prédictions

[10] - Hethcote, Herbert, Ma Zhien, and Liao Shengbing. "Effects of quarantine in six endemic models for infectious diseases." Mathematical Biosciences 180.1 (2002): 141-160.

    mises en quarantaine
