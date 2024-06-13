import os

from utils.fonction import change_value_variables

from config.variables import *
from BDD.bdd import BDD


def change_database(database: str) -> bool:
    """Change la base de donnée"""
    _ret = False

    try:
        BDD().import_table(f"{GLOBAL_PATH}/BDD/import/server/bdd_{database}.sql")
        BDD().change_bdd(database)
        _ret = change_value_variables("MYSQL_DATABASE", database)
    except Exception as e:
        print(e)
        return _ret
    return _ret


def get_database_import():
    """Donne les databases dans le répertoire d'import"""
    doc_list = os.listdir(f"{GLOBAL_PATH}BDD/import/server/")
    if doc_list == []:
        doc_list = ["none"]
    return {key: item for key, item in enumerate(doc_list)}


def get_database_data():
    """Renvoie les infos générales de la base de donnée"""
    messages_froum = {i : BDD(database=MYSQL_DATABASE).get_results('SELECT COUNT(*) AS message_count FROM Onche.messages WHERE message_topic IN (SELECT id_topic FROM Onche.topic WHERE topic_forum = %s);', params=(i,)) for i in range(1,10)}
    topics_froum = {i : BDD(database=MYSQL_DATABASE).get_results('SELECT COUNT(*) FROM topic WHERE topic_forum = %s;', params=(i,)) for i in range(1,10)}
    onchois_forum = BDD(database=MYSQL_DATABASE).get_results("SELECT COUNT(*) FROM onchois;")
    return {"Messages": messages_froum,
            "Topics" : topics_froum,
            "Onchois": f"Nb onchois : {onchois_forum}"}