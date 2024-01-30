from flask_restx import fields
from server.frameworks.api import api

# GENERAL ###################################

api_token = api.model('API Token', {
    'guid': fields.String(required=True,
                          description='GUID received from token request.',
                          example='a1c3255e-eb8a-45e2-9163-5ab8dc5f3092',
                          pattern=r'^[0-9a-zA-Z]{8}-([0-9a-zA-Z]{4}-){3}[0-9a-zA-Z]{12}$'),
})
