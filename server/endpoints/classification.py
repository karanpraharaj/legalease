from flask_restx import Resource

from server.frameworks.api import api
from server.frameworks.serializers import classification_input_parser, classification_obj

from src.classify import run_classify   

cl_ns = api.namespace('classification', description='Operations related to classification')


@cl_ns.route('/')
class ClassificationSubmit(Resource):

    @api.response(200, 'Classification request created', classification_obj)
    @api.response(400, 'Not accepted/parameters not supported')
    @api.marshal_with(classification_obj)
    @api.expect(classification_input_parser)
    def post(self):
        """
        Submittal of new audio file for transcription
        """
        args = classification_input_parser.parse_args()
        doc_text = args['doc_text']
        issue = args['issue']

        if doc_text == '':
            return "Doc text is empty", 400
        
        if issue == '':
            return "Issue is empty", 400

        decision, reason, citations = run_classify(
            doc_text,
            issue
        )

        return_json = {
            'decision': decision,
            'reason': reason,
            'citations': citations,
        }
        return return_json, 200
