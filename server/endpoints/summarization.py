from flask_restx import Resource

from server.frameworks.api import api
from server.frameworks.serializers import summarization_text, summarization_input_parser

from src.summarize import run_summarize

ns = api.namespace('summarization', description='Operations related to summarization of review findings')


@ns.route('/')
class TranscriptionSubmit(Resource):

    @api.response(200, 'Summarization request created', summarization_text)
    @api.response(400, 'Not accepted/parameters not supported')
    @api.marshal_with(summarization_text)
    @api.expect(summarization_input_parser)
    def post(self):
        """
        Submittal of new audio file for transcription
        """
        args = summarization_input_parser.parse_args()
        submitted_text = args['review_findings'] 
        instructions = args['instructions']
        
        if submitted_text == '':
            return "No selected file", 400

        transcription = run_summarize(
            submitted_text,
            instructions
        )

        return_json = {
            'text': transcription,
        }
        return return_json, 200
