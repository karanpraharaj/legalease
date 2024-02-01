from flask_restx import Resource

from server.frameworks.api import api
from server.frameworks.serializers import transcription_text, upload_parser

from src.upload_audio import store_audio_file, allowed_file
from src.transcribe import run_transcribe

ts_ns = api.namespace('transcription', description='Operations related to audio transcription')


@ts_ns.route('/')
class TranscriptionSubmit(Resource):

    @api.response(200, 'Transcription request created', transcription_text)
    @api.response(400, 'Not accepted/parameters not supported')
    @api.marshal_with(transcription_text)
    @api.expect(upload_parser)
    def post(self):
        """
        Submittal of new audio file for transcription
        """
        args = upload_parser.parse_args()
        uploaded_file = args['file']  # This is FileStorage instance
        model = args['model']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if uploaded_file.filename == '':
            return "No selected file", 400

        if not allowed_file(uploaded_file.filename):
            return "File type not allowed", 400

        stored_filepath = store_audio_file(uploaded_file)

        transcription = run_transcribe(
            audio_filepath=stored_filepath,
            model_name=model
        )

        return_json = {
            'text': transcription,
        }
        return return_json, 200
