from getpass import getuser
from datetime import datetime
import json
import xml.etree.ElementTree as ET
import os
from pathlib import Path
from config.Variables.variables import *

def get_all_xml_files() -> list:
    files = os.listdir(CALICE)
    for file in files:
        if not Path(file).suffix == ".xml":
            raise AttributeError("Tous les fichiers dans le calice doivent être des xml")
    return files

def generate_dict_getter(xml_files: list[str]) -> dict:
    names = [file.split(".")[0] for file in xml_files]
    tmp_ = {f'{name}': {} for name in names}
    for file in xml_files:
        with open(f"{CALICE}{file}", 'r', encoding="utf-8") as f:
            root: ET.Element = ET.fromstring(f.read())

        els = root.findall(".//row/parser")
        jels = els
        for el in els:
            for jel in jels:
                if el.get('table') is None:
                    pass
                if jel.get('table') is None:
                    pass
                else:
                    if el.get('where') == jel.get('table'):
                        tmp_[el.get('where')].update({f'{el.get("name")}' : {'xpath': el.find('xpath').text,
                                       'clean': [{'abs': jel.text, 're': jel.get('re')} for jel in el.findall('clean')]}})
    return tmp_
def generate_profil_parser(mega_dict: dict) -> None:
    """Dans le where=profil"""
    print(json.dumps(mega_dict, indent=4))


files = get_all_xml_files()
mega_d = generate_dict_getter(files)
generate_profil_parser(mega_d)
