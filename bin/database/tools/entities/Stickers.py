"""==================================================
   Python class Stickers générée par OQG BDD ENTITIES GENERATOR
   Author: recitasse
   Model: Onche	 Version: 0.8.3
   Made by Recitasse 2024-06-04 18:36:52.149655
=================================================="""

import datetime

from dataclasses import dataclass, field


@dataclass(slots=True)
class Stickers:    id__: int = field(default=None)
    nom_: str = field(default="None")
    collection_: int = field(default=None)


    intern_link: 'StickersBdd' = field(init=False, default=None)

    def __post_init__(self):
        from bin.database.tools.selectors.selector_stickers import StickersBdd
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


