from os import path
from config.variables import CALICE, GLOBAL_PATH
import xml.etree.ElementTree as ET
from bin.OncheQueryGenerator.OQG.OQG_App.tools.file_getter import get_all_xml_files, uppercase_first, set_title


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
        if root.find('.//url'):
            all_[collector_name].update({"params": {}})
            base_url = root.find('.//url').get('base')
            for param in root.findall('.//param'):
                all_[collector_name]["params"].update({param.get("name"): {"mode": param.get("mode"), "type": param.get("type"), "_spec": param.get('_spec', default=None)}})
            all_[collector_name].update({"url": base_url})
        all_[collector_name].update({"elements": {}})
        for row in root.findall('.//row'):
            name = row.get('name')
            parser = row.find("parser")
            if parser.get("where") == collector_name or parser.get("name-equal") == "True":
                type_ = row.find("parser").get("sql-type")
                name_ = parser.get("name")
                bs4_mode = parser.find("css-selector").get("bs4", default=None)
                selector = parser.find("css-selector").get("selector", default=None)
                css_path = (parser.find("css-selector").text, selector, bs4_mode)

                trigger = parser.find("css-selector").get("trigger") if parser.find("css-selector").get("trigger") is not None else ""
                cleans = [(el.text if el.text is not None else "", el.get("re", default=""), el.get("equal", default=""), el.get("cut", default="")) for el in parser.findall("clean")]
                all_[collector_name]["elements"].update({name: {"type": type_, "name": name_, "path": css_path, "trigger": trigger, "cleans": cleans}})

    return all_


def generate_parser(name_file: str, JSON: dict):
    # Generate the import
    tab = "    "
    glb = "from datetime import datetime\n"
    glb += "import re\n"
    glb += "from dataclasses import dataclass\n"
    glb += "from bs4 import BeautifulSoup\n"
    glb += "from bin.WebScrapper.OncheScrapper.req import Requests\n\n\n"

    # Create class
    glb += "@dataclass(init=False)\n"
    glb += f"class {uppercase_first(name_file)}:\n"

    # create collector
    if JSON[name_file]["params"] is not None:
        # génération de l'url
        tmp_ = []; tmpq_ = []; tmpp_ = []; tmp2_ = []
        for name, el in JSON[name_file]["params"].items():
            tmp_.append(f"{name}: {el['type']}")
            tmp2_.append(name)
            if el['mode'] == 'path':
                if el['_spec'] is not None:
                    tmpp_.append(f"{{{set_title(name)}}}")
                else:
                    tmpp_.append(f"{{{name}}}")
            elif el['mode'] == "query":
                tmpq_.append(f"{name}={{{name}}}")
        query_p = f'{"?" if tmpq_.__len__() > 0 else ""}'+'&'.join(tmpq_)
        path_p = '/'.join(tmpp_)
        glb_query = path_p + query_p
        glb += f"{tab}@staticmethod\n"
        glb += f"{tab}def _{name_file}_collector({', '.join(tmp_)}) -> BeautifulSoup:\n"
        glb += f"{2*tab}link = f'{JSON[name_file]['url']}{glb_query}'\n"
        glb += f"{2*tab}return Requests().req_html(link, bs4_mode=True)\n\n"

        # fonction pour le clean
        glb += f"{tab}@staticmethod\n"
        glb += f"{tab}def collector({', '.join(tmp_)}) -> dict:\n"
        glb += f"{2*tab}soup = {uppercase_first(name_file)}._{name_file}_collector({', '.join(tmp2_)})\n"
        glb += f"{2*tab}info = {{}}\n"
        # Traitement des éléments
        for name, el in JSON[name_file]["elements"].items():
            selector = "text"
            if el['path'][1] is not None:
                selector = f"get('{el['path'][1]}')"
            path_ = el['path'][0]
            if el['trigger'] != "":
                glb += f"{2*tab}if soup.select('{path_}').__len__() > 1:\n"
                glb += f"{3*tab}tmp_ = []\n"
                glb += f"{3*tab}for el in soup.select('{path_}'):\n"
                glb += f"{4*tab}if el.{selector} == '{el['trigger']}':\n"
                glb += f"{5*tab}tmp_.append(1)\n"
                glb += f"{4*tab}else:\n"
                glb += f"{5*tab}tmp_.append(0)\n"
                glb += f"{3*tab}info.update({{'{name}': tmp_}})\n"

                glb += f"{2*tab}else:\n"
                glb += f"{3*tab}if soup.select('{path_}')[0].{selector} == '{el['trigger']}':\n"
                glb += f"{4*tab}info.update({{'{name}': 1}})\n"
                glb += f"{3*tab}else:\n"
                glb += f"{4*tab}info.update({{'{name}': 0}})\n"
            else:
                glb += f"{2*tab}if soup.select('{path_}').__len__() > 1:\n"
                glb += f"{3*tab}tmp_ = []\n"
                glb += f"{3*tab}for el in soup.select('{path_}'):\n"

                glb += f"{4*tab}tmp_.append(el.{selector} if {el['path'][2] == None} else el)\n"

                glb += f"{3*tab}info.update({{'{name}': tmp_}})\n"
                glb += f"{2*tab}else:\n"
                glb += f"{3*tab}info.update({{'{name}': soup.select('{path_}')[0].{selector}}})\n"
            if el['cleans'] != [('', '', '', '')]:
                glb += f"{2*tab}cleans = {el['cleans']}\n"
                glb += f"{2*tab}for clean in cleans:\n"

                glb += f"{3*tab}if info['{name}'].__len__() > 1 and not isinstance(info['{name}'], str):\n"
                glb += f"{4*tab}for i in range(info['{name}'].__len__()):\n"
                glb += f"{5*tab}info['{name}'][i] = info['{name}'][i].replace(clean[0], '')\n"
                glb += f"{5*tab}if clean[1] != '':\n"
                glb += f"{6*tab}match = re.search(clean[1], info['{name}'][i])\n"
                glb += f"{6*tab}if match:\n"
                glb += f"{7*tab}rep = ' ' + match[0]\n"
                glb += f"{7*tab}info['{name}'][i] = info['{name}'][i].replace(rep, '') if clean[2] == 'False' else rep\n"
                glb += f"{5*tab}if clean[3] != '':\n"
                glb += f"{6*tab}info['{name}'][i] = info['{name}'][i].split(clean[3])[0]\n"

                glb += f"{3*tab}else:\n"
                glb += f"{4*tab}info['{name}'] = info['{name}'].replace(clean[0], '')\n"
                glb += f"{4*tab}if clean[1] != '':\n"
                glb += f"{5*tab}match = re.search(clean[1], info['{name}'])\n"
                glb += f"{5*tab}if match:\n"
                glb += f"{6*tab}rep = ' ' + match[0]\n"
                glb += f"{6*tab}info['{name}'] = info['{name}'].replace(rep, '') if clean[2] == 'False' else rep\n"
                glb += f"{4*tab}if clean[3] != '':\n"
                glb += f"{5*tab}info['{name}'] = info['{name}'].split(clean[3])[0]\n"


            if el["type"] == "datetime":
                glb += f"{2*tab}if not isinstance(info['{name}'], list):\n"
                glb += f"{3*tab}info['{name}'] = info['{name}'][:-1] if info['{name}'][-1] == ' ' else info['{name}']\n"
                glb += f"{3*tab}info['{name}'] = datetime.strptime(info['{name}'], '%d/%m/%Y %H:%M:%S')\n"
                glb += f"{2*tab}else:\n"
                glb += f"{3*tab}for i in range(info['{name}'].__len__()):\n"
                glb += f"{4*tab}info['{name}'][i] = info['{name}'][i][:-1] if info['{name}'][i][-1] == ' ' else info['{name}'][i]\n"
                glb += f"{3*tab}info['{name}'] = [datetime.strptime(el_, '%d/%m/%Y %H:%M:%S') for el_ in info['{name}']]\n"
            elif el['type'] == "int":
                glb += f"{2*tab}if not isinstance(info['{name}'], list):\n"
                glb += f"{3*tab}info['{name}'] = int(info['{name}'])\n"
                glb += f"{2*tab}else:\n"
                glb += f"{3*tab}info['{name}'] = [int(el_) if isinstance(el_, str) else int(el_) for el_ in info['{name}']]\n"
            elif el['type'] == "float":
                glb += f"{2*tab}if isinstance(info['{name}'], str):\n"
                glb += f"{3*tab}info['{name}'] = float(info['{name}'])\n"
                glb += f"{2*tab}else:\n"
                glb += f"{3*tab}info['{name}'] = [float(el_.strip()) if isinstance(el_, str) else float(el_) for el_ in info['{name}']]\n"
        glb += "\n"
        for el in tmp2_:
            glb += f"{2*tab}info['{el}'] = {el}\n"
        glb += f"\n{2*tab}return info\n"

    return glb

def write_file() -> None:
    JSON = generate_JSON_infos()
    for name in JSON.keys():
        with open(path.join(GLOBAL_PATH, f"bin/OncheQueryGenerator/OQG/OQG_Collector/{name}.py"), "w", encoding="utf-8") as rew:
            rew.write(generate_parser(name, JSON))

write_file()
