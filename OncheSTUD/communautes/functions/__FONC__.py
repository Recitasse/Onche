import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import os
import sys
import community as community_louvain
from matplotlib.patheffects import withStroke
import matplotlib.cm as cm
from collections import defaultdict
import copy
import matplotlib.patches as patches
from prettytable import PrettyTable
from lib_pos import community_layout
import matplotlib.colors as mcolors
import random
from matplotlib.patches import PathPatch

parent = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(parent)

print(parent)

from utils.graphics import bar_etape
from BDD.bdd import BDD
from config.Variables.variables import *

def create_path_effect(linewidth, foreground):
    return [withStroke(linewidth=linewidth, foreground=foreground)]

def generate_random_points(x_range=(0, 20), y_range=(0, 20), size:int=1)->tuple:
    points = []
    x = random.uniform(x_range[0], x_range[1])
    y = random.uniform(y_range[0], y_range[1])
    points = (x, y)
    return points

def generate_points_with_min_distance(N, size_range, min_distance, center=(0, 0)):
    points = []
    
    while len(points) < N:
        bar_etape(N, len(points),"Construction des communautés")
        size = np.random.uniform(*size_range)
        angle = np.random.uniform(0, 2 * np.pi)
        distance = size * np.random.uniform(0, 1)
        
        x = center[0] + distance * np.cos(angle)
        y = center[1] + distance * np.sin(angle)
        
        valid_point = True
        for i, existing_point in enumerate(points):
            if np.linalg.norm(np.array(existing_point) - np.array((x, y))) < min_distance:
                valid_point = False
                break
        
        if valid_point:
            points.append((x, y))

    return points

def generate_random_coordinates(center:tuple, span:float, concentration:float)->tuple:
    """
    Generate random coordinates around a center point.

    Args:
        center (tuple): Center point (x, y) around which to generate coordinates.
        span (float): Range of x and y values for random generation
        concentration (float): Concentration factor for random generation.

    Returns:
        tuple (x, y).
    """
    span_x = span
    span_y = span
    x_center, y_center = center

    angles = np.random.uniform(0, 2 * np.pi)

    radii = np.random.vonmises(0, concentration)

    x_offsets = radii * np.cos(angles)
    y_offsets = radii * np.sin(angles)

    x_coords = x_center + span_x * x_offsets
    y_coords = y_center + span_y * y_offsets
    coordinates = (x_coords, y_coords)

    return coordinates


def graphique(labels_observe, weights_observe, LINK, N, commu:bool=True, nom:str="Test", title:str="Réseau", k:int=1, alp_p:list=[1, 1], size_font:list=[5, 20, 5], dec=0, coef:list=[1,1, 0.12], size:int=40, min_dist:int = 10):
    """
    Permet de tracer le réseau

    Args:
        labels_observé (array N string) : Les noms observés
        weights_observe (array N float) : le poids des noms
        LINK (array NxN float) : La matrice de lien entre les labels
        commu (bool) : tracer le graphe des communautés
        nom (str) : Le nom du dossier
        title (str) : titre du graphique
        k (float) : le layout du graph ]0 - 2] 
        alp_p (array 2 float [0.1- 2]) : coef des alpha [0 -> edges, 1 -> noeuds]
        size_font (array 2 int [0 30 15]) : coef des font_size [0-> minimal value, 1->maximal value 2->seuil (égal à la minimale si inférieur)]
        dec (int) : réajuste le décalage de l'incrémentation
        coef (array 2) : [0-> coef sur les edges, 1-> coef sur les noeuds]
    """
    bs = "\033[1m"; bf = "\033[0m"
    print("Préparation des onchois : ")
    user_weights = {user: weight for user, weight in zip(labels_observe, weights_observe)}


    # Créer un graphe
    G = nx.Graph()
    G.add_nodes_from(labels_observe)
    size_user = []
    for i in range(N):
        size_user.append(weights_observe[i])

    al = alp_p[0]
    max_w = np.max(LINK)
    for i in range(N):
        for j in range(N):
            weight = LINK[i-1+dec, j-1+dec]
            if weight != 0:
                if (np.log(al*weight) - np.log(1)) / (np.log(al*max_w)) - np.log(1) < 0:
                    alp = 0
                else:
                    alp = (np.log(al*weight) - np.log(1)) / (np.log(al*max_w)) - np.log(1)

                G.add_edge(
                    labels_observe[i], 
                    labels_observe[j], 
                    weight=weight*coef[0],
                    alpha=alp, 
                    width=5*alp*coef[0]
                    )
                
    print(f"Détermination des communautés : ")
    partition = community_louvain.best_partition(G)
    community_counts = {}
    for comm in partition.values():
        if comm not in community_counts:
            community_counts[comm] = 1
        else:
            community_counts[comm] += 1

    print(f"-> Filtrage des communautés")
    valid_communities = {comm for comm, count in community_counts.items() if count > 1}
    cleaned_partition = {node: comm for node, comm in partition.items() if comm in valid_communities}

    cleaned_G = nx.Graph()
    cleaned_G.add_nodes_from(cleaned_partition.keys())
    for u, v, attr in G.edges(data=True):
        if u in cleaned_G.nodes() and v in cleaned_G.nodes():
            cleaned_G.add_edge(u, v, **attr)

    unique_communities = set(cleaned_partition.values())
    nb_com = len(unique_communities)
    colormap = plt.cm.get_cmap('jet', nb_com)

    # Recréation des positions des noeuds et commu
    print(f"Position des noeuds : ")
    pos = community_layout(cleaned_G, cleaned_partition)

    community_sizes = {}
    for node, community in cleaned_partition.items():
        if community not in community_sizes:
            community_sizes[community] = 1
        else:
            community_sizes[community] += 1

    size_commu = {commu: size for commu, size in community_sizes.items()}
    size_abs = [(size_commu[community]) for community in unique_communities]

    center_v = generate_points_with_min_distance(len(unique_communities), [np.min(size_abs), np.max(size_abs)],min_dist, (0,0))

    center = {community: center_v[i] for i,community in enumerate(unique_communities)}

    nodes_with_positions = {node: (pos[node][0], pos[node][1]) for node in cleaned_G.nodes()}

    cleaned_user_weights = {user: weight for user, weight in user_weights.items() if user in cleaned_G.nodes()}

    for node, position in nodes_with_positions.items():
        actual_center = center[cleaned_partition[node]]
        new_pos = generate_random_coordinates(actual_center, coef[2]*size_commu[cleaned_partition[node]], 10**-12)
        pos[node] = new_pos
    
    node_colors = [colormap(community) for community in cleaned_partition.values()]

    print(f"{bs}'Done'{bf}")
    print("Préparation du graphique : ")

    fig, ax = plt.subplots(figsize=(size, size), dpi=150, facecolor='black')
    '''for community, pos_center in center.items():
        size = 0.35 * community_sizes[community]
        alpha = 0.02
        color = colormap(community)
        circle = patches.Circle(pos_center, size, alpha=alpha, color=color)
        ax.add_patch(circle)'''

    print("-> Taille, alpha, couleur des noeuds : ")
    node_sizes = [cleaned_user_weights.get(node, 1)*coef[1] for node in cleaned_G.nodes()]

    alph = []
    al1 = alp_p[1]
    for i in range(N):
        m = (np.log(al1*size_user[i]) - np.log(1)) / (np.log(al1*np.max(size_user))) - np.log(1)

        if m < 0:
            alph.append(0)
        elif m>=0:
            alph.append(m)

    print("-> Taille des légendes : ")
    label_font_sizes = {node: size_font[1]*alph[i] for i, node in enumerate(cleaned_G.nodes())}

    nx.draw_networkx_nodes(
        cleaned_G,
        pos,
        node_color=node_colors,
        node_size=node_sizes,
        alpha=[val/size_font[1] for _, val in label_font_sizes.items()]
    )

    node_labels = {label: label for _, label in enumerate(cleaned_G.nodes())}

    it_size = 0
    for key, value in node_labels.items():
        if label_font_sizes[key] < size_font[2]:
            label_font_sizes[key] = size_font[0]
        label_texts = nx.draw_networkx_labels(
            G, 
            pos, 
            labels={key : value}, 
            font_size=label_font_sizes[key], 
            font_color='snow', 
            font_weight="bold", 
            verticalalignment='bottom',)
        it_size+=1

    for label_text in label_texts.values():
        label_text.set_path_effects(create_path_effect(1, 'black'))


    edge_colors = [colormap(cleaned_partition[u]) for u, v in cleaned_G.edges()]


    al = alp_p[0]
    max_w = np.max(LINK)
    for i in range(N):
        for j in range(N):
            weight = LINK[i-1+dec, j-1+dec]
            if weight != 0:
                if (np.log(al*weight) - np.log(1)) / (np.log(al*max_w)) - np.log(1) < 0:
                    alp = 0
                else:
                    alp = (np.log(al*weight) - np.log(1)) / (np.log(al*max_w)) - np.log(1)

                if labels_observe[i] in node_labels.keys() and labels_observe[j] in node_labels.keys():
                    cleaned_G.add_edge(
                        labels_observe[i], 
                        labels_observe[j], 
                        weight=weight*coef[0],
                        alpha=alp, 
                        width=5*alp*coef[0]
                        )

    print("-> Épaisseur, alpha, couleur, style des connexions : ")
    edges = nx.draw_networkx_edges(
        cleaned_G,
        pos,
        alpha=[cleaned_G[u][v]['alpha'] for u, v in cleaned_G.edges()],
        width=[cleaned_G[u][v]['width'] for u, v in cleaned_G.edges()],
        edge_color=edge_colors,
        arrows=True,
        connectionstyle="arc3,rad=0.3"
    )
    print(f"{bs}'Done'{bf}")
    plt.title(f"Constellation {nom} : {len(unique_communities)} communautés, {len(node_labels.keys())} onchois", fontsize=size, fontweight='bold', fontfamily='serif', color='white')
    plt.axis('off')
    print("Sauvegarde svg et png: ")
    plt.savefig(f"{GLOBAL_PATH}/OncheSTUD/communautes/Sujet/{nom}/Communauté_{title}.svg", format="svg")
    print(f"Format {bs}'svg'{bf} Done")
    #plt.savefig(f"{GLOBAL_PATH}/OncheSTUD/communautes/Sujet/{nom}/Communauté_{title}.png", format="png")
    #print(f"Format {bs}'png'{bf} Done")
    plt.close()
    plt.clf()
