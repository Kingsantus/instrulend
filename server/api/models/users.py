from ..utils import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False, unique=True)
    firstname = db.Column(db.String(64), nullable=False)
    lastname = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    phonenumber = db.Column(db.String(15), nullable=False, unique=True)
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'), nullable=False)
    state_id = db.Column(db.Integer, db.ForeignKey('states.id'), nullable=False)
    image_file = db.Column(db.String(60), nullable=False, default='default.jpg')
    password_hash = db.Column(db.String(128))
    is_active = db.Column(db.Boolean(), default=False)
    is_admin = db.Column(db.Boolean(), default=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    is_verified = db.Column(db.Boolean(), default=False)
    is_banned = db.Column(db.Boolean(), default=False)
    post = db.relationship('Post', backref='author', lazy=True)
    reviewer = db.relationship('Review', foreign_keys='Review.user_id', backref='author1', lazy=True)
    reviewed = db.relationship('Review', foreign_keys='Review.author_id', backref='author2', lazy=True)
    rented = db.relationship('Agreement', backref='author4', lazy=True)
    experience = db.relationship('Experience', backref='author6', lazy=True)
    chats_user1 = db.relationship('Chat', backref='user1', foreign_keys='Chat.user1_id', lazy=True)
    chats_user2 = db.relationship('Chat', backref='user2', foreign_keys='Chat.user2_id', lazy=True)
    message = db.relationship('Message', backref='author7', lazy=True)



    def __repr__(self):
        return f'<User {self.username}>'
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)

    
