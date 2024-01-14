import os
import sys

parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(parent_dir)

from flask import Flask, jsonify, Blueprint
from config.Variables.variables import *
from BDD.bdd import BDD

from function import *

app = Flask(__name__)
babelonche_api = Blueprint('babelonche_api', __name__)

# ================ Obtenir l'état de mysql ================

@babelonche_api.route('/mysql', methods=['GET'])
def get_mysql():
    _RUN = False
    text = get_mysql_base()
    if ''.join(text).find("running") > 0:
        _RUN = True
    data = {"state": text, "running": _RUN}
    return jsonify(data)

# ================= information footer ================

@babelonche_api.route('/info', methods=['GET'])
def get_info():
    data = get_version_variables()
    return jsonify(data)

@babelonche_api.route('/connexion', methods=['GET'])
def get_connexion_state():
    data = get_mysql_parameter()
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

@babelonche_api.route('/database/import/<string:path>/<string:type_>', methods=['GET'])
def get_database_import_folder(path: str, type_: str = None, file: str = MYSQL_DATABASE):
    """Ne pas oublier de mettre le path avec de _ et non des /"""
    path = path.replace("_", "/")
    data = get_file_inside(path, type_, file)
    return jsonify(data)

@babelonche_api.route('/database/import/change/<string:nom>', methods=['GET'])
def change_database_name(nom: str):
    nom = nom.split("_")[-1].split(".")[0]
    val = change_database(nom)
    return jsonify(val)

# ================================================

app.register_blueprint(babelonche_api, url_prefix='/api/babelonche')

if __name__ == '__main__':
    app.run(debug=True)