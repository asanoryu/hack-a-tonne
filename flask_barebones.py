from app import app
from flask_restful import Api
from app.api import TestEndpoint, UserProfile, LoginEndpoint

api = Api(app)
api.add_resource(TestEndpoint, '/api/test')
api.add_resource(UserProfile,'/api/user_profile/<int:user_id>', '/api/user_profile')
api.add_resource(LoginEndpoint, '/api/login')

