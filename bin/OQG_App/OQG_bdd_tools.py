from getpass import getuser
from datetime import datetime
import xml.etree.ElementTree as ET

from config.Variables.variables import *


def InternChecker(root: ET.Element) -> str:
    if root.find(".//index/primary-key") is not None:
        check = root.find(".//index/primary-key").get('name')
        return f'is_in_{check}({unformat_und(check)})'
    return ''

def CheckValue(root: ET.Element) -> list:
    if root.find(".//index/primary-key") is not None:
        return [root.find(".//index/primary-key").get('name'), root.find(".//index/primary-key").get('type')]
    return []

def GenerateImportQueries(table: str) -> str:
    table = table[0].upper() + table[1:].lower()
    python_code = '"""==================================================\n'
    python_code += f"   Python class {table}Bdd générée par OQG BDD TOOLS GENERATOR\n"
    python_code += f"   Author: {getuser()}\n"
    python_code += f"   Model: Onche\t Version: {VERSION}\n"
    python_code += f"   Made by Recitasse {datetime.now()}\n"
    python_code += '=================================================="""\n\n'
    python_code += f"import datetime\n\nfrom dataclasses import dataclass\n\nfrom bin.database.tools.entities.{table} import {table}\n\nfrom bin.database.bbd import Link\n\n\n"
    python_code += f"@dataclass(init=False)\nclass {table}Bdd(Link):\n"
    return python_code

def format_und(text: str) -> str:
    if text[-1] == "_":
        return text[:-1]
    return text

def unformat_und(text: str) -> str:
    if text == "id":
        return "id_"
    return text

def GenerateIsFunctions(root: ET.Element, table: str) -> str:
    first_table = table
    table = table[0].upper() + table[1:].lower()
    python_code = ""
    tab = "    "
    unic_indexes = []
    primary_key = root.find('.//primary-key')
    if primary_key is not None:
        unic_indexes.append({'name': f"{primary_key.get('name')}_", 'type': primary_key.get('type')})

    unique_index = root.findall('.//unic-index/name')
    for idx in unique_index:
        unic_indexes.append({'name': idx.text, 'type': idx.get('type')})

    for el in unic_indexes:
        python_code += f"{tab}def is_in_{format_und(el['name'])}(self, {el['name']}: {el['type']}) -> bool:\n"
        python_code += f'{tab*2}query = "SELECT * FROM {first_table} WHERE {first_table}_{format_und(el["name"])} = %s;"\n'
        python_code += f'{tab*2}params = ({el["name"]},)\n{tab*2}try:\n'
        python_code += f"{tab*3}if self.get_results(query, params):\n"
        python_code += f"{tab*4}self._logger.info(f'{first_table} {{{el['name']}}} existe')\n"
        python_code += f"{tab*4}return True\n"
        python_code += f"{tab*2}except Exception as e:\n"
        python_code += f"{tab*3}self._logger.error(f'Une erreur MySQL est survenue : {{e}}')\n"
        python_code += f"""{tab*2}self._logger.info(f"{table} {{{el['name']}}} n'est pas dans la base de donnée.")\n"""
        python_code += f"{tab*2}return False\n\n"
    return python_code + "\n"

def GenerateAddFunctions(root: ET.Element, table: str):
    rows = root.findall(".//row[@null='False']")
    first_table = table
    python_code = ""
    tab = "    "
    infos = []
    for row in rows:
        infos.append([row.get('name'), row.get('type')])

    all_params = ', '.join([f'{first_table}_{info[0]}' for info in infos[1:]])
    params = ', '.join([info[0] for info in infos[1:]])

    python_code += f"{tab}def add_{first_table}(self, {', '.join([': '.join(info) for info in infos[1:]])}) -> None:\n"
    python_code += f"{tab*2}query = 'INSERT INTO {first_table} ({all_params});'\n"
    python_code += f"{tab*2}params = ({params},)\n"
    python_code += f"{tab*2}if not self.is_in_{infos[1][0]}({infos[1][0]}):\n"
    python_code += f"{tab*3}cursor = self.connexion.cursor()\n{tab*3}try:\n"
    python_code += f"{tab*4}cursor.execute(query, params)\n"
    python_code += f"{tab*4}self.connexion.commit()\n"
    python_code += f"{tab*4}self._logger.info(f'{first_table} {{{unformat_und(infos[1][0])}}} existe')\n"
    python_code += f"{tab*3}except Exception as e:\n"
    python_code += f"{tab*4}self._logger.error(f'Une erreur MySQL est survenue : {{e}}')\n"
    python_code += f"{tab*3}finally:\n{tab*4}cursor.close()\n\n"
    return python_code + "\n"


def GenerateUpdateFunctions(root: ET.Element, table: str) -> str:
    first_table = table
    python_code = ""
    tab = "    "
    rows = root.findall(".//rows/row")
    tbu = []
    for row in rows:
        tbu.append([row.get('name'), row.get('type')])
    for el in tbu:
        if el[0] != root.find('.//primary-key').get('name'):
            python_code += f"{tab}def update_{first_table}_{el[0]}(self, {unformat_und(CheckValue(root)[0])}: {CheckValue(root)[1]}, {el[0]}: {el[1]}) -> None:\n"
            python_code += f'{tab*2}query = "UPDATE {first_table} SET {first_table}_{el[0]} = %s WHERE {first_table}_{format_und(CheckValue(root)[0])} = %s;"\n'
            python_code += f'{tab*2}params = ({unformat_und(CheckValue(root)[0])}, {el[0]})\n'
            python_code += f"{tab*2}if not self.{InternChecker(root)}:\n"
            python_code += f"{tab*3}cursor = self.connexion.cursor()\n{tab * 3}try:\n"
            python_code += f"{tab*4}cursor.execute(query, params)\n"
            python_code += f"{tab*4}self.connexion.commit()\n"
            python_code += f"{tab*4}self._logger.info(f'Modification de {el[0]} de {first_table} effectué par {{{el[0]}}}')\n"
            python_code += f"{tab*3}except Exception as e:\n"
            python_code += f"{tab*4}self._logger.error(f'Une erreur MySQL est survenue : {{e}}')\n"
            python_code += f"{tab*3}finally:\n{tab*4}cursor.close()\n\n"
    return python_code + "\n"


def GenerateDeleteFunction(root: ET.Element, table: str) -> str:
    first_table = table
    python_code = ""
    tab = "    "

    python_code += f"{tab}def delete_{first_table}_{format_und(CheckValue(root)[0])}(self, {unformat_und(CheckValue(root)[0])}: {CheckValue(root)[1]}) -> None:\n"
    python_code += f'{tab*2}query = "DELETE FROM {first_table} WHERE {first_table}_{format_und(CheckValue(root)[0])} = %s;"\n'
    python_code += f"{tab*2}params = ({unformat_und(CheckValue(root)[0])},)\n"
    python_code += f"{tab*2}if not self.{InternChecker(root)}:\n"
    python_code += f"{tab*3}cursor = self.connexion.cursor()\n{tab*3}try:\n"
    python_code += f"{tab*4}cursor.execute(query, params)\n"
    python_code += f"{tab*4}self.connexion.commit()\n"
    python_code += f"{tab*4}self._logger.info(f'Suppression de {format_und(CheckValue(root)[0])} de {first_table} effectué')\n"
    python_code += f"{tab*3}except Exception as e:\n"
    python_code += f"{tab*4}self._logger.error(f'Une erreur MySQL est survenue : {{e}}')\n"
    python_code += f"{tab*3}finally:\n{tab*4}cursor.close()\n\n"
    return python_code + "\n"

def Generate2Functions(root: ET.Element, table: str) -> str:
    first_table = table
    python_code = ""
    tab = "    "
    unic_indexes = []
    primary_key = root.find('.//primary-key')
    if primary_key is not None:
        unic_indexes.append({'name': f"{primary_key.get('name')}_", 'type': primary_key.get('type')})

    unique_index = root.findall('.//unic-index/name')
    for idx in unique_index:
        unic_indexes.append({'name': idx.text, 'type': idx.get('type')})

    for el in unic_indexes:
        for jel in unic_indexes:
            if el['name'] != jel['name']:
                python_code += f"{tab}def {format_und(el['name'])}2{format_und(jel['name'])}(self, {unformat_und(el['name'])}: {el['type']}) -> {jel['type']}:\n"
                python_code += f"""{tab*2}query = 'SELECT {first_table}_{format_und(jel['name'])} FROM {first_table} WHERE {first_table}_{format_und(el['name'])} = %s;'\n"""
                python_code += f"{tab*2}params = ({unformat_und(el['name'])},)\n"
                python_code += f"{tab*2}return self.get_results(query, params)\n\n"

        return python_code + "\n"

def GenerateGetFunctions(root: ET.Element, table: str) -> str:
    first_table = table
    table = table[0].upper() + table[1:].lower()
    python_code = ""
    tab = "    "
    unic_indexes = []
    primary_key = root.find('.//primary-key')
    if primary_key is not None:
        unic_indexes.append({'name': f"{primary_key.get('name')}_", 'type': primary_key.get('type')})

    unique_index = root.findall('.//unic-index/name')
    for idx in unique_index:
        unic_indexes.append({'name': idx.text, 'type': idx.get('type')})

    for el in unic_indexes:
        python_code += f"{tab}def get_{first_table}_{format_und(el['name'])}(self, {unformat_und(el['name'])}: {el['type']}) -> {table}:\n"
        python_code += f"{tab*2}query = 'SELECT * FROM {first_table} WHERE {first_table}_{format_und(el['name'])} = %s;'\n"
        python_code += f"{tab*2}params = ({unformat_und(el['name'])},)\n"
        python_code += f"{tab*2}return {table}(*self.get_results(query, params, ind_='all'))\n\n"

    return python_code + "\n"

def GenerateFromFunctions(root: ET.Element, table: str) -> str:
    first_table = table
    table = table[0].upper() + table[1:].lower()
    tab = "    "
    python_code = ""
    infos = []
    rows = root.findall(".//rows/row")
    for row in rows:
        if row.get('type') in ['float', 'int', 'datetime']:
            infos.append([row.get('name'), row.get('type')])

    modes = [{'name': 'from', 'operation': 'BETWEEN', 'args': ['from_', 'to_']},
             {'name': 'ge', 'operation': '>=', 'args': ['to_']},
             {'name': 'eq', 'operation': '==', 'args': ['to_']},
             {'name': 'ne', 'operation': '<>', 'args': ['to_']},
             {'name': 'gt', "operation": '>', 'args': ['to_']},
             {'name': 'le', 'operation': '=<', 'args': ['to_']},
             {'name': 'lt', 'operation': '<', 'args': ['to_']},
             {'name': 'in', 'operation': 'IN', 'args': ['list_']}]

    for mode in modes:
        name = mode['name']
        for info in infos:
            args = ', '.join([f'{m}: {info[1]}' for m in mode['args']])
            params = f'({mode["args"][0]},)'
            qu = f'{mode["operation"]} %s;'
            if mode['operation'] == 'IN':
                args = f'{mode["args"][0]}: list | tuple'
                qu = f'IN ({{",".join(["%s"] * len({mode["args"][0]}))}});'
                params = f"tuple({mode['args'][0]})"
            if mode['operation'] == 'BETWEEN':
                args = f'{mode["args"][0]}: list | tuple, {mode["args"][1]}: list | tuple'
                qu = f"BETWEEN % AND %;"
                params = f"({', '.join([f'{m}' for m in mode['args']])},)"

            python_code += f"{tab}def get_{first_table}_{name}_{format_und(info[0])}(self, {args}) -> list[{table}]:\n"
            python_code += f"{tab * 2}query = f'SELECT * FROM {first_table} WHERE {first_table}_{format_und(info[0])} {qu}'\n"
            python_code += f"{tab * 2}params = {params}\n"
            python_code += f"{tab*2}return [{table}(*row) for row in self.get_results(query, params, ind_='all')]\n\n"
    return python_code + "\n"


def GenerateStrFunctions(root: ET.Element, table: str) -> str:
    first_table = table
    table = table[0].upper() + table[1:].lower()
    tab = "    "
    python_code = ""
    infos = []
    rows = root.findall(".//rows/row")
    for row in rows:
        if row.get('type') == 'str':
            infos.append(row.get('name'))

    operations = [{'op': 'LIKE', 'args': ['deb'], 'type': ['str'], 'name': 'like_start'},
                  {'op': 'LIKE', 'args': ['deb', 'fin'], 'type': ['str', 'str'], 'name': 'like_between'},
                  {'op': 'LIKE', 'args': ['fin'], 'type': ['str'], 'name': 'like_end'},
                  {'op': 'LIKE', 'args': ['mil'], 'type': ['str'], 'name': 'like_mid'},
                  {'op': 'REGEXP', 'args': ['text'], 'type': ['str'], 'name': 'regexp'}]
    for el in [('<', 'lt'), ('>', 'gt'), ('<=', 'le'), ('>=', 'ge'), ('=', 'eq'), ('<>', 'ne')]:
        operations.append({'op': 'INSTR', 'args': ['text', 'occ'], 'type': ['str', 'int'], 'name': f'instr_{el[1]}', 'sym': el[0]})

    for info in infos:
        for op in operations:
            all_params = f"""{', '.join([f'{op["args"][i]}: {op["type"][i]}' for i in range(len(op['args']))])}"""
            python_code += f"{tab}def get_{first_table}_{op['name']}_{info}(self, {all_params}) -> list[{table}]:\n"
            qu = ''
            if op['op'] == "LIKE":
                if len(op['args']) == 1:
                    if op['args'][0] == 'deb':
                        qu = '{deb}%'
                    if op['args'][0] == 'mil':
                        qu = '%{mil}%'
                    if op['args'][0] == 'fin':
                        qu = '%{fin}'
                else:
                    qu = f"{{{op['args'][0]}}}%{{{op['args'][1]}}}"
                python_code += f"""{tab * 2}query = f"SELECT * FROM {first_table} WHERE {first_table}_{info} {op['op']} '{qu}';"\n"""
            if op['op'] == "REGEXP":
                python_code += f"""{tab * 2}query = f"SELECT * FROM {first_table} WHERE {first_table}_{info} {op['op']} '{{{op['args'][0]}}}';"\n"""
            if op['op'] == "INSTR":
                python_code += f"""{tab * 2}query = f"SELECT * FROM {first_table} WHERE {op['op']}({first_table}_{info}, '{{{op['args'][0]}}}') {op['sym']} {{{op['args'][1]}}};"\n"""
            python_code += f"{tab * 2}return [{table}(*row) for row in self.get_results(query, params=(), ind_='all')]\n\n"

    return python_code + "\n"
