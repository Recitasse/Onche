from typing import Any, Dict, Tuple, List
import math
from random import randint
from tkinter import Canvas as c

def center_node(pos: Tuple[int, int], size: float) -> List[Tuple[int, int]]:
    """
    Calcul le centre du noeud en fonction de sa taille
    :param pos: la position initial (x0, y0)
    :param size: la taille du noeud
    :return: La position centrée (xc, yc)
    """
    d = int(math.sqrt(2)/4 * size)
    return [(pos[0] - d, pos[1] + d), (pos[0] + d, pos[1] - d)]


def generate_center(xmax: int, ymax: int) -> Tuple[int, int]:
    """
    Génère les premières coordonnées
    :param xmax: Taille max en X
    :param ymax: Taille max en Y
    :return: Les coordonnées d'un point
    """
    return randint(0, xmax), randint(0, ymax)
