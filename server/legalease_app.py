import os
import logging

from paste.translogger import TransLogger
from waitress import serve
from flask import Flask, Blueprint
from flask.logging import default_handler
from flask_cors import CORS

from server.frameworks.api import api
from server.endpoints.transcription import ts_ns as transcription_namespace
from server.endpoints.summarization import sum_ns as summarization_namespace

app = Flask(__name__)


@app.route('/version', methods=['GET'])
def version():
    return '1.0', 200


def initialize_app(flask_app):
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    blueprint = Blueprint('Endpoints', __name__, url_prefix='/api')
    api.init_app(blueprint)
    api.add_namespace(transcription_namespace)
    api.add_namespace(summarization_namespace)
    flask_app.register_blueprint(blueprint)


initialize_app(app)


def main():
    host = os.getenv('API_HOST', '0.0.0.0')
    port = os.getenv('API_PORT', '80')

    translogger_app = TransLogger(app)
    root = logging.getLogger()
    root.addHandler(default_handler)
    root.setLevel(os.getenv('LOG_LEVEL', 'INFO'))


    serve(translogger_app, host=host, port=port)


if __name__ == '__main__':
    main()
