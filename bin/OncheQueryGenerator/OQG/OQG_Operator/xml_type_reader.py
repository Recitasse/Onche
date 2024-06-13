import xml.etree.ElementTree as ET

from config.variables import *

def get_config(name: str) -> dict:
    with open(f'{GLOBAL_PATH}bin/OQG_Types/Types/OQG_types.xml', 'r', encoding='utf-8') as xml_bdd_f:
        xml_content = xml_bdd_f.read()
    root = ET.fromstring(xml_content)
    result = {}
    record_element = root.find(f".//record[@name='{name}']")

    if record_element is not None:
        record_info = {
            'name': record_element.get('name'),
            'type': record_element.get('type')
        }
        if record_info['type'] == "tuple":
            cases = []
            for case in record_element.findall('.//field'):
                case_info = {
                    'value': case.get('value'),
                    'type': case.get('type'),
                    'default': case.get('default')
                }
                cases.append(case_info)

            record_info['field'] = cases
            result.update(record_info)

        else:
            case = record_element.find('.//field')
            result = {
                'value': case.get('value'),
                'type': case.get('type'),
                'default': case.get('default')
            }

    if result == {}:
        return None
    return result

def get_default(name: str):
    with open(f'{GLOBAL_PATH}bin/OQG_Types/Types/OQG_types.xml', 'r', encoding='utf-8') as xml_bdd_f:
        xml_content = xml_bdd_f.read()
    root = ET.fromstring(xml_content)
    record_element = root.find(f".//record[@name='{name}']")

    if record_element is not None:
        record_info = {
            'name': record_element.get('name'),
            'type': record_element.get('type')
        }
        if record_info['type'] == "tuple":
            for case in record_element.findall('.//field'):
                if case.get("default") == "1":
                    return case.get("value")
        else:
            case = record_element.find('.//field')
            if case.get("default") == "1":
                return case.get("value")


def get_type_from_dict(dic: dict, value: str):
    if dic['type'] == "tuple":
        day_dict = next((field for field in dic['field'] if field['value'] == value), None)
        if day_dict:
            return day_dict['type']
    else:
        return dic['type']
    return None