import os
from pathlib import Path
from getpass import getuser
from datetime import datetime
import xml.etree.ElementTree as ET

from OQG_bdd_generator import get_all_xml_files
from config.Variables.variables import *


def GenerateImportFunctions(table: str) -> str:
    first_table = table
    table = table[0].upper() + table[1:].lower()
    python_code = '"""==================================================\n'
    python_code += f"   Python class {table} générée par OQG BDD ENTITIES GENERATOR\n"
    python_code += f"   Author: {getuser()}\n"
    python_code += f"   Model: Onche\t Version: {VERSION}\n"
    python_code += f"   Made by Recitasse {datetime.now()}\n"
    python_code += '=================================================="""\n\n'
    python_code += f"import datetime\n\nfrom dataclasses import dataclass, field\n\n\n"
    python_code += f"@dataclass(slots=True)\nclass {table}:"
    return python_code

def GenerateValuesFunctions(root: ET.Element, table: str) -> str:
    first_table = table
    table = table[0].upper() + table[1:].lower()
    tab = "    "
    python_code = ""
    infos = []
    rows = root.findall(".//row[@null='False']")
    for row in rows:
        infos.append([row.get('name'), row.get('type'), row.get('default')])

    for info in infos:
        l_ = ""
        r_ = ""
        def_ = info[2]
        if info[0] == "id":
            info[0] += "_"
        if info[1] == "str":
            l_ = '"'
            r_ = '"'
        if info[1] == "datetime":
            def_ = 'datetime.date(year=2024, month=6, day=2)'

        python_code += f"{tab}{info[0]}_: {info[1]} = field(default={l_}{def_}{r_})\n"

    python_code += "\n"
    infos = []
    rows = root.findall(".//row[@null='True']")
    for row in rows:
        infos.append([row.get('name'), row.get('type'), row.get('default')])

    for info in infos:
        l_ = ""
        r_ = ""
        def_ = info[2]
        if info[0] == "id":
            info[0] += "_"
        if info[1] == "str":
            l_ = '"'
            r_ = '"'
        if info[1] == "datetime":
            def_ = 'datetime.date(year=2024, month=6, day=2)'

        python_code += f"{tab}{info[0]}_: {info[1]} = field(init=False, default={l_}{def_}{r_})\n"

    python_code += "\n"
    python_code += f"{tab}intern_link: '{table}Bdd' = field(init=False, default=None)\n\n"
    python_code += f"{tab}def __post_init__(self):\n"
    python_code += f"{tab*2}from bin.database.tools.selectors.selector_{first_table} import {table}Bdd\n"
    python_code += f"{tab*2}self.intern_link = {table}Bdd()\n\n"

    return python_code

def GeneratePropertiesFunc(root: ET.Element, table: str) -> str:
    first_table = table
    table = table[0].upper() + table[1:].lower()
    tab = "    "
    python_code = ""
    infos = []
    rows = root.findall(".//row")
    for row in rows:
        infos.append([row.get('name'), row.get('type')])

    for info in infos:
        if info[0] == "id":
            info[0] += "_"
        python_code += f"{tab}@property\n"
        python_code += f"{tab}def {info[0]}(self) -> {info[1]}:\n"
        python_code += f"{tab*2}return self.{info[0]}_\n\n"

    return python_code

def GenerateSettersFunctions(root: ET.Element, table: str):
    first_table = table
    table = table[0].upper() + table[1:].lower()
    tab = "    "
    python_code = ""
    infos = []
    rows = root.findall(".//row")
    for row in rows:
        infos.append([row.get('name'), row.get('type')])

    primary_key = root.find('.//primary-key')
    tmp_ = []
    if primary_key is not None:
        tmp_ = [primary_key.get('name'), primary_key.get('type')]

    for info in infos:
        if info[0] != tmp_[0]:
            python_code += f"{tab}@{info[0]}.setter\n"
            python_code += f"{tab}def {info[0]}(self, val: {info[1]}) -> None:\n"
            python_code += f"{tab*2}self.intern_link.update_{first_table}_{info[0]}(self.{tmp_[0]}_, val)\n"
            python_code += f"{tab*2}self.{info[0]} = val\n\n"

    return python_code

if __name__ == "__main__":
    files = get_all_xml_files()
    for file in files:
        glb_str = ""
        with open(f"{CALICE}{file}", 'r', encoding="utf-8") as conf:
            root: ET.Element = ET.fromstring(conf.read())
        table_name = root.attrib['table']
        name = table_name[0].upper() + table_name[1:].lower()
        if os.path.exists(f"{GLOBAL_PATH}bin/database/entities/{name}.py"):
            os.remove(f"{GLOBAL_PATH}bin/database/entities/{name}.py")

        glb_str += GenerateImportFunctions(table_name)
        glb_str += "\n"
        glb_str += GenerateValuesFunctions(root, table_name)
        glb_str += "\n"
        glb_str += GeneratePropertiesFunc(root, table_name)
        glb_str += "\n"
        glb_str += GenerateSettersFunctions(root, table_name)
        glb_str += "\n"

        with open(f"{GLOBAL_PATH}bin/database/tools/entities/{name}.py", 'w', encoding="utf-8") as f:
            f.write(glb_str)
