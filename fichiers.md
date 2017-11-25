# Choses à faire avant tout

Malheureusement Farid est chiant avec son environnement de développement. Comme indiqué en bas du fichier `README.md`, il faut avoir au moins **Python 3.6** télechargeable sur le site [python](https://python.org) (donc pas la version pyzo).

Il faut installer les modules `networkx` (tracé de graphes, version **<=1.11**), `matplotlib`, `seaborn` (pour les jolies couleurs), `numpy`. Note: c'est chiant à faire sous Windows.

## Résumé

0. S'assurer de ne pas avoir une version de Python antérieure installée (la désinstaller dans ce cas-là)
1. Installer python 3.6 depuis le site
2. Aller [ICI](https://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy) télécharger `numpy`
3. Executer depuis une invite de commande `pip install nomdufichiertelechargenumpy` après s'etre place dans le bon dossier
4. Aller [ICI](https://www.lfd.uci.edu/~gohlke/pythonlibs/#scipy) télécharger `scipy`
5. Executer depuis une invite de commande `pip install nomdufichiertelechargescipy` après s'etre place dans le bon dossier
6. Executer `pip install matplotlib seaborn networkx==1.11`
7. Télécharger le code source **de la branche farid!!!** (cliquer sur branche farid sur github, puis telecharger à droite)

# Commentaires & Architecture

La plupart du code est commentée proprement: une ligne sur ce que le fonction fait, et description de ce que chaque argument fait. Les lire en cas de souci.

Le code est organisé en plusieurs dossiers: `docs` contient de jolis exemples, `epidemics` tout ce qui est SIR/S, `product_consumption` un ancien TIPE, `trajectometry` voila, et le dossier de base avec MCOT et `traj_to_sirs.py`.

La plupart des fichiers ne font que de définir des fonctions et classes. J'ai souvent ajouté quelques lignes en bas pour que les fonctions fassent une démonstration si on execute le fichier directement (`python fichier.py` dans une invite).

Ce que je te conseille après avoir compris la structure, c'est de créer un fichier `thibault.py` dans le dossier de base et de programmer ce que tu veux avec. Pour ca, importer les fonctions qui t'intéressent en faisant:

    from epidemics.sirs import Sirs
    # par exemple, ou
    from trajectometry.transition import passage

    # generalement:
    from dossier.fichier import fonctionOuClasse, fonctionOuClasse2, ..., fonctionOuClasseN

Enfin, la `MCOT` sur laquelle on avait travaillé est en format markdown sous le nom `MCOT.md` et en format LaTeX sous le nom `MCOT.tex`.

# Fichiers importants

## `epidemics\sirs.py`

Contient la classe `Sirs` qui permet de simuler les modèles SIR, SIRS, SIS. Exemple d'utilisation-type:

    s = Sirs(n=60, d=[4, 2], p=0.05, graph=0.3)
    # Crée un réseau de 60 individus pris d'une maladie qui dure
    # 4 instants, rend immun 2 instants, avec une probabilité de
    # propagation de 0.05. La population est relié par un graphe
    # de densité 0.3

    s.plot()
    # Permet de représenter joliment le réseau

    s.increment(turns=5)
    # Fait avancer l'épidémie de 5 instants

    s.increment_avg(turns=50, sample=500)
    # Effectue 500 simulations des 50 prochains tours, et affiche
    # l'évolution moyenne

Garantie de débloquer 3 points chez le jury si tu leur explique que c'est de la POO.

## `trajectometry`

C'est encore une autre histoire -- il faut construire la base de données. Pour ca, convertir le fichier `.xlsx` de Bicout en `.csv` avec Excel. Le copier dans le dossier `trajectometry` sous le nom `trajecto.csv` et executer `trajectometry\convert.py`.

Ensuite, voici les commandes intéressantes depuis le fichier `trajectometry`:

    repartition.py
    # Affiche le graphe dont Bicout avait parlé

    transition.py
    # Crée matrice de transition

# `traj_to_sirs.py`

C'est le plat de résistance, met tout ensemble pour faire un tracé de `R0` en fonction du temps. Peut aussi simplement crér un modèle SIRS, ainsi qu'une matrice de probabilité de présence (lire commentaires).
