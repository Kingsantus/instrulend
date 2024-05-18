from ..utils import db
from datetime import datetime
from enum import Enum

class State(Enum):
    FCT='fct'
    ABIA='abia'

class Instrument(Enum):
    GUITER='guiter'
    KEYBOARD='keyboard'
    DRUMS='drums'
    BASS='bass'
    VOCALS='vocals'

class Category(Enum):
    INSTRUMENTS='instruments'
    CLOTHES='clothes'
    ELECTRONIC='electronics'

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    state = db.Column(db.Enum(State), default=State.FCT)
    category = db.Column(db.Enum(Category), default=Category.INSTRUMENTS)
    instrument = db.Column(db.Enum(Instrument), default=Instrument.GUITER)
    price = db.Column(db.Integer, nullable=False)
    image_file = db.Column(db.String(60), nullable=False, default='default.jpg')
    available = db.Column(db.Boolean(), default=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'<Post {self.id}>'
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)
    