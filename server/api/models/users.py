from ..utils import db
from datetime import datetime
from enum import Enum

class State(Enum):
    FCT='fct'
    ABIA='abia'

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False, unique=True)
    firstname = db.Column(db.String(64), nullable=False)
    lastname = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    phonenumber = db.Column(db.String(15), nullable=False, unique=True)
    country = db.Column(db.String(10), default='Nigeria', nullable=True)
    state = db.Column(db.Enum(State), default=State.FCT)
    image_file = db.Column(db.String(60), nullable=False, default='default.jpg')
    password_hash = db.Column(db.String(128))
    is_active = db.Column(db.Boolean(), default=False)
    is_admin = db.Column(db.Boolean(), default=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    is_verified = db.Column(db.Boolean(), default=False)
    is_banned = db.Column(db.Boolean(), default=False)
    post = db.relationship('Post', backref='author', lazy=True)


    def __repr__(self):
        return f'<User {self.username}>'
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)

    
