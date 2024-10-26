import os
import datetime
from OQG_bdd_entities import *
from OQG_bdd_tools import *
from OQG_bdd_generator import *
from OQG_integrator_generator import *
from OQG.OQG_App.OQG_collector_generator import write_file as write_collector
from OQG.OQG_App.OQG_integrator_generator import write_file as write_integrator


if __name__ == "__main__":
    # Generate MySQL schema
    date = datetime.datetime.now().strftime("%d%m%Y")
    files = get_all_xml_files()
    n_path = os.path.join(GLOBAL_PATH, r"data/Database/src", f"Onche{date}")
    os.makedirs(n_path, exist_ok=True)
    os.chmod(n_path, 0o777)
    with open(os.path.join(n_path, f'schema{date}.sql'), 'w', encoding="utf-8") as f:
        f.write(metadata())
    with open(os.path.join(n_path, f'schema{date}.sql'), 'w', encoding="utf-8") as f:
        for file_ in files:
            f.write(generate_sql_code_from_xml(file_))
    with open(os.path.join(n_path, f'schema{date}.sql'), 'w', encoding="utf-8") as f:
        f.write(setting())
    print(f"MySQL schema generation complete")

    # Write metadata file


    # Generate selectors
    for file in files:
        glb_str = ""
        with open(f"{CALICE}{file}", 'r', encoding="utf-8") as conf:
            root: ET.Element = ET.fromstring(conf.read())
        table_name = root.attrib['table']

        if os.path.exists(os.path.join(GLOBAL_PATH, f'bin/database/OncheDatabase/selectors/selector_{table_name}.py')):
            os.remove(os.path.join(GLOBAL_PATH, f'bin/database/OncheDatabase/selectors/selector_{table_name}.py'))

        glb_str += GenerateImportQueries(table_name)
        glb_str += GenerateIsFunctions(root, table_name)
        glb_str += GenerateAddFunctions(root, table_name)
        glb_str += GenerateUpdateFunctions(root, table_name)
        glb_str += GenerateDeleteFunction(root, table_name)
        glb_str += Generate2Functions(root, table_name)
        glb_str += GenerateGetFunctions(root, table_name)
        glb_str += GenerateFromFunctions(root, table_name)
        glb_str += GenerateStrFunctions(root, table_name)

        with open(os.path.join(GLOBAL_PATH, f'bin/database/OncheDatabase/selectors/selector_{table_name}.py'), 'w', encoding="utf-8") as f:
            f.write(glb_str)
    print(f"Selectors generation complete")

    # Generate Entities
    for file in files:
        glb_str = ""
        with open(f"{CALICE}{file}", 'r', encoding="utf-8") as conf:
            root: ET.Element = ET.fromstring(conf.read())
        table_name = root.attrib['table']
        name = table_name[0].upper() + table_name[1:].lower()
        if os.path.exists(os.path.join(GLOBAL_PATH, f"bin/database/OncheDatabase/entities/{name}.py")):
            os.remove(os.path.join(GLOBAL_PATH, f"bin/database/OncheDatabase/entities/{name}.py"))

        glb_str += GenerateImportFunctions(table_name)
        glb_str += GenerateValuesFunctions(root, table_name)
        glb_str += GeneratePropertiesFunc(root, table_name)
        glb_str += GenerateSettersFunctions(root, table_name)

        with open(os.path.join(GLOBAL_PATH, f"bin/database/OncheDatabase/entities/{name}.py"), 'w', encoding="utf-8") as f:
            f.write(glb_str)
    print(f"Entities generation complete")

    write_collector()
    print(f"Parser generation complete")

    write_integrator()
    print(f"Integrator generation complete")
    print(f"Overall generation is finished")


