import subprocess
import time

from config.Variables.variables import *
from BDD.bdd import BDD

def cyclic_task_export(database: str = MYSQL_DATABASE):
    BDD(database=database).exporter_bdd()
    command = f"sh {GLOBAL_PATH}BDD/export/export_bdd.sh {database} {GLOBAL_PATH}"
    subprocess.run(command, shell=True)

# Export ddb
if __name__ == "__main__":
    while True:
        cyclic_task_export()
        time.sleep(CYCLIC_EXPORT)

