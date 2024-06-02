"""==================================================
   Python class Badges générée par OQG BDD ENTITIES GENERATOR
   Author: raphael
   Model: Onche	 Version: 0.8.3
   Made by Recitasse 2024-06-02 15:25:10.043296
=================================================="""

import datetime

from dataclasses import dataclass, field

from bin.database.tools.selectors.selector_badges import BadgesBdd


@dataclass(slots=True)
class Badges:
    id__: int = field(default=None)
    nom_: str = field(default="None")


    intern_link: BadgesBdd = field(default_factory=BadgesBdd, init=False)

    def __post_init__(self):
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


