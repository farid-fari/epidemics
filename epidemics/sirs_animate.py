''' Permet de générer des animations de réseaux SIRS.

Introduit la fonction animate pour animer un réseau SIRS.'''

import os
import networkx as nx
import matplotlib as mtpl
import matplotlib.pyplot as plt
import seaborn as sb
import numpy as np
import sirs

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

    model = sirs.Sirs(n, d, p, graph)

    pos = nx.spring_layout(model.graph, pos=nx.circular_layout(model.graph))

    mod = "SIS"
    if d[1]:
        mod = "SIRS"
    if d[1] >= turns:
        mod = "SIR"

    for m in range(turns):
        # On avance d'un tour
        model.increment()

        plt.cla()
        with sb.axes_style('dark'):
            plt.figure(num=1, figsize=(10, 7))
            plt.axis("off")

        xa = np.array([x[0] for i, x in enumerate(list(pos.values()))
                       if model.graph.node[i]['state']])
        ya = np.array([x[1] for i, x in enumerate(list(pos.values()))
                       if model.graph.node[i]['state']])
        # La heatmap a peu d'intéret et est peu stable pour peu de valeurs
        if xa.size > 2:
            sb.kdeplot(xa, ya, shade=True, cmap="Purples", legend=False, shade_lowest=False)

        nx.draw_networkx(
            model.graph,
            pos=pos,
            with_labels=False,
            arrows=False,
            node_color=[2 - k[1]['state'] for k in model.graph.nodes(data=True)],
            cmap=mtpl.cm.get_cmap(name="plasma"),
            vmin=0,
            vmax=2,
            edge_color=[2 - t[2]['color'] for t in model.graph.edges(data=True)],
            edge_cmap=mtpl.cm.get_cmap(name="gray"),
            edge_vmin=0,
            edge_vmax=2.3,
            node_size=5000/(model.n)+200,
            width=0.2)

        plt.title(f"Etat final du modèle {mod} (t={m})")
        plt.plot(-1, -1, marker='o', color=(240/255, 249/255, 33/255))
        plt.plot(-1, -1.2, marker='o', color=(204/255, 71/255, 120/255))
        plt.text(-.95, -1.03, "Susceptible", fontsize=9)
        plt.text(-.95, -1.23, "Infecté", fontsize=9)
        if mod != "SIS":
            plt.plot(-1, -1.4, marker='o', color=(13/255, 8/255, 135/255))
            plt.text(-.95, -1.43, "Retiré", fontsize=9)

        # Il faut que tout rentre
        plt.axis([-1.45, 1.45, -1.45, 1.45])

        plt.savefig(f"animate/{m}.png")
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
