from app import api
from flask_restful import Resource


class TestEndpoint(Resource):
    def get(self):
        return {'test' : 'test'}


