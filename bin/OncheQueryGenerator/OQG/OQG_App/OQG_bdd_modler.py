import xml.etree.ElementTree as ET

from xml_bdd import xml_database
from config.variables import *

xml_database(MYSQL_DATABASE)
xml_bdd = f"{GLOBAL_PATH}bin/OQG_Types/Forum/bdd_metadata.xml"
xml_types = f"{GLOBAL_PATH}config/types.xml"

# type dans la bdd
with open(xml_bdd, 'r', encoding='utf-8') as xml_bdd_f:
    xml_content_bdd = xml_bdd_f.read()
root_bdd = ET.fromstring(xml_content_bdd)
distinct_types_bdd = set()
for table in root_bdd.findall(".//table"):
    for champ in table.findall(".//champ"):
        champ_type = champ.get("type")
        if champ_type:
            distinct_types_bdd.add(champ_type)

# types dans la config
with open(xml_types, 'r', encoding='utf-8') as xml_bdd_types:
    xml_content_bdd = xml_bdd_types.read()
root_types = ET.fromstring(xml_content_bdd)
name_type_mapping = set()
for types in root_types.findall('.//types'):
    for type_element in types.findall('type'):
        name = type_element.get('name')
        data_type = type_element.get('type')
        name_type_mapping.add((name, data_type))

# conversion de tout les types en type python
used_type = {}
for el in distinct_types_bdd:
    for typ in name_type_mapping:
        el_tempo = el
        if len(str(el).split("("))>0 and el != "tinyint(1)":
            el_tempo = str(el).split("(")[0]
        if el_tempo == typ[0]:
            used_type.update({el: typ[1]})

# conversion des type dans les métadonnées
with open(xml_bdd, "r", encoding="utf-8") as new_type:
    text = new_type.read()
    for key, item in used_type.items():
        print(f'type="{key}"', f'type="{item}"')
        text = text.replace(f'type="{key}"', f'type="{item}"')

with open(xml_bdd, "w", encoding="utf-8") as new_type_meta:
    new_type_meta.write(text)