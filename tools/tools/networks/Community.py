from dataclasses import dataclass, field, InitVar
from typing import Dict, Tuple, List, Any, Union
from .Node import Node
from .Edge import Edge


@dataclass(slots=True)
class Community:
    # User parameter
    name: str = field(default="dummy", init=True)

    # Datas
    in_nodes: List[Node] = field(default=None, init=False)
    in_edges: List[Edge] = field(default=None, init=False)
    out_nodes: List[Node] = field(default=None, init=False)
    out_edges: List[Edge] = field(default=None, init=False)

    # Characteristics
    total_weight: float = field(default=0.0, init=False)

    def add_in_nodes(self, nodes_: List[Node]) -> None:
        """
        Ajoute des noeuds à la communauté
        :param nodes_: Liste des noeuds
        :return: None
        """
        for node in nodes_:
            if node not in self.in_nodes:
                self.in_nodes.append(node)
                self.total_weight += node.poids

    def delete_in_node(self, nodes_: List[Node]) -> None:
        """
        Enlève des noeuds de la communauté
        :param nodes_: Les noeuds à enlever
        :return: None
        """
        for node in nodes_:
            if node in self.in_nodes:
                self.in_nodes.remove(node)

    def delete_out_node(self, nodes_: List[Node]) -> None:
        """
        Enlève les noeuds de la communautés extérieurs
        :param nodes_: liste des noeuds externes à enlever
        :return: None
        """
        for node in nodes_:
            if node in self.out_nodes:
                self.out_nodes.remove(node)

    def add_in_edges(self, edges_: List[Edge]) -> None:
        """
        Ajoute des liens à la communauté
        :param edges_: List des liens intérieur
        :return: None
        """
        for edge in edges_:
            if edge not in self.in_edges:
                self.in_edges.append(edge)

    def delete_in_edge(self, edges_: List[Edge]) -> None:
        """
        Enlève des liens externes
        :param edges_: Liste des liens à enlever
        :return: None
        """
        for edge in edges_:
            if edge not in self.in_edges:
                self.in_edges.remove(edge)

    def delete_out_edge(self, edges_: List[Edge]) -> None:
        """
        Enlève des liens internes
        :param edges_: Liste des liens internes à enlever
        :return: None
        """
        for edge in edges_:
            if edge not in self.out_edges:
                self.out_edges.remove(edge)

    def add_out_nodes(self, nodes_: List[Node]) -> None:
        """
        Ajoute des noeuds externes à la communautés
        :param nodes_: Noeud externe
        :return: None
        """
        for node in nodes_:
            if node not in self.out_nodes:
                self.out_nodes.append(node)

    def add_out_edges(self, edges_: List[Edge]) -> None:
        """
        Ajoute des les liens avec les noeuds exterieur
        :param edges_: Liste des liens extérieur
        :return:
        """
        for edge in edges_:
            if edge not in self.in_edges:
                self.in_edges.append(edge)

    @property
    def total(self) -> float:
        return self.total_weight
