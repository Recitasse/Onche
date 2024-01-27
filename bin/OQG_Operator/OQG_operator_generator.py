import xml.etree.ElementTree as ET

from config.Variables.variables import *
from bin.OQG_Operator.xml_type_reader import get_config, get_default, get_type_from_dict

def reset_operation(file_name):
    with open(f"{pwd}/OQG_{file_name}.py", "w", encoding="utf-8") as op:
        op.write("")

pwd = f"{GLOBAL_PATH}bin/OQG_Operator/"
tree = ET.parse(f'{GLOBAL_PATH}bin/OQG_Types/operator/operator.xml')
root = tree.getroot()

result = []
for operationlist in root.findall('.//operationlist'):
    for operator in operationlist.findall('.//operator'):
        operationlist_info = {
            'name': operationlist.get('name')
        }

        operator_info = {
            'name': operator.get('name'),
            'description': operator.get('description'),
            'type': operator.get('type'),
            'function' : operator.find('.//function').text
        }

        parameters = {}
        for operation in operator.findall('.//operation'):

            parameter_list = []
            
            for parameter in operation.findall('.//parameter'):
                parameter_info = {
                    'type': parameter.get('type'),
                    'opt': parameter.get('opt'),
                    'value': parameter.text,
                    'linked': parameter.get('linked'),
                    'container': parameter.get('container')
                }
                parameter_list.append(parameter_info)

            parameters.update({i: parameter_list[i] for i in range(len(parameter_list))})

            operator_info['parameters'] = parameters
            operationlist_info['operator'] = operator_info

        result.append(operationlist_info)




for i, func in enumerate(result):
    print(func)
    file_name = func['name']
    func_name = func['operator']['function']
    with open(f"{pwd}/OQG_{file_name}.py", "a", encoding="utf-8") as op:
        operator = func['operator']
        name_func = operator['name']
        description = operator['description']
        output_type = operator['type']
        param = []
        input_ = [","]
        params_query = []
        if len(operator['parameters'].values()) > 1:
            for parameter in operator['parameters'].values():
                if parameter['container']:
                    cont = f"{parameter['container']} "
                else:
                    cont = ""
                if parameter['linked'] == "1":
                    input_.append(f" {cont}'+"+ str(parameter['value']) + "+'")
                else:
                    link=", "
                    input_.append(f"{link}{cont}%s")
                    params_query.append(parameter['value'])

                if parameter['opt'] == "1":
                    conf = get_config(parameter['type'])
                    dflt = get_default(parameter['type'])
                    if get_type_from_dict(conf, dflt):
                        if get_type_from_dict(conf, dflt) == "str":
                            param.append(f"{parameter['value']}: {get_type_from_dict(conf, dflt)} = '{dflt}'")
                        else:
                            param.append(f"{parameter['value']}: {get_type_from_dict(conf, dflt)} = {eval(dflt)}")
                    else:
                        param.append(f"{parameter['value']}: {conf} = {dflt}")
                else:
                    if get_config(parameter['type']):
                        param.append(f"{parameter['value']}: {get_config(parameter['type'])}")
                    else:
                        param.append(f"{parameter['value']}: {parameter['type']}")
            query = f"query='SELECT {func_name}({''.join(input_).replace(',, ','')});'\n"
            param_str = f", params=({', '.join(params_query)},)"
        else:
            query = f"query='SELECT {func_name}();'\n"
            param_str =""
        if i==0:
            op.write("import datetime\n\n")
            op.write("from config.Variables.variables import *\n")
            op.write("from BDD.bdd import BDD\n\n")
        op.write(f"def {name_func}({', '.join(param)}) -> {output_type}:\n")
        op.write(f'    """"{description}"""\n')
        op.write(f'    try:\n')
        op.write(f'        bdd_tmp = BDD()\n')
        op.write(f"        {query}")
        op.write(f"        return bdd_tmp.get_results(query{param_str})\n")
        op.write(f"    except Exception as e:\n")
        op.write(f"        print(e)\n")
        op.write(f"    return None\n\n")
                




