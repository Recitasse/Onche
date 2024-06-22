from dataclasses import dataclass, field, InitVar
from typing import Dict, List, Tuple, Union, ClassVar
from .Node import Node


@dataclass(init=True, slots=True)
class Edge:
    weight: float = field(default=1.0, init=True)
    liens: InitVar[List[Node]] = field(default=None, init=True)

    color: str = field(default="cyan", init=False)
    alpha: float = field(default=0.5, init=False)
    curvature: float = field(default=0.3, init=False)

    edges: dict = field(default=None, init=False)

    def __post_init__(self, liens: Tuple[Node, Tuple[Node]]) -> None:
        assert liens[1].__len__() >= 1, "Impossible d'ajouter moins de 1 noeud"
        self.edges.update({liens[0]: liens[1]})

    @property
    def poids(self) -> float:
        return self.weight

    @poids.setter
    def poids(self, val: float) -> None:
        self.weight = val

    @property
    def edge(self) -> Dict:
        return self.edges

    def __lt__(self, other: Union['Edge', float, int]) -> bool:
        """
        Compare le poids du lien
        :param other: Un autre lien ou une valeur
        :return: True si la taille du lien est moins grande que other
        """
        if isinstance(other, Edge):
            return self.weight < other.weight
        return self.weight < other

    def __le__(self, other: Union['Edge', float, int]) -> bool:
        """
        Compare le poids du lien
        :param other: Un autre lien ou une valeur
        :return: True si la taille du lien inférieur ou égale que other
        """
        if isinstance(other, Edge):
            return self.weight <= other.weight
        return self.weight <= other

    def __gt__(self, other: Union['Edge', float, int]) -> bool:
        """
        Compare le poids du lien
        :param other: Un autre lien ou une valeur
        :return: True si la taille du lien supérieur que other
        """
        if isinstance(other, Edge):
            return self.weight > other.weight
        return self.weight > other

    def __ge__(self, other: Union['Edge', float, int]) -> bool:
        """
        Compare le poids du lien
        :param other: Un autre lien ou une valeur
        :return: True si la taille du lien supérieur ou égale que other
        """
        if isinstance(other, Edge):
            return self.weight >= other.weight
        return self.weight >= other

    def __ne__(self, other: Union['Edge', float, int]) -> bool:
        """
        Compare le poids du lien
        :param other: Un autre lien ou une valeur
        :return: True si la taille est différente de other
        """
        if isinstance(other, Edge):
            return self.weight != other.weight
        return self.weight != other

    def __eq__(self, other: Union['Edge', float, int]) -> bool:
        """
        Compare le poids du lien
        :param other: Un autre lien ou une valeur
        :return: True si la taille est égale à other
        """
        if isinstance(other, Edge):
            return self.weight == other.weight
        return self.weight == other

    def __add__(self, other: Union['Edge', float, int]) -> float:
        """
        Ajoute la valeur du lien
        :param other: La valeur à ajouter
        :return: la somme des deux valeurs
        """
        if isinstance(other, Edge):
            return self.weight + other.weight
        return self.weight + other

    def __sub__(self, other: Union['Edge', float, int]) -> float:
        """
        Ajoute la valeur du lien
        :param other: La valeur à ajouter
        :return: la différence des deux valeurs
        """
        if isinstance(other, Edge):
            return self.weight - other.weight
        return self.weight - other

    def __mul__(self, other: Union['Edge', float, int]) -> float:
        """
        Ajoute la valeur du lien
        :param other: La valeur à ajouter
        :return: la multiplication des deux valeurs
        """
        if isinstance(other, Edge):
            return self.weight * other.weight
        return self.weight * other

    def __truediv__(self, other: Union['Edge', float, int]) -> float:
        """
        Ajoute la valeur du lien
        :param other: La valeur à ajouter
        :return: la division des deux valeurs
        """
        if isinstance(other, Edge):
            return self.weight / other.weight
        return self.weight / other

    def __pow__(self, other: Union['Edge', float, int]) -> float:
        """
        Ajoute la valeur du lien
        :param other: La valeur à ajouter
        :return: la puissance des deux valeurs
        """
        if isinstance(other, Edge):
            return self.weight ** other.weight
        return self.weight ** other

    def __iadd__(self, other: Union['Edge', float, int]) -> 'Edge':
        """
        Ajoute la valeur du lien
        :param other: La valeur à ajouter
        :return: update la valeur du lien
        """
        val_ = self.weight + other
        if isinstance(other, Edge):
            val_ = self.weight + other.weight
        self.weight = val_
        return self

    def __isub__(self, other: Union['Edge', float, int]) -> 'Edge':
        """
        Ajoute la valeur du lien
        :param other: La valeur à ajouter
        :return: update la valeur du lien
        """
        val_ = self.weight - other
        if isinstance(other, Edge):
            val_ = self.weight - other.weight
        self.weight = val_
        return self

    def __imul__(self, other: Union['Edge', float, int]) -> 'Edge':
        """
        Ajoute la valeur du lien
        :param other: La valeur à ajouter
        :return: update la valeur du lien
        """
        val_ = self.weight * other
        if isinstance(other, Edge):
            val_ = self.weight * other.weight
        self.weight = val_
        return self

    def __itruediv__(self, other: Union['Edge', float, int]) -> 'Edge':
        """
        Ajoute la valeur du lien
        :param other: La valeur à ajouter
        :return: update la valeur du lien
        """
        val_ = self.weight / other
        if isinstance(other, Edge):
            val_ = self.weight / other.weight
        self.weight = val_
        return self

    def __ipow__(self, other: Union['Edge', float, int]) -> 'Edge':
        """
        Ajoute la valeur du lien
        :param other: La valeur à ajouter
        :return: update la valeur du lien
        """
        val_ = self.weight ** other
        if isinstance(other, Edge):
            val_ = self.weight ** other.weight
        self.weight = val_
        return self
