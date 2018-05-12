from app import app
from flask_restful import Api
from app.api import TestEndpoint

api = Api(app)
api.add_resource(TestEndpoint, '/api/test')

