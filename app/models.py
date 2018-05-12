from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
# from geoalchemy2 import Geometry

association_table_event_invitations = db.Table('event_user_invitations', db.Model.metadata,
    db.Column('event_id', db.Integer, db.ForeignKey('event.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)
association_table_user_sport = db.Table('user_sport', db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('sport_id', db.Integer, db.ForeignKey('sport.id'))
)


class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    phone = db.Column(db.String(32))
    city = db.Column(db.String(32))
    picture = db.Column(db.String(64))
    events = db.relationship('Event', backref='user')
    sports = db.relationship("Sport",
                    secondary=association_table_user_sport)

    def __repr__(self):

        return '<User {}>'.format(self.username)
    
    def to_dict(self):
        return {'user' : self.username, 'email': self.email, 'id': self.id, 'city' : self.city, 'picture': self.picture, 'sports': self.get_sports()}

    def get_sports(self):
        return [s.name for s in self.sports]
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username


class Sport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    description = db.Column(db.String(2048), index=True)
    
    def __repr__(self):
        return '<Sport {}>'.format(self.name)    

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(64), index=True, unique=True, nullable=False)
    status = db.Column(db.String(64), index=True, nullable=False)
    when = db.Column(db.Date, index=True,nullable=False)
    sport_id = db.Column(db.Integer, db.ForeignKey(Sport.id), primary_key=True, nullable=False)
    
    user_id =  db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True,
        nullable=False)
    users = db.relationship("User",
                    secondary=association_table_event_invitations,)

    def __repr__(self):
        return '<Event {}>'.format(self.name)    
    





@login.user_loader
def load_user(id):
    return User.query.filter_by(username=id).first()
