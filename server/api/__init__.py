from flask import Flask, jsonify
from werkzeug.exceptions import RequestEntityTooLarge, NotFound, MethodNotAllowed, BadRequest, Unauthorized, Forbidden
from flask_restx import Api
from .config.config import config_dict
from .utils import db
from .models.users import User
from .models.admin import Admin
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
from flask_socketio import SocketIO
from flask_cors import CORS

def create_app(config=config_dict['prod']):
    app=Flask(__name__)
    CORS(app, supports_credentials=True)

    app.config.from_object(config)

    db.init_app(app)

    migrate = Migrate(app, db)

    socketio = SocketIO(app, cors_allowed_origins="*")

    authorizations = {
        "Bearer Auth":{
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            "description":"Add a JWT with ** Bearer &lt;JWT&gt; to authorize"
        }
    }

    api=Api(app,
        title="Instrulend",
        description="A rest api for peer to peer renting",
        authorizations=authorizations,
        security="Bearer Auth"
    )

    api.add_namespace(auth_namespace, path='/auth')
    api.add_namespace(category_namespace, path='/v1')
    api.add_namespace(country_namespace, path='/v1')
    api.add_namespace(post_namespace, path='/instrument')
    api.add_namespace(review_namespace, path='/review')
    api.add_namespace(message_namespace, path='/message')

    jwt = JWTManager(app)

    @socketio.on('connect')
    def handle_connect():
        print('Client connected')

    @socketio.on('disconnect')
    def handle_disconnect():
        print('Client disconnected')


    @api.errorhandler(RequestEntityTooLarge)
    def handle_request_entity_too_large(error):
        return {'message': 'File is too large. Maximum size is 5 MB.'}, 413
    
    @api.errorhandler(NotFound)
    def not_found(error):
        return {"error":"Not found"}, 404
    
    @api.errorhandler(MethodNotAllowed)
    def method_not_allowed(error):
        return {"error": "Method not allowed"}, 405

    @api.errorhandler(BadRequest)
    def bad_request(error):
        return {"error": "Bad Request"}, 400

    @api.errorhandler(Forbidden)
    def forbidden(error):
        return {"error": "Forbidden"}, 403

    @api.errorhandler(Unauthorized)
    def unauthorized(error):
        return {"error": "Unauthorized"}, 401

    @app.shell_context_processor
    def make_shell_context():
        return {
            'db': db, 
            'User': User,
            'Admin': Admin, 
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
    
    return app, socketio