import os

from paste.translogger import TransLogger
from waitress import serve
from logging.config import dictConfig
from flask import Flask, Blueprint

from endpoints.transcription import ns as transcription_namespace
from frameworks.api import api

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

app = Flask(__name__)


@app.route('/version', methods=['GET'])
def version():
    return '1.0', 200


def initialize_app(flask_app):
    flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = 'list'
    flask_app.config['RESTPLUS_VALIDATE'] = True
    flask_app.config['RESTPLUS_MASK_SWAGGER'] = False
    flask_app.config['ERROR_404_HELP'] = False

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
