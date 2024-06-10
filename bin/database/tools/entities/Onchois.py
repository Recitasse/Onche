"""==================================================
   Python class Onchois générée par OQG BDD ENTITIES GENERATOR
   Author: recitasse
   Model: Onche	 Version: 0.8.3
   Made by Recitasse 2024-06-05 18:11:12.350439
=================================================="""

import datetime

from dataclasses import dataclass, field


@dataclass(slots=True)
class Onchois:
    id__: int = field(default=None)
    ban_: int = field(default=0)
    niveau_: int = field(default=1)
    nom_: str = field(default="None")
    message_: int = field(default=0)
    date_: datetime = field(default=datetime.date(year=2024, month=6, day=2))

    sexe_: str = field(init=False, default="None")
    age_: int = field(init=False, default=None)
    qualite_: int = field(init=False, default=5)
    pos_: int = field(init=False, default=None)
    neg_: int = field(init=False, default=None)
    neu_: int = field(init=False, default=None)

    intern_link: 'OnchoisBdd' = field(init=False, default=None)

    def __post_init__(self):
        from bin.database.tools.selectors.selector_onchois import OnchoisBdd
        self.intern_link = OnchoisBdd()


    @property
    def id_(self) -> int:
        return self.id__

    @property
    def ban(self) -> int:
        return self.ban_

    @property
    def niveau(self) -> int:
        return self.niveau_

    @property
    def nom(self) -> str:
        return self.nom_

    @property
    def sexe(self) -> str:
        return self.sexe_

    @property
    def age(self) -> int:
        return self.age_

    @property
    def qualite(self) -> int:
        return self.qualite_

    @property
    def pos(self) -> int:
        return self.pos_

    @property
    def neg(self) -> int:
        return self.neg_

    @property
    def neu(self) -> int:
        return self.neu_

    @property
    def message(self) -> int:
        return self.message_

    @property
    def date(self) -> datetime:
        return self.date_


    @ban.setter
    def ban(self, val: int) -> None:
        self.intern_link.update_onchois_ban(self.id_, val)
        self.ban = val

    @niveau.setter
    def niveau(self, val: int) -> None:
        self.intern_link.update_onchois_niveau(self.id_, val)
        self.niveau = val

    @nom.setter
    def nom(self, val: str) -> None:
        self.intern_link.update_onchois_nom(self.id_, val)
        self.nom = val

    @sexe.setter
    def sexe(self, val: str) -> None:
        self.intern_link.update_onchois_sexe(self.id_, val)
        self.sexe = val

    @age.setter
    def age(self, val: int) -> None:
        self.intern_link.update_onchois_age(self.id_, val)
        self.age = val

    @qualite.setter
    def qualite(self, val: int) -> None:
        self.intern_link.update_onchois_qualite(self.id_, val)
        self.qualite = val

    @pos.setter
    def pos(self, val: int) -> None:
        self.intern_link.update_onchois_pos(self.id_, val)
        self.pos = val

    @neg.setter
    def neg(self, val: int) -> None:
        self.intern_link.update_onchois_neg(self.id_, val)
        self.neg = val

    @neu.setter
    def neu(self, val: int) -> None:
        self.intern_link.update_onchois_neu(self.id_, val)
        self.neu = val

    @message.setter
    def message(self, val: int) -> None:
        self.intern_link.update_onchois_message(self.id_, val)
        self.message = val

    @date.setter
    def date(self, val: datetime) -> None:
        self.intern_link.update_onchois_date(self.id_, val)
        self.date = val


