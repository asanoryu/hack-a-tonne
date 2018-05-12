from app import app
from flask_restful import Api
from app.api import TestEndpoint, UserProfile, LoginEndpoint, SuggestMatch
from app.api import CurrentUser, LogoutEndpoint, RegisterUserEndpoint
from app.api import FindSuggestion


api = Api(app)
api.add_resource(TestEndpoint, '/api/test')
api.add_resource(UserProfile,'/api/user_profile/<int:user_id>', '/api/user_profile')
api.add_resource(LoginEndpoint, '/api/login')
api.add_resource(LogoutEndpoint, '/api/logout')
api.add_resource(RegisterUserEndpoint,'/api/register')
api.add_resource(CurrentUser, '/api/current_user')
api.add_resource(SuggestMatch, '/api/suggest')
api.add_resource(FindSuggestion, '/api/suggestion')


