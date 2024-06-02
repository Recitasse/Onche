"""==================================================
   Python class Stickers générée par OQG BDD ENTITIES GENERATOR
   Author: raphael
   Model: Onche	 Version: 0.8.3
   Made by Recitasse 2024-06-02 15:25:10.042924
=================================================="""

import datetime

from dataclasses import dataclass, field

from bin.database.tools.selectors.selector_stickers import StickersBdd


@dataclass(slots=True)
class Stickers:
    id__: int = field(default=None)
    nom_: str = field(default="None")
    collection_: int = field(default=None)


    intern_link: StickersBdd = field(default_factory=StickersBdd, init=False)

    def __post_init__(self):
        self.intern_link = StickersBdd()


    @property
    def id_(self) -> int:
        return self.id__

    @property
    def nom(self) -> str:
        return self.nom_

    @property
    def collection(self) -> int:
        return self.collection_


    @nom.setter
    def nom(self, val: str) -> None:
        self.intern_link.update_stickers_nom(self.id_, val)
        self.nom = val

    @collection.setter
    def collection(self, val: int) -> None:
        self.intern_link.update_stickers_collection(self.id_, val)
        self.collection = val


