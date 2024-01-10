import numpy as np
import os
import sys
import networkx as nx
import matplotlib.pyplot as plt
import community as community_louvain
from OncheSTUD.graphique.functions.lib_pos import community_layout

parent = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(parent)

from matplotlib.patheffects import withStroke
from BDD.bdd import BDD
from random import uniform
from config.Variables.variables import *
from utils.graphics import bar_etape


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


class Graphique(nx.Graph):
    def __init__(self, weight_lim: tuple, edge_weight_lim: tuple, LINK: np.ndarray):
        # public
        self.min_weight, self.max_weight = weight_lim
        self.min_edge_weight, self.max_edge_weight = edge_weight_lim
        self.LINK = LINK
        self.community = {}
        super().__init__()
        
        # private
        self.G_user_weight = []
        self.G_user_pos = {}

    def prepare_nodes(self, user: list, weight: list, color: list, alpha: list, pos: dict) -> None:
        """Ajoute les noeuds au graphique de la bonne couleur, alpha"""
        for i in range(len(user)):
            self.add_node(user[i],
                          color=color[i],
                          weight=self.normalize(weight[i], self.max_weight, self.min_weight),
                          alpha=self.normalize(alpha[i], 1, 0))
        nx.draw_networkx_nodes(self, pos)

    
    def prepare_edge(self, user: list, LINK: np.ndarray, al: float, weight_coef: float) -> None:
        """Prépare les liens entre les utilisateurs via la matrice de lien"""
        max_w = np.max(LINK)
        N = len(LINK[0][:])
        for i in range(N):
            for j in range(N):
                weight = LINK[i, j]
                if weight != 0:
                    if (np.log(al*weight) - np.log(1)) / (np.log(al*max_w)) - np.log(1) < 0:
                        alp = 0
                    else:
                        alp = (np.log(al*weight) - np.log(1)) / (np.log(al*max_w)) - np.log(1)

                    self.add_edge(
                        user[i], 
                        user[j], 
                        weight=weight*weight_coef,
                        alpha=alp, 
                        width=alp*weight_coef,
                        )
                    
    def prepare_community(self, min_dist: int, user: list, weight: list):
        """Prépare les communautés"""

        user_weights = {user_: weight_ for user_, weight_ in zip(user, weight)}
        partition = community_louvain.best_partition(self)
        community_counts = {}
        for comm in partition.values():
            if comm not in community_counts:
                community_counts[comm] = 1
            else:
                community_counts[comm] += 1

        valid_communities = {comm for comm, count in community_counts.items() if count > 1}
        cleaned_partition = {node: comm for node, comm in partition.items() if comm in valid_communities}

        self.cleaned_G = nx.Graph()
        self.cleaned_G.add_nodes_from(cleaned_partition.keys())
        for u, v, attr in self.edges(data=True):
            if u in self.cleaned_G.nodes() and v in self.cleaned_G.nodes():
                self.cleaned_G.add_edge(u, v, **attr)

        unique_communities = set(cleaned_partition.values())
        nb_com = len(unique_communities)
        colormap = plt.cm.get_cmap('jet', nb_com)

        # Recréation des positions des noeuds et commu
        print(f"Position des noeuds : ")
        pos = community_layout(self.cleaned_G, cleaned_partition)

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
        nodes_with_positions = {node: (pos[node][0], pos[node][1]) for node in self.cleaned_G.nodes()}

        cleaned_user_weights = {user: weight for user, weight in user_weights.items() if user in self.cleaned_G.nodes()}

        for node, position in nodes_with_positions.items():
            actual_center = center[cleaned_partition[node]]
            new_pos = generate_random_coordinates(actual_center, coef[2]*size_commu[cleaned_partition[node]], 10**-12)
            pos[node] = new_pos
        
        node_colors = [colormap(community) for community in cleaned_partition.values()]

    def _set_community(self) -> None:
        """Créer les communautés par algorithme de Louvain
        Attention /!\ cette méthode doit être utilisé après la création des edges"""

    def _add_user_to_node(self, user_name: str | list, weight: int | list) -> None:
        """Permet de mettre au bon format la liste des user"""
        if isinstance(user_name, str) and isinstance(weight, int):
            self.G_user_weight.append((user_name, weight))
        elif isinstance(user_name, list) and isinstance(weight, list):
            if len(user_name) == len(weight):
                for i in range(len(user_name)):
                    self.G_user_weight.append((user_name[i], weight[i]))
            else:
                raise IndexError("La taille de la list user doit correspondre à celle des poids.")

    def _add_user_pos(self, user_name: str | list, pos: tuple | list) -> None:
        """Permet de mettre au bon format les positions des utilisateurs"""
        if isinstance(user_name, str) and isinstance(pos, tuple):
            self.G_user_pos.update({user_name: pos})
        elif isinstance(user_name, list) and isinstance(pos, list):
            if len(user_name) == len(pos):
                self.G_user_pos.update({user_name: pos})
            else:
                raise IndexError("La taille de la list user doit correspondre à celle des poids.")

    @staticmethod
    def normalize(list_mapped: list, b2: int = 1, b1: int = 0) -> list:
        """Nomalise des valeurs entre max et inf pour la liste donnée"""
        a1 = np.min(list_mapped)
        a2 = np.max(list_mapped)
        return [b1+ ((x - a1) * (b2 - b1))/(a2 - a1) for x in list_mapped]