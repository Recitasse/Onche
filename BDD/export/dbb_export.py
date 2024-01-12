import subprocess
import time
import os
import sys

parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(parent_dir)

from config.Variables.variables import *
from BDD.bdd import BDD

# Export ddb
if __name__ == "__main__":
    print(MYSQL_DATABASE, GLOBAL_PATH)
    BDD(database=MYSQL_DATABASE).exporter_bdd()
    command = f"sh {GLOBAL_PATH}BDD/export/export_bdd.sh {MYSQL_DATABASE} {GLOBAL_PATH}"
    subprocess.run(command, shell=True)
