from ..utils import db
from datetime import datetime

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    state_id = db.Column(db.Integer, db.ForeignKey('states.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    type_id = db.Column(db.Integer, db.ForeignKey('types.id'), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    image_file = db.Column(db.String(60), nullable=False)
    available = db.Column(db.Boolean(), default=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    rented = db.relationship('Agreement', backref='author5', lazy=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    reviewpost = db.relationship('PostReview', backref='reviewpost', lazy=True)

    def __repr__(self):
        return f'<Post {self.id}>'
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)
    