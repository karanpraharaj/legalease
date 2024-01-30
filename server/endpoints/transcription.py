import logging
import uuid

from flask import request
from flask_restx import Resource

from src.transcribe import run_transcribe
from server.frameworks.api import api
from server.frameworks.serializers import api_token

ns = api.namespace('transcription', description='Operations related to audio transcription')


@ns.route('/create')
class TranscriptionBatchSubmit(Resource):

    @api.response(200, 'Transcription request created', api_token)
    @api.response(400, 'Not accepted/parameters not supported')
    def post(self):
        """
        Create a new batch for processing.
        """
        return_json = {
            'guid': uuid.uuid4(),
        }
        logging.info(f"Transcription token created: {return_json['guid']}")
        return return_json, 200


@ns.route('/information')
class TranscriptionInformation(Resource):

    @api.response(200, 'Information returned', api_token)
    @api.response(404, 'Batch not found in storage')
    @api.expect(api_token)
    @api.marshal_with(api_token)
    def post(self):
        """
        Get information on a batch.
        """
        token = request.json['guid']
        logging.info(f"Transcription token information: {token}")
        return_json = {
            'guid': token,
        }
        return return_json, 200
        # if batch_document is not None:
        #     batch_document['guid'] = batch_document['_id']
        #     return batch_document, 200
        # else:
        #     return '', 404
