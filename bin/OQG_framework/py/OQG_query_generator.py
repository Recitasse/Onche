import os

from pathlib import Path

import xml.etree.ElementTree as ET

from config.Variables.variables import *
from bin.fonctions.xml_type_reader import get_config, get_default, get_type_from_dict


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

    def get_tables_from_name(self, name: str) -> dict:
        for table in self.root.findall(".//table"):
            if table.attrib:
                if table.attrib['name'] == name:
                    fields = []
                    for champ in table.findall('champ'):
                        field = {
                            'name': champ.text,
                            'type': champ.attrib.get('type'),
                            'Null': champ.attrib.get('Null'),
                            'Key': champ.attrib.get('Key', None),
                            'Default': champ.attrib.get('Default', None)
                        }
                        fields.append(field)
                    return {
                        'name': name,
                        'fields': fields
                    }
    def generate_queries_table(self, name: str) -> None:
        table_dict = self.get_tables_from_name(name)


if __name__ == "__main__":
    p = PythonQueryGenerator()
    p.generate_queries_table("onchois")
