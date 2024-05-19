from flask import Flask
from flask_restx import Api
from .config.config import config_dict
from .utils import db
from .models.users import User
from .models.post import Post
from .models.enum import State, Category, Country, Type
from .models.agreement import Agreement
from .models.messages import Chat, Message
from .models.review import Review, Experience
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from .route.post.views import post_namespace
from .route.auth.views import auth_namespace
from .route.review.views import review_namespace
from .route.socketio.views import message_namespace
from .route.country.views import country_namespace
from .route.category.views import category_namespace

def create_app(config=config_dict['dev']):
    app=Flask(__name__)

    app.config.from_object(config)

    db.init_app(app)

    migrate = Migrate(app, db)

    api=Api(app)

    api.add_namespace(auth_namespace, path='/auth')
    api.add_namespace(category_namespace, path='/v1')
    api.add_namespace(country_namespace, path='/v1')
    api.add_namespace(post_namespace, path='/instrument')
    api.add_namespace(review_namespace, path='/review')
    api.add_namespace(message_namespace, path='/message')

    jwt = JWTManager(app)

    @app.shell_context_processor
    def make_shell_context():
        return {
            'db': db, 
            'User': User, 
            'Post': Post,
            'State': State,
            'Country': Country,
            'Category': Category,
            'Type': Type,
            'Agreement': Agreement,
            'Chat': Chat,
            'Message': Message,
            'Review': Review,
            'Experience': Experience,
        }

    return app