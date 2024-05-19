from app import db, login_manager
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from sqlalchemy.orm import validates
from flask_login import UserMixin
from enum import Enum
from datetime import datetime
from hashlib import sha256
from flask import current_app

class Category(Enum):
    KEYBOARDS_SYNTHESIZERS = 'Keyboards & Synthesizers'
    ELECTRIC_GUITARS = 'Electric Guitars'
    ACOUSTIC_GUITARS = 'Acoustic Guitars'
    BASS_GUITARS = 'Bass Guitars'
    DRUM_KITS = 'Drum Kits'
    ELECTRONIC_DRUM_MACHINES = 'Electronic Drum Machines'
    DJ_CONTROLLERS = 'DJ Controllers'
    TURNTABLES = 'Turntables'
    MIXERS_AUDIO = 'Mixers (Audio)'
    MICROPHONES = 'Microphones'
    HEADPHONES = 'Headphones'
    PA_SYSTEMS = 'PA Systems'
    STUDIO_MONITORS = 'Studio Monitors'
    STAGE_LIGHTING = 'Stage Lighting'
    EFFECTS_PEDALS = 'Effects Pedals'
    AUDIO_INTERFACES = 'Audio Interfaces'
    MIDI_CONTROLLERS = 'MIDI Controllers'
    DIGITAL_PIANOS = 'Digital Pianos'
    STAGE_AMPLIFIERS = 'Stage Amplifiers'
    RECORDING_EQUIPMENT = 'Recording Equipment'
    KARAOKE_MACHINES = 'Karaoke Machines'
    CD_PLAYERS_RECORDERS = 'CD Players & Recorders'
    TAPE_DECKS = 'Tape Decks'
    VINYL_RECORDS = 'Vinyl Records'
    CABLES_CONNECTORS = 'Cables & Connectors'
    MUSICAL_INSTRUMENT_CASES_BAGS = 'Musical Instrument Cases & Bags'
    MUSIC_STANDS = 'Music Stands'
    INSTRUMENT_ACCESSORIES = 'Instrument Accessories (e.g., guitar picks, drumsticks)'
    SPEAKER_STANDS = 'Speaker Stands'
    SUBWOOFERS = 'Subwoofers'
    PORTABLE_PA_SYSTEMS = 'Portable PA Systems'
    LIVE_SOUND_MIXERS = 'Live Sound Mixers'
    WIRELESS_MICROPHONE_SYSTEMS = 'Wireless Microphone Systems'
    IN_EAR_MONITORS = 'In-Ear Monitors'
    DIGITAL_AUDIO_WORKSTATIONS = 'Digital Audio Workstations (DAWs)'
    MUSIC_PRODUCTION_SOFTWARE = 'Music Production Software'
    SAMPLE_LIBRARIES_SOUND_PACKS = 'Sample Libraries & Sound Packs'
    SOUND_MODULES = 'Sound Modules'
    MUSIC_PRODUCTION_CONTROLLERS = 'Music Production Controllers'
    ANALOG_SYNTHESIZERS = 'Analog Synthesizers'
    EFFECTS_PROCESSORS = 'Effects Processors'
    SPEAKER_CABINETS = 'Speaker Cabinets'
    SPEAKER_COMPONENTS = 'Speaker Components (e.g., woofers, tweeters)'
    POWER_AMPLIFIERS = 'Power Amplifiers'
    KARAOKE_MICROPHONES = 'Karaoke Microphones'
    KARAOKE_SPEAKERS = 'Karaoke Speakers'
    DJ_LIGHTING = 'DJ Lighting'
    DJ_SOFTWARE = 'DJ Software'
    DJ_MIXERS = 'DJ Mixers'
    DJ_TURNTABLE_CARTRIDGES = 'DJ Turntable Cartridges'

class City(Enum):
    ABIA = 'Abia'
    ADAMAWA = 'Adamawa'
    AKWA_IBOM = 'Akwa Ibom'
    ANAMBRA = 'Anambra'
    BAUCHI = 'Bauchi'
    BAYELSA = 'Bayelsa'
    BENUE = 'Benue'
    BORNO = 'Borno'
    CROSS_RIVER = 'Cross River'
    DELTA = 'Delta'
    EBONYI = 'Ebonyi'
    EDO = 'Edo'
    EKITI = 'Ekiti'
    ENUGU = 'Enugu'
    FCT = 'FCT'
    GOMBE = 'Gombe'
    IMO = 'Imo'
    JIGAWA = 'Jigawa'
    KADUNA = 'Kaduna'
    KANO = 'Kano'
    KATSINA = 'Katsina'
    KEBBI = 'Kebbi'
    KOGI = 'Kogi'
    KWARA = 'Kwara'
    LAGOS = 'Lagos'
    NASARAWA = 'Nasarawa'
    NIGER = 'Niger'
    OGUN = 'Ogun'
    ONDO = 'Ondo'
    OSUN = 'Osun'
    OYO = 'Oyo'
    PLATEAU = 'Plateau'
    RIVERS = 'Rivers'
    SOKOTO = 'Sokoto'
    TARABA = 'Taraba'
    YOBE = 'Yobe'
    ZAMFARA = 'Zamfara'

class Rating(Enum):
    ZERO = 0
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    phone_number = db.Column(db.String(15), unique=True, nullable=False)
    city = db.Column(db.String(50))
    country = db.Column(db.String(10), nullable=False, default='Nigeria')
    password = db.Column(db.String(60), nullable=False)
    verification_number = db.Column(db.String(25), unique=True)
    verified_user = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    image_file = db.Column(db.String(50), nullable=False, default='default.jpg')
    posts = db.relationship('Post', backref='author', lazy=True)
    reviewer = db.relationship('Review', foreign_keys='Review.user_id', backref='author1', lazy=True)
    reviewed = db.relationship('Review', foreign_keys='Review.author_id', backref='author2', lazy=True)
    rented = db.relationship('Agreement', backref='author4', lazy=True)
    expirence = db.relationship('Expirence', backref='author6', lazy=True)
    chats_user1 = db.relationship('Chat', backref='user1', foreign_keys='Chat.user1_id', lazy=True)
    chats_user2 = db.relationship('Chat', backref='user2', foreign_keys='Chat.user2_id', lazy=True)
    message = db.relationship('Message', backref='author7', lazy=True)

    def get_reset_token(self, expires_sec=900):
        serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        return serializer.dumps({'user_id': self.id})
    
    @staticmethod
    def verify_reset_token(token, max_age=900):
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        try:
            data = serializer.loads(token, max_age=max_age)
            user_id = data['user_id']
            return User.query.get(user_id)
        except SignatureExpired:
            return None  
        except BadSignature:
            return None  

    def __repr__(self):
        return f"User('{self.first_name}', '{self.last_name}', '{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    city = db.Column(db.String(50), nullable=False)
    country = db.Column(db.String(10), nullable=False, default='Nigeria')
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    image_file = db.Column(db.String(50), nullable=False)
    availability = db.Column(db.Boolean, nullable=False, default=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    rented = db.relationship('Agreement', backref='author5', lazy=True)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
    
class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    star_rating = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Review('{self.content}')"

class Agreement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rented_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    returned_date = db.Column(db.DateTime)
    returned = db.Column(db.Boolean, nullable=False, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

    def __repr__(self) -> str:
        return f"Agreement('{self.returned}')"
    
class Expirence(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    star_rating = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Review('{self.content}')"

class Chat(db.Model):
    id = db.Column(db.String(64), primary_key=True)
    user1_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user2_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    messages = db.relationship('Message', backref='chat', lazy=True)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.String(64), db.ForeignKey('chat.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime)