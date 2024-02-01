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

summarization_text = api.model('Summarization Text', {
    'text': fields.String(required=True,
                          description='Summarization text.',
                          example='This is a summary.'),
})

classification_text = api.model('Classification Text', {
    'decision': fields.String(required=True,
                                description='Classification decision.',
                                example='This is a classification.'),
    'reason': fields.String(required=True,
                            description='Classification reason.',
                            example='This is a reason.'),
    'citations': fields.String(required=True,
                            description='Citations for classification.',
                            example='This is a citation.'),
})

# https://flask-restx.readthedocs.io/en/latest/parsing.html#file-upload
upload_parser = api.parser()
upload_parser.add_argument('file', location='files', type=FileStorage, required=True, help='Audio file to be transcribed.')

summarization_input_parser = api.parser()
summarization_input_parser.add_argument('review_findings', type=str, required=True, help='Text to be summarized.')
summarization_input_parser.add_argument('instructions', type=str, required=False, help='Instructions for summarization.')

classification_input_parser = api.parser()
classification_input_parser.add_argument('doc_text', type=str, required=True, help='Text to be classified.')
classification_input_parser.add_argument('issue', type=str, required=True, help='Issue to be classified.')