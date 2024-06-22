from dataclasses import dataclass, InitVar, field
from typing import Dict, Tuple, Any


@dataclass
class BiDict(dict):

    def update(self, *args, **kwargs):
        nargs: dict = args[0]
        for key, value in nargs.items():
            self.__setitem__(key, value)

        for key, value in kwargs.items():
            self.__setitem__(key, value)

    def pop(self, __key):
        self.__delitem__(__key)

    def __setitem__(self, key, value):
        if key in self and self[key] != value:
            raise ValueError(f"Clé {key} déjà présente avec une valeur différente.")
        if value in self and self[value] != key:
            raise ValueError(f"Valeur {value} déjà présente comme clé avec une valeur différente.")
        super().__setitem__(key, value)
        super().__setitem__(value, key)

    def __getitem__(self, item) -> Tuple[Any, Any]:
        if item not in self:
            raise ValueError(f"{item} n'est pas dans le dictionnaire")
        val = super().__getitem__(item)
        return super().__getitem__(item), super().__getitem__(val)

    def __delitem__(self, item) -> None:
        x, y = self.__getitem__(item)
        super().__delitem__(x)
        super().__delitem__(y)

    def __str__(self) -> str:
        return "{" + ", ".join(f"{self.__type(key)}: {self.__type(val)}" for key, val in self.items()) + "}"

    def __type(self, val: Any) -> str:
        """
        Obtient le type et accomode le string pour la méthode __str__
        :param val: Valeur à sépcifier
        :return: le string de la méthode
        """
        if isinstance(val, str):
            return f"'{val}'"
        return val
