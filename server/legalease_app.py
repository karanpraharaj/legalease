import os

from paste.translogger import TransLogger
from waitress import serve
from flask import Flask, Blueprint

from server.frameworks.api import api
from server.endpoints.transcription import ns as transcription_namespace

app = Flask(__name__)


@app.route('/version', methods=['GET'])
def version():
    return '1.0', 200


def initialize_app(flask_app):
    blueprint = Blueprint('Endpoints', __name__, url_prefix='/api')
    api.init_app(blueprint)
    api.add_namespace(transcription_namespace)
    flask_app.register_blueprint(blueprint)


initialize_app(app)


def main():
    host = os.getenv('API_HOST', '0.0.0.0')
    port = os.getenv('API_PORT', '8080')
    serve(TransLogger(app), host=host, port=port)


if __name__ == '__main__':
    main()
