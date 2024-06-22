from dataclasses import dataclass, field, InitVar
from typing import Dict, List, Tuple, Union, ClassVar
from tools.tools.networks.visual.graphic import Graphic
from random import randint


@dataclass(init=True, slots=True)
class Node:
    weight: float = field(default=1.0, init=True)
    name: str = field(default="", init=True)

    positions: Tuple[int, int] = field(default=None, init=False)
    color: str = field(default="blue", init=False)
    alpha: float = field(default=0.8, init=False)

    id__: int = field(default=1, init=False)

    NodeId: ClassVar[int] = 0

    def __post_init__(self) -> None:
        Node.NodeId += 1
        self.id__ = Node.NodeId
        self.positions = (randint(0, Graphic.size[0]), randint(0, Graphic.size[1]))

    @property
    def id_(self) -> int:
        return self.id__

    @property
    def poids(self) -> float:
        return self.weight

    @poids.setter
    def poids(self, val: Union[int, float]) -> None:
        self.weight = val

    @property
    def nom(self) -> str:
        return self.name

    @nom.setter
    def nom(self, val: str) -> None:
        self.name = val

    @property
    def noeud(self) -> Tuple[float, str]:
        return self.weight, self.name

    @property
    def position(self) -> Tuple[int, int]:
        return self.positions

    @position.setter
    def position(self, val: Tuple[int, int]) -> None:
        self.positions = val

    @classmethod
    def reset_ids(cls) -> None:
        cls.NodeId = 0

    def __lt__(self, other: Union['Node', float, int]) -> bool:
        """
        Compare le poids du noeud
        :param other: Un autre noeud ou une valeur
        :return: True si la taille du noeud est moins grande que other
        """
        if isinstance(other, Node):
            return self.weight < other.weight
        return self.weight < other

    def __le__(self, other: Union['Node', float, int]) -> bool:
        """
        Compare le poids du noeud
        :param other: Un autre noeud ou une valeur
        :return: True si la taille du noeud inférieur ou égale que other
        """
        if isinstance(other, Node):
            return self.weight <= other.weight
        return self.weight <= other

    def __gt__(self, other: Union['Node', float, int]) -> bool:
        """
        Compare le poids du noeud
        :param other: Un autre noeud ou une valeur
        :return: True si la taille du noeud supérieur que other
        """
        if isinstance(other, Node):
            return self.weight > other.weight
        return self.weight > other

    def __ge__(self, other: Union['Node', float, int]) -> bool:
        """
        Compare le poids du noeud
        :param other: Un autre noeud ou une valeur
        :return: True si la taille du noeud supérieur ou égale que other
        """
        if isinstance(other, Node):
            return self.weight >= other.weight
        return self.weight >= other

    def __ne__(self, other: Union['Node', float, int]) -> bool:
        """
        Compare le poids du noeud
        :param other: Un autre noeud ou une valeur
        :return: True si la taille est différente de other
        """
        if isinstance(other, Node):
            return self.weight != other.weight
        return self.weight != other

    def __add__(self, other: Union['Node', float, int]) -> float:
        """
        Ajoute la valeur du noeud
        :param other: La valeur à ajouter
        :return: la somme des deux valeurs
        """
        if isinstance(other, Node):
            return self.weight + other.weight
        return self.weight + other

    def __sub__(self, other: Union['Node', float, int]) -> float:
        """
        Ajoute la valeur du noeud
        :param other: La valeur à ajouter
        :return: la différence des deux valeurs
        """
        if isinstance(other, Node):
            return self.weight - other.weight
        return self.weight - other

    def __mul__(self, other: Union['Node', float, int]) -> float:
        """
        Ajoute la valeur du noeud
        :param other: La valeur à ajouter
        :return: la multiplication des deux valeurs
        """
        if isinstance(other, Node):
            return self.weight * other.weight
        return self.weight * other

    def __truediv__(self, other: Union['Node', float, int]) -> float:
        """
        Ajoute la valeur du noeud
        :param other: La valeur à ajouter
        :return: la division des deux valeurs
        """
        if isinstance(other, Node):
            return self.weight / other.weight
        return self.weight / other

    def __pow__(self, other: Union['Node', float, int]) -> float:
        """
        Ajoute la valeur du noeud
        :param other: La valeur à ajouter
        :return: la puissance des deux valeurs
        """
        if isinstance(other, Node):
            return self.weight ** other.weight
        return self.weight ** other

    def __iadd__(self, other: Union['Node', float, int]) -> 'Node':
        """
        Ajoute la valeur du noeud
        :param other: La valeur à ajouter
        :return: update la valeur du noeud
        """
        if isinstance(other, Node):
            val_ = self.weight + other.weight
        else:
            val_ = self.weight + other
        self.weight = val_
        return self

    def __isub__(self, other: Union['Node', float, int]) -> 'Node':
        """
        Ajoute la valeur du noeud
        :param other: La valeur à ajouter
        :return: update la valeur du noeud
        """
        if isinstance(other, Node):
            val_ = self.weight - other.weight
        else:
            val_ = self.weight - other
        self.weight = val_
        return self

    def __imul__(self, other: Union['Node', float, int]) -> 'Node':
        """
        Ajoute la valeur du noeud
        :param other: La valeur à ajouter
        :return: update la valeur du noeud
        """
        if isinstance(other, Node):
            val_ = self.weight * other.weight
        else:
            val_ = self.weight * other
        self.weight = val_
        return self

    def __itruediv__(self, other: Union['Node', float, int]) -> 'Node':
        """
        Ajoute la valeur du noeud
        :param other: La valeur à ajouter
        :return: update la valeur du noeud
        """
        if isinstance(other, Node):
            val_ = self.weight / other.weight
        else:
            val_ = self.weight / other
        self.weight = val_
        return self

    def __ipow__(self, other: Union['Node', float, int]) -> 'Node':
        """
        Ajoute la valeur du noeud
        :param other: La valeur à ajouter
        :return: update la valeur du noeud
        """
        if isinstance(other, Node):
            val_ = self.weight ** other.weight
        else:
            val_ = self.weight ** other
        self.weight = val_
        return self

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.id_ == other.id_
        return False

    def __hash__(self):
        return hash(self.id_)