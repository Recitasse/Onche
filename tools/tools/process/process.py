from dataclasses import dataclass, field
from typing import Union
from pathlib import Path


@dataclass(init=True, order=False, slots=True)
class Process:
    name: str = field(default="dummy", init=True)
    pid_: Union[None, int] = field(default=None, init=False)
    command: str = field(default="dummy_com", init=True)
    is_script: bool = field(default=False, init=True, kw_only=True)
    _running: bool = field(default=False, init=False)

    def __post_init__(self) -> None:
        if self.is_script:
            path = Path(self.command)
            if not (path.exists() and (path.suffix == '.sh' or path.suffix == '.bat')):
                raise ValueError(f"Le fichier n'existe pas ou n'est pas au bon format : {self.command}")

    @property
    def pid(self) -> Union[None, int]:
        return self.pid_

    @pid.setter
    def pid(self, val: int) -> None:
        self.pid_ = val

    def __repr__(self) -> str:
        """
        Représentation du processus
        :return:
        """
        return (f"{self.name}\t : {self.pid}\t {self._running}"
                f"{'is script' if self.is_script else self.command}\n")
