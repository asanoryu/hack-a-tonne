from app import api, login
from flask_restful import Resource, reqparse
from app.models import User
from flask_login import current_user, login_user, logout_user,login_required


class TestEndpoint(Resource):
    def get(self):
        return {'test' : 'test'}

class UserProfile(Resource):
    def get(self, user_id=None):
        if not user_id:
            return {'error' : 'no user_id provided'}
        user = User.query.filter_by(id=user_id).first()
        if user:
            return user.to_dict()
        else:
            return {'error' : 'no such user'}

class LoginEndpoint(Resource):
    def __init__(self, *args, **kwargs):
        super(LoginEndpoint, self).__init__()
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username',
                                    type=str,
                                    required=True,
                                    help='No name provided',
                                    location='json')
        self.reqparse.add_argument('password',
                                    type=str,
                                    required=True,
                                    default="",
                                    help='No parameters provided',
                                    location='json')

    def post(self):
        args = self.reqparse.parse_args(strict=True)
        try:
            user = User.query.filter_by(username=args['username']).first()
            if user is None or not user.check_password(args['password']):
                return {'error' : 'Invalid username or password'}
            login_user(user, remember=True)
            return user.to_dict()
        except Exception as e:
            return {'error' : str(e)}

class CurrentUser(Resource):
    def get(self):
        print(current_user)
        if not current_user.is_authenticated:
            return {'error' : 'not logged in'}
        return current_user.to_dict()