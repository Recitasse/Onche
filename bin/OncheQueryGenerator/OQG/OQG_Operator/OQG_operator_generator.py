from pathlib import Path

import xml.etree.ElementTree as ET

from config.variables import *
from bin.OncheQueryGenerator.OQG.OQG_Operator.xml_type_reader import get_config, get_default, get_type_from_dict


class PythonOperatorGenerator:
    def __init__(self, prefix: str, path: str = "bin/OQG_Types/operator/operator.xml") -> None:
        self.prefix = prefix
        self.pwd = f"{GLOBAL_PATH}bin/OQG_Operator/"
        self.path_file = f'{GLOBAL_PATH}{path}'

        self.__create_root()
        self.__redo_install(self.prefix)

    def __create_root(self) -> None:
        """Créer l'élément root pour le parse du xml"""
        if Path(self.path_file).exists():
            self.tree = ET.parse(self.path_file)
            self.root = self.tree.getroot()
            return
        raise FileNotFoundError(f"Le fichier {self.path_file} n'existe pas.")

    def __redo_install(self, prefix: str) -> None:
        files_ = os.listdir(self.pwd)
        for file_ in files_:
            if len(file_.split(prefix))>1 and len(file_.split("operator"))!=2:
                print(f"Fichier {os.path.join(self.pwd, file_)} supprimé")
                os.remove(os.path.join(self.pwd, file_))

    def generate_operator(self) -> None:
        """Génère le script python des opérateurs"""

        result = []
        for operationlist in self.root.findall('.//operationlist'):
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
                            'container': parameter.get('container'),
                            'inline': parameter.get('inline'),
                            'sour': parameter.get('sour')
                        }
                        parameter_list.append(parameter_info)

                    parameters.update({i: parameter_list[i] for i in range(len(parameter_list))})

                    operator_info['parameters'] = parameters
                    operationlist_info['operator'] = operator_info

                result.append(operationlist_info)

        file_viewed = []
        for i, func in enumerate(result):
            file_name = func['name']
            func_name = func['operator']['function']
            with open(f"{self.pwd}/OQGop_{file_name}.py", "a", encoding="utf-8") as op:
                operator = func['operator']
                name_func = operator['name']
                description = operator['description']
                output_type = operator['type']
                param = []
                original_param = []
                input_ = [","]
                params_query = []
                if len(operator['parameters'].values()) > 1:
                    for parameter in operator['parameters'].values():
                        sour = ""
                        if parameter['sour']:
                            sour = parameter['sour']
            
                        cont = ""
                        if parameter['container']:
                            cont = f"{parameter['container']} "

                        if parameter['linked'] == "1":
                            input_.append(f" {cont}{sour}'+"+ str(parameter['value']) + f"+'{sour}")
                        else:
                            link=", "
                            input_.append(f"{link}{cont}%s")
                            params_query.append(f"{sour}{parameter['value']}{sour}")

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
                    if parameter['inline'] == "1":
                        query = f"query='SELECT {''.join(input_).replace(',, ','')};'\n"
                else:
                    query = f"query='SELECT {func_name}();'\n"
                    param_str =""

                original_param = (parameter['value'], parameter['type'])
                if func['name'] not in file_viewed:
                    op.write("import datetime\n\n")
                    op.write("from config.Variables.variables import *\n")
                    op.write("from BDD.bdd import BDD\n\n")
                op.write(f"def {name_func}({', '.join(param)}) -> {output_type}:\n")
                op.write(f'\t"""{description}"""\n')
                if original_param:
                    op.write(f"{self.type_limiter(original_param)}")
                op.write(f'\ttry:\n')
                op.write(f'\t\tbdd_tmp = BDD()\n')
                op.write(f"\t\t{query}")
                op.write(f"\t\treturn bdd_tmp.get_results(query{param_str})\n")
                op.write(f"\texcept Exception as e:\n")
                op.write(f"\t\tprint(e)\n")
                op.write(f"\treturn None\n\n")
            file_viewed.append(func['name'])
                
    def type_limiter(self, original_parameter: tuple) -> str:
        """Ecrit les conditions et limitations d'un type donné"""
        type_name = original_parameter[1]
        variable_name = original_parameter[0]
        vals = get_config(type_name)
        text_ =""
        if vals:
            if vals['type'] == "tuple":
                val_p = tuple(t['value'] for t in vals['field'])
                text_ += f"\tif {variable_name} not in {val_p}:\n"
                text_ += f"""\t\tprint("Erreur, {variable_name} doit être l'une de ces valeurs : {val_p}.")\n"""
        return text_

t = PythonOperatorGenerator("op")
t.generate_operator()

