from ...models.post import Post
from ...models.users import User
from flask import request
from flask_restx import Namespace, Resource, fields
from http import HTTPStatus
from flask_jwt_extended import jwt_required, get_jwt_identity
from ...utils import db
from .files import save_picture, allowed_file
from werkzeug.utils import secure_filename

post_namespace = Namespace('post', description="Name of the post")

post_model = post_namespace.model(
    'Post',{
        'id': fields.Integer(description='ID of the post'),
        'title': fields.String(description='Title of the post', required=True),
        'description': fields.String(description='Body of the post', required=True),
        'author': fields.Integer(attribute='author.id'),
        'state_id': fields.Integer(description='State of the post', required=True),
        'category_id': fields.Integer(description='Category of the post', required=True), 
        'type_id': fields.Integer(description='type of instrument', required=True),
        'price': fields.Integer(description='Price of rental',required=True),
        'image_file': fields.String(description='Image file',required=True),
        'available': fields.Boolean(description='Available'),
        'created_at': fields.DateTime(description='Date of creation')
    }
)

create_post_model = post_namespace.model(
    'CreatePost',{
        'id': fields.Integer(description='ID of the post'),
        'title': fields.String(description='Title of the post', required=True),
        'description': fields.String(description='Body of the post', required=True),
        'state_id': fields.Integer(description='State of the post', required=True),
        'category_id': fields.Integer(description='Category of the post', required=True), 
        'type_id': fields.Integer(description='type of instrument', required=True),
        'price': fields.Integer(description='Price of rental',required=True),
        'image_file': fields.String(description='Image file',required=True),
        'author': fields.Integer(description='Author of the post', required=True),
    }
)

update_post_model = post_namespace.model(
    'CreatePost',{
        'id': fields.Integer(description='ID of the post'),
        'title': fields.String(description='Title of the post', required=True),
        'description': fields.String(description='Body of the post', required=True),
        'state_id': fields.Integer(description='State of the post', required=True),
        'category_id': fields.Integer(description='Category of the post', required=True), 
        'type_id': fields.Integer(description='type of instrument', required=True),
        'price': fields.Integer(description='Price of rental',required=True),
        'image_file': fields.String(description='Image file',required=True),
        'author': fields.Integer(description='Author of the post', required=True),
        'available': fields.Boolean(description='Available'),
    }
)

instrument_status_model = post_namespace.model(
    'InstrumentStatus',{
        'available': fields.Boolean(description='the status of the post', required=True)
    }
)

@post_namespace.route('/posts/')
class PostList(Resource):
    @post_namespace.marshal_with(post_model)
    @post_namespace.doc(
        description="Get all posts"
    )
    @jwt_required()
    def get(self):
        """Provides a list of post"""
        posts = Post.query.all()

        return posts, HTTPStatus.OK

    @post_namespace.expect(create_post_model)
    @post_namespace.marshal_with(post_model)
    @post_namespace.doc(
        description="create a new post"
    )
    @jwt_required()
    def post(self):
        """Create a new post"""
        username = get_jwt_identity()
        current_user = User.query.filter_by(username=username).first()
        if not current_user:
            return {"message": "User not found"}, HTTPStatus.UNAUTHORIZED

        data = request.form

        required_fields = ['title', 'description', 'category_id', 'state_id', 'type_id', 'price']
        missing_fields = [field for field in required_fields if not data.get(field)]

        if missing_fields:
            return {"message": "Incomplete data", "missing_fields": missing_fields}, HTTPStatus.BAD_REQUEST


        new_post = Post(
            title=data.get('title'),
            description=data.get('description'),
            state_id=data.get('state_id'),
            category_id=data.get('category_id'),
            type_id=data.get('type_id'),
            price=data.get('price'),
        )

        file = request.files.get('image_file')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            picture_fn = save_picture(file)
            new_post.image_file = picture_fn
        else:
            return None
        
        new_post.user_id = current_user.id

        new_post.save()

        return new_post, HTTPStatus.CREATED
    
@post_namespace.route('/post/<int:post_id>')
class PostWithId(Resource):

    @post_namespace.expect(update_post_model)
    @post_namespace.marshal_with(post_model)
    @post_namespace.doc(
        description="Update a post"
    )
    @jwt_required()
    def put(self, post_id):
        """Update a post"""
        username = get_jwt_identity()

        post = Post.get_by_id(post_id)

        user = User.query.filter_by(username=username).first()

        if not user:
            return {"message": "User not found"}, HTTPStatus.NOT_FOUND

        if post.user_id != user.id:
            return {"message": "You are not authorized to update this post"}, HTTPStatus.FORBIDDEN

        data = request.form

        # Validate required fields
        required_fields = ['title', 'description', 'state_id', 'category_id', 'type_id', 'price', 'available']
        missing_fields = [field for field in required_fields if field not in data]

        if missing_fields:
            return {"message": "Incomplete data", "missing_fields": missing_fields}, HTTPStatus.BAD_REQUEST

        # Update post attributes
        post.title = data.get('title')
        post.description = data.get('description')
        post.state_id = data.get('state_id')
        post.category_id = data.get('category_id')
        post.type_id = data.get('type_id')
        post.price = data.get('price')
        # Convert available field to boolean
        available_str = data.get('available')
        if available_str is not None:
            post.available = available_str.lower() in ['true', '1', 't', 'y', 'yes']
        else:
            post.available = post.available

        # Handle image file upload
        file = request.files.get('image_file')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            picture_fn = save_picture(file)
            post.image_file = picture_fn

        # Commit the changes to the database
        db.session.commit()

        return post, HTTPStatus.NO_CONTENT

    @post_namespace.marshal_with(post_model)
    @post_namespace.doc(
        description="Get a post"
    )
    @jwt_required()
    def get(self, post_id):
        """Get a post"""
        post = Post.get_by_id(post_id)

        if not post:
            return {"message": "The requested post does not exist"}, HTTPStatus.NOT_FOUND

        return post, HTTPStatus.OK

    @post_namespace.marshal_with(post_model)
    @post_namespace.doc(
        description="Delete a post"
    )
    @jwt_required()
    def delete(self,post_id):
        "delete a post"
        username = get_jwt_identity()

        post = Post.get_by_id(post_id)

        user = User.query.filter_by(username=username).first()

        if not user:
            return {"message": "User not found"}, HTTPStatus.NOT_FOUND

        if post.user_id != user.id:
            return {"message": "You are not authorized to update this post"}, HTTPStatus.FORBIDDEN
        
        post.delete()

        return {"message":f"Deleted {post_id} successfully!!"}, HTTPStatus.NO_CONTENT

@post_namespace.route('/user/<int:user_id>/post/<int:post_id>')
class GetUserPost(Resource):

    @post_namespace.marshal_with(post_model)
    @post_namespace.doc(
        description="Get a post from a user"
    )
    @jwt_required()
    def get(self, user_id, post_id):
        """Get a post of a user"""
        user = User.get_by_id(user_id)

        post = Post.query.filter_by(id=post_id, user_id=user_id).first()

        if not post:
            return {"message": f"No post found with ID {post_id} for user ID {user_id}"}, HTTPStatus.NOT_FOUND

        return post, HTTPStatus.OK



@post_namespace.route('/user/<int:user_id>/post')
class GetUserPost(Resource):

    @post_namespace.marshal_with(post_model)
    @post_namespace.doc(
        description="Get all posts from a user"
    )
    @jwt_required()
    def get(self, user_id):
        """Get a list of post of a user"""
        user = User.get_by_id(user_id)

        if user is None:
            return {"message": f"No user with the ID {user_id} found"}, HTTPStatus.NOT_FOUND

        posts = user.post

        return posts, HTTPStatus.OK

@post_namespace.route('/post/status/<int:post_id>')
class InstrumentStatus(Resource):
    @post_namespace.expect(instrument_status_model)
    @post_namespace.marshal_with(post_model)
    @post_namespace.doc(
        description="Update the status of the specified post"
    )
    @jwt_required()
    def patch(self, post_id):
        """Update the status of a post"""
        username = get_jwt_identity()

        post = Post.get_by_id(post_id)

        user = User.query.filter_by(username=username).first()

        if not user:
            return {"message": "User not found"}, HTTPStatus.NOT_FOUND

        if post.user_id != user.id:
            return {"message": "You are not authorized to update this post"}, HTTPStatus.FORBIDDEN

        data = post_namespace.payload
        # Validate required fields
        required_fields = ['available']
        missing_fields = [field for field in required_fields if field not in data]

        if missing_fields:
            return {"message": "Incomplete data", "missing_fields": missing_fields}, HTTPStatus.BAD_REQUEST
        
        available_str = data.get('available')
        if available_str is not None:
            post.available = available_str.lower() in ['true', '1', 't', 'y', 'yes']
        else:
            post.available = post.available

        db.session.commit()

        return post, HTTPStatus.OK

    