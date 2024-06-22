from dataclasses import dataclass, field, InitVar
from typing import Any, List, Dict, Tuple
from utils.bidict.bidict import BiDict
from ..Edge import Edge
from ..Node import Node


@dataclass(init=True, order=True, slots=True)
class CommunityLouvain:



    _A: List[List, ...] = None
    _m: float = 0.0