from ...models.post import Post
from ...models.users import User
from flask_restx import Namespace, Resource, fields
from http import HTTPStatus
from flask_jwt_extended import jwt_required, get_jwt_identity
from ...utils import db

post_namespace = Namespace('post', description="Name of the post")



post_model = post_namespace.model(
    'Post',{
        'id': fields.Integer(description='ID of the post'),
        'title': fields.String(description='Title of the post', required=True),
        'description': fields.String(description='Body of the post', required=True),
        'author': fields.Integer(description='Author of the post', required=True),
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
        'author': fields.Integer(description='Author of the post', required=True),
        'state_id': fields.Integer(description='State of the post', required=True),
        'category_id': fields.Integer(description='Category of the post', required=True), 
        'type_id': fields.Integer(description='type of instrument', required=True),
        'price': fields.Integer(description='Price of rental',required=True),
        'image_file': fields.String(description='Image file',required=True),
    }
)

@post_namespace.route('/posts/')
class PostList(Resource):
    @post_namespace.marshal_with(post_model)
    @jwt_required()
    def get(self):
        """Provides a list of post"""
        posts = Post.query.all()

        return posts, HTTPStatus.OK

    @post_namespace.expect(create_post_model)
    @post_namespace.marshal_with(post_model)
    @jwt_required()
    def post(self):
        """Create a new post"""
        username = get_jwt_identity()
        current_user = User.query.filter_by(username=username).first()
        if not current_user:
            return {"message": "User not found"}, HTTPStatus.UNAUTHORIZED

        data = post_namespace.payload

        new_post = Post(
            title=data['title'],
            description=data['description'],
            state_id=data['state_id'],
            category_id=data['category_id'],
            type_id=data['type_id'],
            price=data['price'],
            image_file=data['image_file']
        )

        new_post.author=current_user

        new_post.save()

        return new_post, HTTPStatus.CREATED
    
@post_namespace.route('/post/<int:post_id>')
class PostWithId(Resource):

    @post_namespace.expect(post_model)
    @post_namespace.marshal_with(post_model)
    @jwt_required()
    def put(self, post_id):
        """Update a post"""
        username = get_jwt_identity()

        post = Post.get_by_id(post_id)

        user = User.query.filter_by(username=username).first()

        if not user:
            return {"message": "User not found"}, HTTPStatus.UNAUTHORIZED

        if post.user_id != user.id:
            return {"message": "You are not authorized to update this post"}, HTTPStatus.FORBIDDEN

        data = post_namespace.payload

        post.title = data['title']
        post.description = data['description']
        post.state = data['state']
        post.category = data['category']
        post.instrument = data['instrument']
        post.price = data['price']
        post.available = data['available']
        post.image_file = data['image_file']

        db.session.commit()

        return post, HTTPStatus.OK

    @post_namespace.marshal_with(post_model)
    @jwt_required()
    def get(self, post_id):
        """Get a post"""
        post = Post.get_by_id(post_id)

        if not post:
            return {"message": "The requested post does not exist"}, HTTPStatus.NOT_FOUND

        return post, HTTPStatus.OK

    def delete(self,post_id):
        "delete a post"
        pass

@post_namespace.route('/user/<int:user_id>/post/<int:post_id>')
class GetUserPost(Resource):

    @post_namespace.marshal_with(post_model)
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
    def post(self, post_id):
        """Update the status of a post"""
        pass
    