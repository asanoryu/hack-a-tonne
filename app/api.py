from app import api, login, db
from flask_restful import Resource, reqparse
from app.models import User, Sport, association_table_user_sport, Match
from flask_login import current_user, login_user, logout_user,login_required
import sqlalchemy
from flask import request

def arrayType(value, name):
    full_json_data = request.get_json()
    my_list = full_json_data[name]
    if(not isinstance(my_list, (list))):
        raise ValueError("The parameter " + name + " is not a valid array")
    return my_list



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
    def __init__(self, *args, **kwargs):
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
                                    type=arrayType,
                                    required=False,
                                    default="",
                                    location='json')
        self.reqparse.add_argument('city',
                                    type=str,
                                    location='json')
        self.reqparse.add_argument('phone',
                                    type=str,
                                    location='json')
        self.reqparse.add_argument('picture',
                                    type=str,
                                    location='json')
    def post(self):
        args = self.reqparse.parse_args()
        user = User(username=args['username'],email=args['email'])
        user.set_password(args['password'])
        user.city = args.get('city', None)  
        user.phone = args.get('phone', None)
        user.picture = args.get('picture', None)
        db.session.add(user)
        print(args['sports'])
        try:
            for _sport in args['sports']:
                print(_sport)
                sport = Sport.query.filter_by(name=_sport).first()
                if not sport:          
                    sport = Sport(name=_sport)
                    db.session.add(sport)
                db.session.flush()
                statement = association_table_user_sport.insert().values(user_id=user.id, sport_id=sport.id)
                db.session.execute(statement)
        except KeyError:
            pass
        try:
            
            db.session.commit()
        except sqlalchemy.exc.IntegrityError as e:
            db.session.rollback()
            print(e)
            return {'error' : 'user exists'}
        return user.to_dict()


class ChallengeEndpoint(Resource):
    def __init__(self, *args, **kwargs):
        super(ChallengeEndpoint, self).__init__()
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('defender_id',
                                    type=int,
                                    required=True,
                                    help='No defender provided',
                                    location='json')
        self.reqparse.add_argument('sport',
                                    type=str,
                                    required=True,
                                    default="",
                                    help='No sport provided',
                                    location='json')
    

    def post(self):
        args = self.reqparse.parse_args()
        defender = User.query.filter_by(id=args['defender_id']).first()
        if not defender:
            return {'error' : 'no such defender'}
        sport = Sport.query.filter_by(name=args['sport']).first()
        if not sport:
            return {'error' : 'no such sport'}

        match = Match(challenger_id=current_user.id, defender_id=defender.id, sport_id=sport.id)
        db.session.add(match)
        db.session.commit()
        return {'message' : 'success'}

class SuggestMatch(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        print(current_user)
        city = current_user.city
        parser.add_argument('sport_id', type=int)

        print( parser.parse_args())
        #return current_user.to_dict()

    def suggestMatch(city, sport):
        res=[]
        from_city=User.query.filter_by(city=city)
        for i in from_city:
            if sport in i.sports:
                res.append(i.to_dict())
        print(res)

class FindSuggestion(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        print(current_user.city)
        city = current_user.city
        parser.add_argument('sports', type=arrayType)

        #print( parser.parse_args())
        return self.suggestMatch(city, parser.parse_args().sports)

    def suggestMatch(self, city, sports):
        sports = Sport.query.filter(Sport.name.in_(sports)).all()
        sport_names = ''
        for sport in sports:
            sport_names += '"{}",'.format(sport.name)
        sport_names = sport_names[:-1]
        print(sport_names)
        result = db.engine.execute("SELECT * FROM `user` u INNER JOIN  user_sport us ON us.user_id =u.id \
INNER JOIN sport s ON s.id = us.sport_id WHERE s.name IN ({sports}) AND u.city = '{city}';".format(city=city,sports=sport_names))
        matches = []
        for res in result:
            print(res[0])
            if res[0] == current_user.id:
                continue
            user = User.query.filter(User.id == res[0]).first()
            sports = [s.name for s in user.sports]
            tmp = {'id' : res[0], 'username' : res[1], 'email' : res[2], 'city': res[5], 'sports' : sports}
            matches.append(tmp)
        return matches
        # sug = User.query.filter(User.city == city, Sport.id.in_(sids)).all()
        # print(sug)
        # return [u.to_dict() for u in sug]
        # # return User.query.filter(User.city == city, User.sports.in_(sports)).all()



class GetSports(Resource):
    def get(self):

        sports = Sport.query.all()
        sports = [i.to_dict() for i in sports]
        return sports



class NotificationEndpoint(Resource):
    def get(self):
        notifications = []
        defender_matches = Match.query.filter_by(defender_id = current_user.id, shown=False).order_by(Match.timest).all()
        print(defender_matches)
        if defender_matches:
            for match in defender_matches:
                notif = {'type' : 'challenge', 'from' : match.challenger_id.username, 'sport' : match.sport_id.name, 'timestamp': match.timest}
                match.shown = True
                db.session.commit()
                notifications.append(notif)

        challenges = Match.query.filter(Match.challenger_id == current_user.id, Match.accepted != 0).all()
        if challenges:
            for match in challenges:
                notif = {'type' : 'response', 'from' : match.defender_id.name, 'sport' : match.sport_id.name, 'timestamp': match.timest}
                if match.accepted == 1:
                    notif['response'] = 'accepted'
                elif match.accepted == 2:
                    notif['response'] = 'declined'
                notifications.append(notif)
        return sorted(notifications, key=lambda k: k['timestamp'])
