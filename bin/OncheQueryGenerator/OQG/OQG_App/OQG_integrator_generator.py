import datetime
import json
import time
from os import path
from config.variables import CALICE, GLOBAL_PATH
import xml.etree.ElementTree as ET
from bin.OncheQueryGenerator.OQG.OQG_App.tools.file_getter import get_all_xml_files, uppercase_first


def generate_JSON_infos() -> dict:
    """
    Renvoie la liste des based_url, ce sur quoi le parser sera généré
    """
    all_ = {}
    files = get_all_xml_files()
    for file in files:
        collector_name = file.split(".")[0]
        all_.update({collector_name: {}})
        tree = ET.parse(path.join(CALICE, file))
        root = tree.getroot()
        for row in root.findall('.//row'):
            if row.find('parser').get('where') == collector_name:
                all_[collector_name].update({row.get("name"): {"py-type": row.get("type"), "default": row.get("default")}})
    return all_


def generate_integrator(name_file: str, JSON: dict):
    tab = "    "
    glb = "from datetime import datetime\n"
    glb += "from dataclasses import dataclass\n"
    glb += "from bin.database.OncheDatabase.link.link import Link\n\n\n"

    glb += "@dataclass(init=False)\n"
    glb += f"class {uppercase_first(name_file)}Integrator(Link):\n"

    tmp_ = []; tmpn_ = []
    for key, value in JSON[name_file].items():
        tmpn_.append(key)
        tmp_.append(f"{key}: {value['py-type']} = {value['default'] if value['default'] != 'CURRENT_TIMESTAMP(2)' else None}")
    glb += f"{tab}def insert_{name_file}(self, {', '.join(tmp_)}) -> None:\n"
    glb += f"{2*tab}query = 'INSERT INTO {name_file} ({', '.join(tmpn_)}) VALUES ({', '.join(['%s'] * JSON[name_file].items().__len__())})'\n"
    glb += f"{2*tab}params = ({', '.join(tmpn_)})\n"
    glb += f"{2*tab}self.QUERY(query=query, values=params)\n"

    return glb


def write_file() -> None:
    JSON = generate_JSON_infos()
    for name in JSON.keys():
        with open(path.join(GLOBAL_PATH, f"bin/database/OncheDatabase/integrator/{name}.py"), "w", encoding="utf-8") as rew:
            rew.write(generate_integrator(name, JSON))

write_file()