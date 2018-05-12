from app import api, login, db
from flask_restful import Resource, reqparse
from app.models import User, Sport, association_table_user_sport
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

class LogoutEndpoint(Resource):
    def get(self):
        logout_user()
        return {'message' : 'logged out'}


class RegisterUserEndpoint(Resource):
    super(RegisterUserEndpoint, self).__init__()
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
        self.reqparse.add_argument('email',
                                    type=str,
                                    required=True,
                                    default="",
                                    help='No parameters provided',
                                    location='json')
        self.reqparse.add_argument('sports',
                                    type=list,
                                    required=False,
                                    default="",
                                    location='json')
        self.reqparse.add_argument('city',
                                    type=str,
                                    location='json')
    def post(self):
        args = self.reqparse.parse_args()
        user = User(username=args['username'],email=args['password'])
        user.set_password(args['password'])
        try:
            user.city = args['city']
        except KeyError:
            user.city = None        
        try:
            for _sport in args['sports']:
                sport = Sport.query.filter_by(name=_sport)
                if not sport:          
                    sport = Sport(name=_sport)
                statement = association_table_user_sport.insert().values(user_id=user.id, sport_id=sport.id)
                db.session.execute(statement)
                db.session.commit()
        except KeyError:
            pass
        db.session.add(User)
        db.session.commit()

        return User.to_dict()