import logging

from typing import Optional
from subprocess import run, PIPE
from typing import Callable
from flask import Flask, jsonify, Blueprint

from config.Variables.variables import *
from utils.logger import logger

from WebAPP.API.function.database.mysql import *
from WebAPP.API.function.database.database import *
from WebAPP.API.function.utils.general import *

app = Flask(__name__)
babelonche_api = Blueprint('babelonche_api', __name__)
log_api = logger(PATH_API_LOG, "api", True)

# ================ Méthode API + LOGGER + page d'erreur ======================

def do_api_method(api_method, log: logging, error_id: int = 0, *args, **kwargs):
    """Applique les fonctions et renvoie leur valeur logguée et ou l'ID de l'erreur si la requête a échouée."""
    data = {}
    try:
        data = api_method(*args, **kwargs)
        log.info(f"Fonction debug")
    except Exception as e:
        log.error(f"Erreur id {error_id}: {e}")
        data = {"state": False, "id": error_id}
    return data

# ================ Obtenir l'état de mysql ================

@babelonche_api.route('/mysql/state', methods=['GET'])
def get_mysql():
    return do_api_method(api_method=get_mysql_status, log=log_api)


@babelonche_api.route('/mysql/info', methods=['GET'])
def get_mysql_info():
    """Renvoie les informations de la base de donnée"""
    return do_api_method(api_method=get_mysql_database_info, log=log_api)


@babelonche_api.route('/mysql/database', methods=['GET'])
def get_mysql_database():
    """Donne les databases dans le répertoire d'import"""
    return do_api_method(api_method=get_mysql_available_database, log=log_api)

@babelonche_api.route('/mysql/start/<string:password>', methods=['GET'])
def command_mysql_start(password: str):
    """Démarre mysql"""
    return do_api_method(start_mysql, password=password, log=log_api)

@babelonche_api.route('/mysql/stop/<string:password>', methods=['GET'])
def command_mysql_stop(password: str):
    """Arrête mysql"""
    return do_api_method(stop_mysql, password=password, log=log_api)

# ============== DATABASE ==================

@babelonche_api.route('/database/info', methods=['GET'])
def get_database_info_general():
    """Rencoie les infos générales de la database"""
    return do_api_method(api_method=get_database_data, log=log_api)


@babelonche_api.route('/database/import', methods=['GET'])
def get_database_imports():
    """Renvoie tout les fichiers d'import"""
    return do_api_method(api_method=get_database_import, log=log_api)


@babelonche_api.route('/database/import/change/<string:nom>', methods=['GET'])
def change_database_name(nom: str):
    """Permet de changer de base de donnée"""
    nom = nom.split("_")[-1].split(".")[0]
    return do_api_method(change_database, database=nom, log=log_api)

# =============== GENERAL ========================

@babelonche_api.route('general/info', methods=['GET'])
def get_info():
    """Info générales du webapp"""
    return do_api_method(api_method=get_database_version, log=log_api)


@babelonche_api.route('/general/import/<string:path>/<string:type_>', methods=['GET'])
def get_database_import_folder(path: str, type_: str = None, file: str = MYSQL_DATABASE):
    """Ne pas oublier de mettre le path avec de _ et non des /"""
    path = path.replace("_", "/")
    return do_api_method(get_file_inside_folder, folder=path, type_=type_, log=log_api)

# ================================================

app.register_blueprint(babelonche_api, url_prefix='/api/babelonche')

if __name__ == '__main__':
    app.run(debug=True)