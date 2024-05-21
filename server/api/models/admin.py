from ..utils import db
from datetime import datetime

class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(64), nullable=False, unique=True)
    firstname = db.Column(db.String(64), nullable=False)
    lastname = db.Column(db.String(64), nullable=False)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean(), default=True)
    image_file = db.Column(db.String(60), nullable=False, default='default.jpg')
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.username}>'
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)