import xml.etree.ElementTree as ET

from config.Variables.variables import *

xml_types = f"{GLOBAL_PATH}config/types.xml"
pwd = f"{GLOBAL_PATH}bin/OQG_Types_refactor/"

with open(xml_types, 'r', encoding='utf-8') as xml:
    xml_content = xml.read()
root = ET.fromstring(xml_content)
date_types = root.findall(".//dates/types/type")
result = [{'name': t.get('name'), 'type': t.get('type')} for t in date_types]

with open(f"{pwd}serialize_date.py", 'w', encoding="utf-8") as d:
    d.write("import datetime\n\n")
    for res in result:
        d.write(f"def serialize_{res['name']}(date: {res['type']}) -> str:\n")
        d.write(f'    """Serialize {res["type"]} to str"""\n')
        if res['type'] == "datetime":
            d.write(f'    return date.strftime("%Y-%m-%d %H:%M:%S")\n\n\n')
