from flask import Flask, jsonify, Blueprint

app = Flask(__name__)
babelonche_api = Blueprint('babelonche_api', __name__)

@babelonche_api.route('/data', methods=['GET'])
def get_data():
    data = {"key": "value"}
    return jsonify(data)

app.register_blueprint(babelonche_api, url_prefix='/api/babelonche')

if __name__ == '__main__':
    app.run(debug=True)