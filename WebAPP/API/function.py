import os
import sys
import subprocess

from flask import Flask, jsonify, Blueprint
from random import randint

parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(parent_dir)

from config.Variables.variables import *
from utils.fonction import change_value_variables
from BDD.bdd import BDD

SUCESS = True
ERROR = False

def get_mysql_base():
    """Renvoie l'état de la connexion mysql"""
    try:
        result = subprocess.run(["systemctl", "status", "mysql"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output = result.stdout
    except Exception as e:
        output = f"Erreur : {e}"
    return output.split("\n")

def get_mysql_parameter():
    """Renvoie les paramètres de la base de donnée actuellement"""
    try:
        size = BDD(database=MYSQL_DATABASE).size()
    except Exception as e:
        size = "Aucune connexion"

    date = DDB.split("_")[-1].split(".")[0][:8]
    str_date = date[5:7]+"/"+date[4:6]+"/"+date[:4]
    return {"user": f"User : {MYSQL_USER}", "host": f"Host : {MYSQL_HOST}" if len(MYSQL_HOST)>0 else "Host : 127.0.0.1", "database": f"Database : {MYSQL_DATABASE}", "size": f"Size : {size} Mo", "date": f"Date : {str_date}"}

def get_database_data():
    """Renvoie les infos générales de la base de donnée"""
    messages_froum = {i : BDD(database=MYSQL_DATABASE).get_results('SELECT COUNT(*) AS message_count FROM Onche.messages WHERE message_topic IN (SELECT id_topic FROM Onche.topic WHERE topic_forum = %s);', params=(i,)) for i in range(1,10)}
    topics_froum = {i : BDD(database=MYSQL_DATABASE).get_results('SELECT COUNT(*) FROM topic WHERE topic_forum = %s;', params=(i,)) for i in range(1,10)}
    onchois_forum = BDD(database=MYSQL_DATABASE).get_results("SELECT COUNT(*) FROM onchois;")
    return {"Messages": messages_froum,
            "Topics" : topics_froum,
            "Onchois": f"Nb onchois : {onchois_forum}"}

def get_version_variables():
    """Renvoie les variables d'état du sytème"""
    date = DDB.split("_")[-1].split(".")[0][:8]
    str_date = date[5:7]+"/"+date[4:6]+"/"+date[:4]
    bdd = DDB.split("_")[1]
    return {"version": VERSION, "Créateur": CREATEUR, "BDD": bdd,"DATE": str_date}

def get_database_import():
    """Donne les databases dans le répertoire d'import"""
    doc_list = os.listdir(f"{GLOBAL_PATH}BDD/import/")
    if doc_list == []:
        doc_list = ["none"]
    return {key: item for key, item in enumerate(doc_list)}

def get_file_inside(folder: str, type_: str = None, excepte: str = None):
    """Renvoie le contenue d'un répertoire"""
    doc = []
    files = os.listdir(f"{GLOBAL_PATH}{folder}")
    if type_:
        for file in files:
            if file.endswith("."+type_) and file.split(".")[0].split("_")[-1] != excepte:
                doc.append(file)
    else:
        doc_t = []
        for file in files:
            if file.split(".")[0].split("_")[-1] != excepte:
                doc_t.append(file)
        return doc_t
    return doc

print(get_file_inside("BDD/import/", "sql", MYSQL_DATABASE))

# =========================================

def change_database(database: str) -> bool:
    """Change la base de donnée"""
    _ret = ERROR
    try:
        BDD(database=MYSQL_DATABASE).change_bdd(database)
        _ret = change_value_variables("MYSQL_DATABASE", database)
    except Exception as e:
        return _ret
    return _ret