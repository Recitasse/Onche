from flask import Flask, jsonify, Blueprint
from config.Variables.variables import *

app = Flask(__name__)
babelonche_api = Blueprint('babelonche_api', __name__)

from WebAPP.API.function.database.mysql import *
from WebAPP.API.function.database.database import *
from WebAPP.API.function.utils.general import *

# ================ Obtenir l'état de mysql ================

@babelonche_api.route('/mysql/state', methods=['GET'])
def get_mysql():
    _RUN = False
    text = get_mysql_status()
    if ''.join(text).find("running") > 0:
        _RUN = True
    data = {"state": text, "running": _RUN}
    return jsonify(data)


@babelonche_api.route('/mysql/info', methods=['GET'])
def get_mysql_info():
    data = get_mysql_database_info()
    return jsonify(data)


@babelonche_api.route('/mysql/database', methods=['GET'])
def get_mysql_database():
    """Donne les databases dans le répertoire d'import"""
    data = get_mysql_available_database()
    return jsonify(data)

@babelonche_api.route('/mysql/start/<string:password>', methods=['GET'])
def command_mysql_start(password: str):
    """Démrre mysql"""
    data = start_mysql(password)
    return jsonify(data)

@babelonche_api.route('/mysql/stop/<string:password>', methods=['GET'])
def command_mysql_stop(password: str):
    """Démrre mysql"""
    data = stop_mysql(password)
    return jsonify(data)

# ============== DATABASE ==================

@babelonche_api.route('/database/info', methods=['GET'])
def get_database_info_general():
    try:
        data = get_database_data()
    except Exception as e:
        data = {}
    return jsonify(data)


@babelonche_api.route('/database/import', methods=['GET'])
def get_database_imports():
    data = get_database_import()
    return jsonify(data)


@babelonche_api.route('/database/import/change/<string:nom>', methods=['GET'])
def change_database_name(nom: str):
    nom = nom.split("_")[-1].split(".")[0]
    val = change_database(nom)
    return jsonify(val)

# =============== GENERAL ========================

@babelonche_api.route('general/info', methods=['GET'])
def get_info():
    data = get_database_version()
    return jsonify(data)


@babelonche_api.route('/general/import/<string:path>/<string:type_>', methods=['GET'])
def get_database_import_folder(path: str, type_: str = None, file: str = MYSQL_DATABASE):
    """Ne pas oublier de mettre le path avec de _ et non des /"""
    path = path.replace("_", "/")
    data = get_file_inside_folder(path, type_, file)
    return jsonify(data)

# ================================================

app.register_blueprint(babelonche_api, url_prefix='/api/babelonche')

if __name__ == '__main__':
    app.run(debug=True)