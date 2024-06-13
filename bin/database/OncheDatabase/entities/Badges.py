"""
==================================================
Python class Badges générée par OncheQueryGenerator BDD ENTITIES GENERATOR
Author: recitasse
Model: Onche	 Version: 0.8.3
Made by Recitasse 2024-06-13 20:34:24.350745
==================================================
"""

import datetime

from dataclasses import dataclass, field


@dataclass(slots=True, order=False)
class Badges:
    id__: int = field(default=None)
    nom_: str = field(default="None")


    intern_link: 'BadgesBdd' = field(init=False, default=None)

    def __post_init__(self):
        from ..selectors.selector_badges import BadgesBdd
        self.intern_link = BadgesBdd()


    @property
    def id_(self) -> int:
        return self.id__

    @property
    def nom(self) -> str:
        return self.nom_


    @nom.setter
    def nom(self, val: str) -> None:
        self.intern_link.update_badges_nom(self.id_, val)
        self.nom = val


