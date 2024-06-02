"""==================================================
   Python class Messages générée par OQG BDD ENTITIES GENERATOR
   Author: raphael
   Model: Onche	 Version: 0.8.3
   Made by Recitasse 2024-06-02 15:25:10.043952
=================================================="""

import datetime

from dataclasses import dataclass, field

from bin.database.tools.selectors.selector_messages import MessagesBdd


@dataclass(slots=True)
class Messages:
    id__: int = field(default=None)
    oid_: int = field(default=None)
    user_: int = field(default=None)
    topic_: int = field(default=None)
    message_: str = field(default="None")
    date_: datetime = field(default=datetime.date(year=2024, month=6, day=2))

    touser_: int = field(init=False, default=None)

    intern_link: MessagesBdd = field(default_factory=MessagesBdd, init=False)

    def __post_init__(self):
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
    def topic(self) -> int:
        return self.topic_

    @property
    def message(self) -> str:
        return self.message_

    @property
    def touser(self) -> int:
        return self.touser_

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

    @topic.setter
    def topic(self, val: int) -> None:
        self.intern_link.update_messages_topic(self.id_, val)
        self.topic = val

    @message.setter
    def message(self, val: str) -> None:
        self.intern_link.update_messages_message(self.id_, val)
        self.message = val

    @touser.setter
    def touser(self, val: int) -> None:
        self.intern_link.update_messages_touser(self.id_, val)
        self.touser = val

    @date.setter
    def date(self, val: datetime) -> None:
        self.intern_link.update_messages_date(self.id_, val)
        self.date = val


