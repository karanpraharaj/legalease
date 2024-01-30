import logging
import uuid

from flask import request
from flask_restx import Resource

from src.transcribe import run_transcribe
from server.frameworks.api import api
from server.frameworks.serializers import api_token

ns = api.namespace('transcription', description='Operations related to audio transcription')


@ns.route('/')
class TranscriptionBatchSubmit(Resource):

    @api.response(200, 'Transcription request created', api_token)
    @api.response(400, 'Not accepted/parameters not supported')
    @api.marshal_with(api_token)
    def post(self):
        """
        Create a new batch for processing.
        """
        return_json = {
            'guid': uuid.uuid4(),
        }
        logging.info(f"Transcription token created: {return_json['guid']}")
        return return_json, 200


@ns.route('/<string:token>')
@ns.param('token', 'The transcription token')
class TranscriptionInformation(Resource):

    @ns.doc('get_transcription_information')
    @ns.marshal_with(api_token)
    def get(self, token):
        """
        Get information on a batch.
        """
        logging.info(f"Transcription token information: {token}")
        return_json = {
            'guid': token,
        }
        return return_json, 200
