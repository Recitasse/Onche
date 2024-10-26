"""
==================================================
Python class Messages générée par OQG BDD ENTITIES GENERATOR
Author: recitasse
Model: Onche	 Version: 0.8.3
Made by Recitasse 2024-08-05 19:28:31.354658
==================================================
"""

import datetime

from dataclasses import dataclass, field


@dataclass(slots=True, order=False)
class Messages:
    id__: int = field(default=None)
    oid_: int = field(default=None)
    user_: int = field(default=None)
    message_: str = field(default="None")
    date_: datetime = field(default=datetime.date(year=2024, month=6, day=2))

    touser_: int = field(init=False, default=None)
    pemt_: int = field(init=False, default=None)
    answeroid_: int = field(init=False, default=None)

    intern_link: 'MessagesBdd' = field(init=False, default=None)

    def __post_init__(self):
        from ..selectors.selector_messages import MessagesBdd
        self.intern_link = MessagesBdd()


    @property
    def id_(self) -> int:
        return self.id__

    @property
    def oid(self) -> int:
        return self.oid_

    @property
    def user(self) -> int:
        return self.user_

    @property
    def message(self) -> str:
        return self.message_

    @property
    def touser(self) -> int:
        return self.touser_

    @property
    def pemt(self) -> int:
        return self.pemt_

    @property
    def answeroid(self) -> int:
        return self.answeroid_

    @property
    def date(self) -> datetime:
        return self.date_


    @oid.setter
    def oid(self, val: int) -> None:
        self.intern_link.update_messages_oid(self.id_, val)
        self.oid = val

    @user.setter
    def user(self, val: int) -> None:
        self.intern_link.update_messages_user(self.id_, val)
        self.user = val

    @message.setter
    def message(self, val: str) -> None:
        self.intern_link.update_messages_message(self.id_, val)
        self.message = val

    @touser.setter
    def touser(self, val: int) -> None:
        self.intern_link.update_messages_touser(self.id_, val)
        self.touser = val

    @pemt.setter
    def pemt(self, val: int) -> None:
        self.intern_link.update_messages_pemt(self.id_, val)
        self.pemt = val

    @answeroid.setter
    def answeroid(self, val: int) -> None:
        self.intern_link.update_messages_answeroid(self.id_, val)
        self.answeroid = val

    @date.setter
    def date(self, val: datetime) -> None:
        self.intern_link.update_messages_date(self.id_, val)
        self.date = val


