"""==================================================
   Python class Onchois générée par OQG BDD ENTITIES GENERATOR
   Author: raphael
   Model: Onche	 Version: 0.8.3
   Made by Recitasse 2024-06-02 15:25:10.043776
=================================================="""

import datetime

from dataclasses import dataclass, field

from bin.database.tools.selectors.selector_onchois import OnchoisBdd


@dataclass(slots=True)
class Onchois:
    id__: int = field(default=None)
    oid_: int = field(default=None)
    niveau_: int = field(default=1)
    nom_: str = field(default="None")
    message_: int = field(default=0)
    date_: datetime = field(default=datetime.date(year=2024, month=6, day=2))

    sexe_: str = field(init=False, default="None")
    age_: int = field(init=False, default=None)
    qualite_: int = field(init=False, default=5)

    intern_link: OnchoisBdd = field(default_factory=OnchoisBdd, init=False)

    def __post_init__(self):
        self.intern_link = OnchoisBdd()


    @property
    def id_(self) -> int:
        return self.id__

    @property
    def oid(self) -> int:
        return self.oid_

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
    def message(self) -> int:
        return self.message_

    @property
    def date(self) -> datetime:
        return self.date_


    @oid.setter
    def oid(self, val: int) -> None:
        self.intern_link.update_onchois_oid(self.id_, val)
        self.oid = val

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

    @message.setter
    def message(self, val: int) -> None:
        self.intern_link.update_onchois_message(self.id_, val)
        self.message = val

    @date.setter
    def date(self, val: datetime) -> None:
        self.intern_link.update_onchois_date(self.id_, val)
        self.date = val


