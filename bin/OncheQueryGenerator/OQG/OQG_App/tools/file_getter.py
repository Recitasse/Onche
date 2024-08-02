from os import listdir
from pathlib import Path
from config.variables import CALICE
from typing import List


def get_all_xml_files() -> List[str]:
    files = listdir(CALICE)
    for file in files:
        if not Path(file).suffix == ".xml":
            raise AttributeError("Tous les fichiers dans le calice doivent être des xml")
    return files


def uppercase_first(text: str) -> str:
    """
    Renvoie le même string avec la première lettre en maj
    """
    return text[0].upper() + text[1:].lower()


def set_title(text: str) -> str:
    """
    Renvoie le même texte mais sous format de titre
    """
    text = text.lower()
    text = text.replace(' ', '-')
    return text
