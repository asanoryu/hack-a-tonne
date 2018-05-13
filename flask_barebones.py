from app import app,db
import sqlalchemy
from flask_restful import Api
from app.api import TestEndpoint, UserProfile, LoginEndpoint
from app.api import CurrentUser, LogoutEndpoint, RegisterUserEndpoint
from app.api import FindSuggestion, SuggestMatch, GetSports
from app.api import ChallengeEndpoint
from app.api import NotificationEndpoint
from app.models import User, Sport, association_table_user_sport
import click
import faker
import random

fake = faker.Faker()

api = Api(app)
api.add_resource(TestEndpoint, '/api/test')
api.add_resource(UserProfile,'/api/user_profile/<int:user_id>', '/api/user_profile')
api.add_resource(LoginEndpoint, '/api/login')
api.add_resource(LogoutEndpoint, '/api/logout')
api.add_resource(RegisterUserEndpoint,'/api/register')
api.add_resource(CurrentUser, '/api/current_user')
api.add_resource(ChallengeEndpoint, '/api/challenge')
api.add_resource(SuggestMatch, '/api/suggest')
api.add_resource(FindSuggestion, '/api/suggestion')
api.add_resource(GetSports, '/api/sports')
api.add_resource(NotificationEndpoint, '/api/notifications')


@app.cli.command()
def seed():
    SPORTS = ['Basketball', 'Badmington', 'Football', 'Tennis', 'Other']
    CITIES = ['Sofia', 'Plovdiv', 'Varna']
    for COUNTER in range(20):
        random.shuffle(SPORTS)
        name = fake.name()
        user = User(username=name.replace(" ", ""),email=name.replace(" ", "_")+"@adidas.com")
        user.set_password("12345678")
        user.city = CITIES[int(random.random()*len(CITIES))]
        user.phone = fake.phone_number()
        user.picture = "picture.png"
        sports = SPORTS[:int(random.random()*len(SPORTS)+1)]

        try:
            for _sport in sports:
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
        user.sports = [Sport.query.filter_by(name=i).first() for i in sports]
        print(user.sports)
        db.session.add(user)
        try:
            
            db.session.commit()
        except sqlalchemy.exc.IntegrityError as e:
            db.session.rollback()
            print( {'error' : 'user exists'})