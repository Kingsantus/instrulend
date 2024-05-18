from ...models.post import Post
from ...models.users import User
from flask_restx import Namespace, Resource, fields
from http import HTTPStatus
from flask_jwt_extended import jwt_required, get_jwt_identity

post_namespace = Namespace('post', description="Name of the post")

post_model = post_namespace.model(
    'Post',{
        'id': fields.Integer(description='ID of the post'),
        'title': fields.String(description='Title of the post', required=True),
        'description': fields.String(description='Body of the post', required=True),
        'author': fields.String(description='Author of the post', required=True),
        'state': fields.String(description='State of the post'),
        'category': fields.String(description='Category of the post', required=True, enum=['INSTRUMENTS','CLOTHES', 'ELECTRONIC']), 
        'instrument': fields.String(description='type of instrument', required=True, enum=['GUITER', 'DRUMS', 'KEYBOARD', 'BASS', 'VOCAL']),
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
        'author': fields.String(description='Author of the post', required=True),
        'state': fields.String(description='State of the post'),
        'category': fields.String(description='Category of the post', required=True, enum=['INSTRUMENTS','CLOTHES', 'ELECTRONIC']), 
        'instrument': fields.String(description='type of instrument', required=True, enum=['GUITER', 'DRUMS', 'KEYBOARD', 'BASS', 'VOCAL']),
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

        data = post_namespace.payload

        new_post = Post(
            title=data['title'],
            description=data['description'],
            state=data['state'],
            category=data['category'],
            instrument=data['instrument'],
            price=data['price'],
            image_file=data['image_file']
        )

        new_post.author=current_user

        new_post.save()

        return new_post, HTTPStatus.CREATED
    
@post_namespace.route('/post/<int:post_id>')
class PostWithId(Resource):
    def put(self, post_id):
        """Update a post"""
        pass

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
    def get(self, user_id, post_id):
        """Get a post of a user"""
        pass

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

        if not posts:
            return {"message": f"No posts found for user ID {user_id}"}, HTTPStatus.OK

        return posts, HTTPStatus.OK

@post_namespace.route('/post/status/<int:post_id>')
class InstrumentStatus(Resource):
    def post(self, post_id):
        """Update the status of a post"""
        pass
    