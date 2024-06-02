"""==================================================
   Python class Topic générée par OQG BDD ENTITIES GENERATOR
   Author: raphael
   Model: Onche	 Version: 0.8.3
   Made by Recitasse 2024-06-02 15:25:10.043462
=================================================="""

import datetime

from dataclasses import dataclass, field

from bin.database.tools.selectors.selector_topic import TopicBdd


@dataclass(slots=True)
class Topic:
    id__: int = field(default=None)
    oid_: int = field(default=None)
    operateur_: int = field(default=None)
    nom_: str = field(default="None")
    date_: datetime = field(default=datetime.date(year=2024, month=6, day=2))
    message_: int = field(default=None)
    lien_: str = field(default="None")
    forum_: int = field(default=None)


    intern_link: TopicBdd = field(default_factory=TopicBdd, init=False)

    def __post_init__(self):
        self.intern_link = TopicBdd()


    @property
    def id_(self) -> int:
        return self.id__

    @property
    def oid(self) -> int:
        return self.oid_

    @property
    def operateur(self) -> int:
        return self.operateur_

    @property
    def nom(self) -> str:
        return self.nom_

    @property
    def date(self) -> datetime:
        return self.date_

    @property
    def message(self) -> int:
        return self.message_

    @property
    def lien(self) -> str:
        return self.lien_

    @property
    def forum(self) -> int:
        return self.forum_


    @oid.setter
    def oid(self, val: int) -> None:
        self.intern_link.update_topic_oid(self.id_, val)
        self.oid = val

    @operateur.setter
    def operateur(self, val: int) -> None:
        self.intern_link.update_topic_operateur(self.id_, val)
        self.operateur = val

    @nom.setter
    def nom(self, val: str) -> None:
        self.intern_link.update_topic_nom(self.id_, val)
        self.nom = val

    @date.setter
    def date(self, val: datetime) -> None:
        self.intern_link.update_topic_date(self.id_, val)
        self.date = val

    @message.setter
    def message(self, val: int) -> None:
        self.intern_link.update_topic_message(self.id_, val)
        self.message = val

    @lien.setter
    def lien(self, val: str) -> None:
        self.intern_link.update_topic_lien(self.id_, val)
        self.lien = val

    @forum.setter
    def forum(self, val: int) -> None:
        self.intern_link.update_topic_forum(self.id_, val)
        self.forum = val


