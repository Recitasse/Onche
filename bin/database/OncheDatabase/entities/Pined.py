"""
==================================================
Python class Pined générée par OQG BDD ENTITIES GENERATOR
Author: recitasse
Model: Onche	 Version: 0.8.3
Made by Recitasse 2024-08-05 19:28:31.354198
==================================================
"""

import datetime

from dataclasses import dataclass, field


@dataclass(slots=True, order=False)
class Pined:
    id__: int = field(default=None)
    userid_: int = field(default=None)
    badgeid_: int = field(default=None)


    intern_link: 'PinedBdd' = field(init=False, default=None)

    def __post_init__(self):
        from ..selectors.selector_pined import PinedBdd
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


