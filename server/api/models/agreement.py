from ..utils import db
from datetime import datetime

class Agreement(db.Model):
    __tablename__ = 'Agreements'
    id = db.Column(db.Integer, primary_key=True)
    rented_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    returned_date = db.Column(db.DateTime)
    returned = db.Column(db.Boolean, nullable=False, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)

    def __repr__(self) -> str:
        return f"Agreement('{self.returned}')"
