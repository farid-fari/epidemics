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

1. **Modèle SIR** [1] [3] [6]
L'étude d'épidémies est faite selon deux principaux axes: l'approche déterministe qui relève des équations différentielles, et l'approche stochastique qui se base sur l'étude de graphes. La plupart des modèles utilisés se traduisent facilement entre les deux approches, et le plus fameux est le modèle SIR [1]. Il s'agit de diviser la population en personnes *susceptibles* de contracter l'épidémie, celles qui sont *infectées* et celles qui sont *retirées* (mortes ou immunisées). De ce modèle découlent la plupart des autre modèles étudiés, qui font entrer en jeu d'autres facteurs (immunité temporaire ou période d'incubation, par exemple).
*...*
2. **Trajectométrie** [2] + B
3. **Stopper une épidémie** [4] [7]
*$R_0$, etc...*
4. **Extensions du modèle SIR** (*chaines de Markov*) [4] [5] [7] + ...
*réseaux W-S, oscillations SIRS, ...*

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

-> introduction au modele SIR

[2] - F. Downton, The Area under the Infectives Trajectory of the General Stochastic Epidemic, Journal of Applied Probability (1972) (...)

-> **importance** de la trajectoire

[3] - Matt J. Keeling and Ken T. D. Eames, **Networks and epidemic models**,  Journal of the Royal Society Interface (2005) (...)

-> résume bien l'ensemble des modèles utilisés

[4] - H. Falconet, A.Jego, **Modéliser la propagation d'un épidémie** (2015) (...)

-> Résumé bien l'ensemble des modèles en francais, approche maths fondamentale

[5] - Nicholas C. Grassly, Christophe Fraser & Geoffrey P. Garnett, **Host immunity and synchronized epidemics of syphilis across the United States**, Nature (2005) (...)

-> analyse plus pratique d'epidemies, et d'oscillations

[6] -  David Easley, Jon Kleinberg, **Networks, Crowds, and Markets** (2010), Chapter 21: *Epidemics* (...)

-> livre qui reprend le sujet en detail

[7] - Science Etonnante, **Propagation d'épidémies et graphes aléatoires** (2013) (...)

NCM - 44, 52, 69, 173, 183, 195, 196, 213, 238, 267, 278

