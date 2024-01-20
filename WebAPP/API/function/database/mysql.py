import os
from getpass import getpass

from subprocess import run, PIPE

from config.Variables.variables import *
from BDD.bdd import BDD

def get_mysql_status() -> list:
    """Renvoie l'état sous forme de texte de la connexion mysql"""
    try:
        result = run(["systemctl", "status", "mysql"], stdout=PIPE, stderr=PIPE, text=True)
        output = result.stdout
    except Exception as e:
        output = f"Erreur : {e}"
    return output.split("\n")

def get_mysql_connexion() -> bool:
    """Renvoie le booléen de la connexion à la base de donnée"""
    result = get_mysql_status()
    if ''.join(result).find("inactive") > 0:
        return False
    return True

def get_mysql_database_info() -> dict:
    """Renvoie les paramètres de la base de donnée actuellement, user, host, database name, size"""
    try:
        size = BDD(database=MYSQL_DATABASE).size()
    except Exception as e:
        size = "Aucune connexion"

    date = DDB.split("_")[-1].split(".")[0][:8]
    str_date = date[5:7]+"/"+date[4:6]+"/"+date[:4]
    return {"user": f"User : {MYSQL_USER}", "host": f"Host : {MYSQL_HOST}" if len(MYSQL_HOST)>0 else "Host : 127.0.0.1", "database": f"Database : {MYSQL_DATABASE}", "size": f"Size : {size} Mo", "date": f"Date : {str_date}"}


def get_mysql_available_database() -> dict:
    """Donne les databases dans le répertoire d'import"""
    doc_list = os.listdir(f"{GLOBAL_PATH}BDD/import/local/")
    if doc_list == []:
        doc_list = ["none"]
    return {key: item for key, item in enumerate(doc_list)}


def start_mysql(password: str) -> bool:
    """Démarre la connexion mysql"""
    start_mysql_command = f"""echo "{password}" | sudo -S -p "" systemctl start mysql"""
    try:
        run(start_mysql_command, shell=True, check=True)
    except Exception as e:
        return False
    return get_mysql_connexion()

def stop_mysql(password: str) -> bool:
    """Déconnexion mysql"""
    start_mysql_command = f"""echo "{password}" | sudo -S -p "" systemctl stop mysql"""
    try:
        run(start_mysql_command, shell=True, check=True)
    except Exception as e:
        return False
    return not get_mysql_connexion()
