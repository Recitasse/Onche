from OQG_bdd_entities import *
from OQG_bdd_tools import *
from OQG_bdd_generator import *
from OQG_parser_generator import *


if __name__ == "__main__":
    # Generate MySQL schema
    files = get_all_xml_files()
    if 'schema.sql' in os.listdir(f'{GLOBAL_PATH}/bin/database'):
        os.remove(f'{GLOBAL_PATH}/bin/database/schema.sql')
    with open(f'{GLOBAL_PATH}/bin/database/schema.sql', 'a', encoding="utf-8") as f:
        f.write(metadata())
    with open(f'{GLOBAL_PATH}/bin/database/schema.sql', 'a', encoding="utf-8") as f:
        for file_ in files:
            f.write(generate_sql_code_from_xml(file_))
    with open(f'{GLOBAL_PATH}/bin/database/schema.sql', 'a', encoding="utf-8") as f:
        f.write(setting())
    print(f"MySQL schema generation complete")

    # Generate selectors
    for file in files:
        glb_str = ""
        with open(f"{CALICE}{file}", 'r', encoding="utf-8") as conf:
            root: ET.Element = ET.fromstring(conf.read())
        table_name = root.attrib['table']

        if os.path.exists(f"{GLOBAL_PATH}bin/database/selectors/selector_{table_name}.py"):
            os.remove(f"{GLOBAL_PATH}bin/database/selectors/selector_{table_name}.py")

        glb_str += GenerateImportQueries(table_name)
        glb_str += GenerateIsFunctions(root, table_name)
        glb_str += GenerateAddFunctions(root, table_name)
        glb_str += GenerateUpdateFunctions(root, table_name)
        glb_str += GenerateDeleteFunction(root, table_name)
        glb_str += Generate2Functions(root, table_name)
        glb_str += GenerateGetFunctions(root, table_name)
        glb_str += GenerateFromFunctions(root, table_name)
        glb_str += GenerateStrFunctions(root, table_name)

        with open(f"{GLOBAL_PATH}bin/database/tools/selectors/selector_{table_name}.py", 'w', encoding="utf-8") as f:
            f.write(glb_str)
    print(f"Selectors generation complete")

    # Generate Entities
    for file in files:
        glb_str = ""
        with open(f"{CALICE}{file}", 'r', encoding="utf-8") as conf:
            root: ET.Element = ET.fromstring(conf.read())
        table_name = root.attrib['table']
        name = table_name[0].upper() + table_name[1:].lower()
        if os.path.exists(f"{GLOBAL_PATH}bin/database/entities/{name}.py"):
            os.remove(f"{GLOBAL_PATH}bin/database/entities/{name}.py")

        glb_str += GenerateImportFunctions(table_name)
        glb_str += GenerateValuesFunctions(root, table_name)
        glb_str += GeneratePropertiesFunc(root, table_name)
        glb_str += GenerateSettersFunctions(root, table_name)

        with open(f"{GLOBAL_PATH}bin/database/tools/entities/{name}.py", 'w', encoding="utf-8") as f:
            f.write(glb_str)
    print(f"Entities generation complete")

    generate_badge_getter(files)
    print(f"Parser generation complete")

    print(f"Overall generation is finished")


