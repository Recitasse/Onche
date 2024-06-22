from networkx import Graph, draw, draw_networkx_nodes, get_node_attributes, draw_networkx_labels
import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass, field, InitVar
from typing import Any, Tuple, List, ClassVar


@dataclass(init=True, repr=False, order=False)
class Graphic(Graph):
    titre: str = field(default="Graphique des communautés", init=True)

    size: ClassVar[Tuple[int, int]] = (800, 600)

    @property
    def resolution(self) -> Tuple[int, int]:
        return self.size

    @resolution.setter
    def resolution(self, size: Tuple[int, int]) -> None:
        Graphic.size = size
