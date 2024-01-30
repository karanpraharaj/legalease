import logging
import traceback

from flask_restx import Api

api = Api(version='1.0', title='RevealAI Legalease API', description='RevealAI Legalease API')


@api.errorhandler
def default_error_handler(e):
    message = 'An unhandled exception occurred.'
    logging.exception(traceback.format_exc())
    return {'message': message}, 500

