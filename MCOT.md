# Analyse stochastique d'épidémies

## 1. Positionnement thématique
| Mot-clés       | *(anglais)*         | Thèmes                              |
| -------------- | ------------------- | ----------------------------------- |
| épidémies      | epidemics           | Mathématiques discrètes (*graphes*) |
| modèle SIR     | SIR model           | Modélisations stochastiques         |
| infections     | infections          | Simulation informatique             |
| immunité       | immunity            |                                     |
| trajectométrie | trajectory analysis |                                     |

## 2. Bibliographie commentée

1. **Modèle SIR** [1] [2]

L'étude d'épidémies est faite selon deux principaux axes: l'approche déterministe qui relève des équations différentielles, et l'approche stochastique qui se base sur l'étude de graphes. La plupart des modèles utilisés se traduisent facilement entre les deux approches, et le plus fameux est le modèle SIR [1]. Il s'agit de diviser la population en personnes *susceptibles* de contracter l'épidémie, celles qui sont *infectées* et celles qui sont *retirées* (mortes ou immunisées). De ce modèle découlent la plupart des autre modèles étudiés, qui font entrer en jeu d'autres facteurs (immunité temporaire ou période d'incubation, par exemple). *[...]*

2. **Trajectométrie** + Bic

Dans les épidémies se propageant de manière rapide et peu prédictible, l'étude des déplacements devient primordiale. Aussi est-il capital de savoir interpréter le role de ces derniers dans la transmission d'une épidémie [3]. Au-delà du role de diffusion joué par ces mouvements, leurs impacts sont souvent hétérogènes sur les populations - certaines classes sociales sont nettements plus touchés que d'autres, expliquant par exemple la diffusion du Malaria en Afrique [4].

3. **Stopper une épidémie**

*$R_0$, etc...*

4. **Extensions du modèle SIR**

Une des études les plus populaires dans l'épidémiologie est celle des synchronisations dans un réseau: lorsque les conditions sont rassemblées, une épidémie peut survivre par "vagues", en apparaissant et disparaissant dans différentes régions [2]. C'est par exemple le cas de certaines MST, comme la syphilis aux Etats-Unis [5].

Les phénomènes dits de "petit monde" sont aussi importants dans l'étude d'une épidémie: les hommes se relieraient en vaste cliques, qui sont particulièrement vulnérables envers certaines épidémies [7]. Le modèle notable est celui de *Watts-Strogatz* [8], qui est souvent cité comme archétype du "petit monde".

La recherche d'un seuil épidémique est aussi à la mode: existe-t-il une fonction permettant de dire si une épidémie va persister ou non à partir des paramètres et d'un seuil? [7] Dans certains modèles, un seuil épidémique est établi et prouvé, dans d'autres il est démontré qu'il n'existe pas de tel seuil.

Enfin, l'étude de chaines de Markov *[...]*

*(191 mots)*

## 3. Problématique(s) retenues

Comment modéliser la propagation d'une épidémie dans une région?

## 4. Objectif(s) du travail

Déterminer des méthodes de limitation de propoagation pour tout graphe et toute infection étant trop compliqué, nous avons divisé le problème en deux optiques envisageables:

- Comment **étouffer** une *épidémie donnée*, une fois lancée, en fonction du graphe et des trajectoires donnés? (identification de individus/secteurs à vacciner, à quarantiner, ...)
- Comment **prévenir**, pour un *graphe et des trajectoires donnés*, la propagation d'un épidémie avant son incubation en fonction de ses caractéristiques? (identification de noeuds centraux, limites dans les moyens pouvant être déployés)
- Quelles sont les **caractéristiques intéressantes** d'une épidémie dans un graphe donné?

## 5. Liste de réferences bibliographiques
*(ébauche temporaire...)*

[1] -  W. O. Kermack and A. G. McKendrick, **A Contribution to the Mathematical Theory of Epidemics**, Proceedings of the Royal Society A (1927) (...)

    invention du modele SIR

[2] -  David Easley, Jon Kleinberg, **Networks, Crowds, and Markets** (2010), Chapter 21: *Epidemics* (...)

    livre qui reprend le sujet en detail

[3] - Downton, F. (1972). **The Area under the Infectives Trajectory of the General Stochastic Epidemic**. *Journal of Applied Probability*, 9(2), 414-417. doi:10.2307/3212809

    importance de la trajectoire

[4] - Martens, Pim, and Lisbeth Hall. **"Malaria on the move: human population movement and malaria transmission."** *Emerging infectious diseases 6.2* (2000): 103.

    importance des mouvements

[5] - H. Falconet, A.Jego, **Modéliser la propagation d'un épidémie** (2015) (...)

    résume bien l'ensemble des modèles en francais, approche maths fondamentale

[6] - Nicholas C. Grassly, Christophe Fraser & Geoffrey P. Garnett, **Host immunity and synchronized epidemics of syphilis across the United States**, Nature (2005) (...)

    analyse plus concrète des oscillations

[7] - David (2013, Fevrier 25). **Propagation d'épidémies et graphes aléatoires**. Obtenu sur [sciencetonnante.wordpress.com/2013/02/25/propagation-depidemies-et-graphes-aleatoires/](https://sciencetonnante.wordpress.com/2013/02/25/propagation-depidemies-et-graphes-aleatoires/)

    tour du domaine

[8] - Watts, Duncan J., and Steven H. Strogatz. **"Collective dynamics of ‘small-world’networks."** *Nature* 393.6684 (1998): 440-442.

    modèle de petit monde

NCM - 44, 52, 69, 173, 183, 195, 196, 213, 238, 267, 278

