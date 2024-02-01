from werkzeug.datastructures import FileStorage
from flask_restx import fields
from server.frameworks.api import api

# GENERAL ###################################

api_token = api.model('API Token', {
    'guid': fields.String(required=True,
                          description='GUID received from token request.',
                          example='a1c3255e-eb8a-45e2-9163-5ab8dc5f3092',
                          pattern=r'^[0-9a-zA-Z]{8}-([0-9a-zA-Z]{4}-){3}[0-9a-zA-Z]{12}$'),
})

transcription_text = api.model('Transcription Text', {
    'text': fields.String(required=True,
                          description='Transcription text.',
                          example='This is a transcription.'),
})

# https://flask-restx.readthedocs.io/en/latest/parsing.html#file-upload
upload_parser = api.parser()
upload_parser.add_argument('file', location='files', type=FileStorage, required=True, help='Audio file to be transcribed.')

summarization_input_parser = api.parser()
summarization_input_parser.add_argument('review_findings', type=str, required=True, help='Text to be summarized.')
summarization_input_parser.add_argument('instructions', type=str, required=False, help='Instructions for summarization.')