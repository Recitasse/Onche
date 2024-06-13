import os

from pathlib import Path

import xml.etree.ElementTree as ET

from config.variables import *


class PythonQueryGenerator:
    def __init__(self, path: str = "bin/OQG_Types/Forum/bdd_metadata.xml") -> None:
        self.pwd = f"{GLOBAL_PATH}bin/OQG_Operator/"
        self.path_file = f'{GLOBAL_PATH}{path}'

        self.__create_root()
        self.__redo_install()

    def __create_root(self) -> None:
        """Créer l'élément root pour le parse du xml"""
        if Path(self.path_file).exists():
            self.tree = ET.parse(self.path_file)
            self.__locate_root()
            return
        raise FileNotFoundError(f"Le fichier {self.path_file} n'existe pas.")

    def __redo_install(self) -> None:
        files_ = os.listdir(self.pwd)
        for file_ in files_:
            if len(file_.split("_queries"))>1:
                print(f"Fichier {os.path.join(self.pwd, file_)} supprimé")
                os.remove(os.path.join(self.pwd, file_))

    def __locate_root(self) -> None:
        self.root = self.tree.getroot()
        self.root = self.root.find(".//tables")

    def get_tables(self) -> dict:
        for table in self.root.findall(".//table"):
            print(table)


if __name__ == "__main__":
    p = PythonQueryGenerator()
    p.get_tables()
