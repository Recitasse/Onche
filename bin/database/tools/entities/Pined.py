"""==================================================
   Python class Pined générée par OQG BDD ENTITIES GENERATOR
   Author: raphael
   Model: Onche	 Version: 0.8.3
   Made by Recitasse 2024-06-02 15:25:10.043620
=================================================="""

import datetime

from dataclasses import dataclass, field

from bin.database.tools.selectors.selector_pined import PinedBdd


@dataclass(slots=True)
class Pined:
    id__: int = field(default=None)
    userid_: int = field(default=None)
    badgeid_: int = field(default=None)


    intern_link: PinedBdd = field(default_factory=PinedBdd, init=False)

    def __post_init__(self):
        self.intern_link = PinedBdd()


    @property
    def id_(self) -> int:
        return self.id__

    @property
    def userid(self) -> int:
        return self.userid_

    @property
    def badgeid(self) -> int:
        return self.badgeid_


    @userid.setter
    def userid(self, val: int) -> None:
        self.intern_link.update_pined_userid(self.id_, val)
        self.userid = val

    @badgeid.setter
    def badgeid(self, val: int) -> None:
        self.intern_link.update_pined_badgeid(self.id_, val)
        self.badgeid = val


