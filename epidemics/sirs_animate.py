''' Illustre les oscillations possibles dans certains réseaux avec le modèle SIRS.

Introduit la fonction plot pour tracer un réseau SIRS.'''

import os
import random as rand
import networkx as nx
import matplotlib.pyplot
import matplotlib as mtpl
import seaborn as sb
import numpy as np

def animate(n=60, d=[4, 2], p=0.05, turns=100, graph=0.3):
    '''Trace un graphe du modèle SIRS après un nombre défini de tours.

        n (int): nombre de personnes
        d[0] (int): duration de l'infection en tours
        d[1] (int): duration de l'immunité en tours
            s'il vaut 0, on aura un modèle SIS
            s'il est >= à turns, c'est un modèle SIR
        p (float): probabilité d'infection
        turns (int): nombre de tours à simuler
        graph (nx.Graph ou int ou float): un éventuel graphe imposé,
            ou bien une densité pour qu'un graphe soit généré'''
    if not os.path.exists('animate'):
        os.mkdir('animate')

    if isinstance(graph, float) or isinstance(graph, int):
        # On a alors passé une densité pour la génération d'un graphe
        graph = nx.gnp_random_graph(n, graph, directed=True)
    else:
        # On initialise le nombre de personnes
        n = graph.number_of_nodes()

    # On initialise les attributs
    for node in graph.nodes(data=True):
        # state = 0=S et 1=I, age = nombre de tours infecté
        node[1]['state'] = 0
        # age = nombre de tours infecté
        node[1]['age'] = 0
    for edge in graph.edges(data=True):
        # color = 0 neutre, 1 tentative d'infection, 2 infection transmise
        edge[2]['color'] = 0

    # On infecte un patient zero en on l'affiche
    graph.node[rand.randint(0, n - 1)]['state'] = 1

    pos = nx.spring_layout(graph, pos=nx.circular_layout(graph))

    for m in range(turns):
        # Evite de traiter des patient infectés dès ce tour-ci
        for node in [k for k in graph.nodes(data=True) if k[1]['state'] >= 1]:
            # On ne s'interesse qu'aux patients infectés
            if node[1]['state'] == 1:
                if node[1]['age'] < d[0]:
                    node[1]['age'] += 1
                    for other in graph[node[0]]:
                        # Si l'autre est dans l'état S
                        if not graph.node[other]['state']:
                            if rand.random() < p:
                                # On met les stats au mode infecté
                                graph.node[other]['state'] = 1
                                graph.node[other]['age'] = 0 # par sureté (non nécessaire)

                                # Pour la coloration
                                graph.edge[node[0]][other]['color'] = 2
                            else:
                                graph.edge[node[0]][other]['color'] = 1
                else:
                    if d[1]:
                        # Passage en mode retiré
                        node[1]['state'] = 2
                        node[1]['age'] = 0
                    else:
                        # Passage en mode susceptible
                        node[1]['state'] = 0
                        node[1]['age'] = 0
            elif node[1]['state'] == 2:
                if node[1]['age'] < d[1]:
                    node[1]['age'] += 1
                else:
                    # Remise à zero des statistiques
                    node[1]['state'] = 0
                    node[1]['age'] = 0

        mtpl.pyplot.cla()
        with sb.axes_style('dark'):
            mtpl.pyplot.figure(num=1, figsize=(10, 7))
            mtpl.pyplot.axis("off")

        xa = np.array([x[0] for i, x in enumerate(list(pos.values())) if graph.node[i]['state']])
        ya = np.array([x[1] for i, x in enumerate(list(pos.values())) if graph.node[i]['state']])
        # La heatmap a peu d'intéret et est peu stable pour peu de valeurs
        if xa.size > 2:
            sb.kdeplot(xa, ya, shade=True, cmap="Purples", legend=False, shade_lowest=False)

        nx.draw_networkx(
            graph,
            pos=pos,
            with_labels=False,
            arrows=False,
            node_color=[2 - k[1]['state'] for k in graph.nodes(data=True)],
            cmap=mtpl.cm.get_cmap(name="plasma"),
            vmin=0,
            vmax=2,
            edge_color=[2 - t[2]['color'] for t in graph.edges(data=True)],
            edge_cmap=mtpl.cm.get_cmap(name="gray"),
            edge_vmin=0,
            edge_vmax=2.3,
            node_size=5000/n+200,
            width=0.2)

        mod = "SIS"
        if d[1]:
            mod = "SIRS"
        if d[1] >= turns:
            mod = "SIR"
        mtpl.pyplot.title(f"Etat final du modèle {mod} (t={m})")
        mtpl.pyplot.plot(-1, -1, marker='o', color=(240/255, 249/255, 33/255))
        mtpl.pyplot.plot(-1, -1.2, marker='o', color=(204/255, 71/255, 120/255))
        mtpl.pyplot.text(-.95, -1.03, "Susceptible", fontsize=9)
        mtpl.pyplot.text(-.95, -1.23, "Infecté", fontsize=9)
        if mod != "SIS":
            mtpl.pyplot.plot(-1, -1.4, marker='o', color=(13/255, 8/255, 135/255))
            mtpl.pyplot.text(-.95, -1.43, "Retiré", fontsize=9)

        # Il faut que tout rentre
        mtpl.pyplot.axis([-1.45, 1.45, -1.45, 1.45])

        mtpl.pyplot.savefig(f"animate/{m}.png")
        print(m)

if __name__ == "__main__":
    import subprocess
    animate()
    os.chdir('animate') # crée par la fonction
    if os.path.exists('final.mkv'):
        os.unlink('final.mkv')
    try:
        subprocess.run(['ffmpeg', '-r', '8', '-i', '%d.png', 'final.mkv'])
        subprocess.run(['vlc', 'final.mkv'])
    except (subprocess.CalledProcessError, FileNotFoundError):
        raise ProcessLookupError('ffmpeg ou vlc manquant')
