import os

from config.Variables.variables import *

def get_database_version():
    # TODO modifier l'obtention de la date, via la génération du XML lors de son export
    """Renvoie les variables d'état du sytème"""
    date = DDB.split("_")[-1].split(".")[0][:8]
    #str_date = date[5:7]+"/"+date[4:6]+"/"+date[:4]
    #bdd = DDB.split("_")[1]
    return {"version": VERSION, "Créateur": CREATEUR, "BDD": DDB,"DATE": "tempo"}


def get_file_inside_folder(folder: str, type_: str = None, excepte: str = None) -> list:
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