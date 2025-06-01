from flask import Flask, request, jsonify, Blueprint
from src.download import download_and_save_tournaments
from src.process import process_and_save
from src.repository import Repository

app = Flask(__name__)
api = Blueprint('api', __name__, url_prefix='/api/pomysl-grandprix')
repository = Repository()

@api.route('/raw-data', methods=['GET'])
def get_raw_data():
    data = repository.get_raw_data()
    return jsonify(data), 200

@api.route('/data', methods=['GET'])
def get_data():
    data = repository.get_data()
    return jsonify(data), 200

@api.route('/update-data', methods=['POST'])
def update_data():
    download_and_save_tournaments()
    process_and_save()
    return 'Updated', 201

app.register_blueprint(api)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
