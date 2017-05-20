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

L'étude d'épidémies est faite selon deux principales approches: l'approche déterministe qui relève des équations différentielles, et l'approche stochastique qui se base sur l'étude de graphes. La plupart des modèles utilisés se traduisent facilement entre les deux approches, et le plus fameux est le modèle SIR [1]. Il s'agit de diviser la population en personnes *susceptibles* de contracter l'épidémie, celles qui sont *infectées* et celles qui sont *retirées* (mortes ou immunisées). De ce modèle découlent la plupart des autre modèles étudiés, qui font entrer en jeu d'autres facteurs (immunité temporaire ou période d'incubation, par exemple).

## 3. Problématique(s) retenues

Déterminer des méthodes de limitation de propoagation pour tout graphe et toute infection étant trop compliqué, nous avons divisé le problème en deux optiques envisageables:

- Comment **étouffer** une *épidémie donnée*, une fois lancée, en fonction du graphe donné? (identification de individus/secteurs à vacciner, à quarantiner, ...)
- Comment **prévenir**, pour un *graphe donné*, la propagation d'un épidémie avant son incubation en fonction de ses caractéristiques? (identification de noeuds centraux, limites dans les moyens pouvant être déployés)

## 4. Objectif(s) du travail

- Etre capable de lister des mesures concrètes pour limiter la propagation (en *prévention* et en *étouffement*) (par exemple, liste des personnes à cibler, ...)
- Savoir quels paramètres ont quelle importance dans la propagation (identification éventuelle d'un seuil d'infection, ...)

## 5. Liste de réferences bibliographiques
*(ébauche temporaire...)*

[1] -  W. O. Kermack and A. G. McKendrick, **A Contribution to the Mathematical Theory of Epidemics**, Proceedings of the Royal Society A (1927) (...)

-> invention du modele SIR

[2] - Matt J. Keeling and Ken T. D. Eames, **Networks and epidemic models**,  Journal of the Royal Society Interface (2005) (...)

-> résume bien l'ensemble des 

[3] - Nicholas C. Grassly, Christophe Fraser & Geoffrey P. Garnett, **Host immunity and synchronized epidemics of syphilis across the United States**, Nature (2005) (...)

-> analyse plus pratique d'epidemies, et d'oscillations

[4] - 

NCM - 44, 52, 69, 173, 183, 195, 196, 213, 238, 267, 278

