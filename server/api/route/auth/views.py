from flask_restx import Namespace, Resource, fields
from flask import request, current_app
from ...models.users import User
from werkzeug.security import generate_password_hash, check_password_hash
from http import HTTPStatus
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt
from flask_login import logout_user
from werkzeug.utils import secure_filename
import os


auth_namespace = Namespace('auth', description='A namespace for authentication')

signup_model=auth_namespace.model(
    'SignUp',{
        'id':fields.Integer(),
        'username':fields.String(required=True, description='Username'),
        'email':fields.String(required=True, description='Email'),
        'password':fields.String(required=True, description='Password'),
        'confirmPassword':fields.String(required=True, description='Confirm Password'),
        'first_name':fields.String(required=True, description='First name'),
        'last_name':fields.String(required=True, description='Last name'),
        'phonenumber':fields.String(required=True, description='Phone number'),
        'country_id': fields.Integer(required=True, description='users country'),
        'state_id': fields.Integer(required=True, description='state of user')
    }
)

admin_model=auth_namespace.model(
    'SignUp',{
        'id':fields.Integer(),
        'username':fields.String(required=True, description='Username'),
        'email':fields.String(required=True, description='Email'),
        'password':fields.String(required=True, description='Password'),
        'confirmPassword':fields.String(required=True, description='Confirm Password'),
        'first_name':fields.String(required=True, description='First name'),
        'last_name':fields.String(required=True, description='Last name'),
        'phonenumber':fields.String(required=True, description='Phone number'),
        'country_id': fields.Integer(required=True, description='users country'),
        'state_id': fields.Integer(required=True, description='state of user'),
        'is_admin': fields.Boolean(required=True, description='if user is admin')
    }
)

user_model=auth_namespace.model(
    'User', {
        'id':fields.Integer(),
        'username':fields.String(required=True, description='Username'),
        'email':fields.String(required=True, description='Email'),
        'first_name':fields.String(required=True, description='First name'),
        'last_name':fields.String(required=True, description='Last name'),
        'phonenumber':fields.String(required=True, description='Phone number'),
        'country':fields.Integer(description='Country'),
        'image_file':fields.String(description='Image file'),
        'is_active':fields.Boolean(description='Is active'),
        'state':fields.Integer(description='State'),
        'is_admin':fields.Boolean(description='Is admin'),
        'date_created':fields.String(description='Date created'),
        'is_verified':fields.Boolean(description='Is verified'),
        'is_banned':fields.Boolean(description='Is banned'),
    }
)

login_model=auth_namespace.model(
    'Login', {
        'login': fields.String(required=True, description='Username or Email'),
        'password': fields.String(required=True, description='A Password')
    }
)

user_update_model = auth_namespace.model(
    'UserUpdate', {
        'first_name': fields.String(description='First name'),
        'last_name': fields.String(description='Last name'),
        'phonenumber': fields.String(description='Phone number'),
        'country': fields.Integer(description='Country'),
        'state': fields.Integer(description='State'),
        'image_file': fields.String(description='Image file')
    }
)

admin_update_model = auth_namespace.model(
    'AdminUpdate', {
        'is_admin': fields.Boolean(description='Admin status'),
        'is_verified': fields.Boolean(description='Verified status'),
        'is_banned': fields.Boolean(description='Banned status')
    }
)

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@auth_namespace.route('/signup/')
class Signup(Resource):
    @auth_namespace.expect(signup_model)
    @auth_namespace.marshal_with(user_model)
    def post(self):
        """Create a new user"""
        data = request.get_json()

        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        confirm_password = data.get('confirmPassword')
        phonenumber = data.get('phonenumber')

        # Check if passwords match
        if password != confirm_password:
            return {'message': 'Passwords do not match'}, HTTPStatus.BAD_REQUEST

        # Check if username, email, or phonenumber already exist
        if User.query.filter_by(username=username).first():
            return {'message': 'Username already exists'}, HTTPStatus.BAD_REQUEST
        if User.query.filter_by(email=email).first():
            return {'message': 'Email already exists'}, HTTPStatus.BAD_REQUEST
        if User.query.filter_by(phonenumber=phonenumber).first():
            return {'message': 'Phone number already exists'}, HTTPStatus.BAD_REQUEST
        
        # Create new user
        new_user = User(
            username=data.get('username'),
            email=data.get('email'),
            password_hash=generate_password_hash(data.get('password')),
            firstname=data.get('first_name'),
            lastname=data.get('last_name'),
            phonenumber=data.get('phonenumber'),
            country_id=data.get('country_id'),
            state_id=data.get('state_id'),
            is_admin=data.get('is_admin'),
        )

        new_user.save()

        return new_user, HTTPStatus.CREATED
    
@auth_namespace.route('/admin/signup/')
class Signup(Resource):
    @auth_namespace.expect(admin_model)
    @auth_namespace.marshal_with(admin_model)
    def post(self):
        """Create a new user"""
        data = request.get_json()

        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        confirm_password = data.get('confirmPassword')
        phonenumber = data.get('phonenumber')

        # Check if passwords match
        if password != confirm_password:
            return {'message': 'Passwords do not match'}, HTTPStatus.BAD_REQUEST

        # Check if username, email, or phonenumber already exist
        if User.query.filter_by(username=username).first():
            return {'message': 'Username already exists'}, HTTPStatus.BAD_REQUEST
        if User.query.filter_by(email=email).first():
            return {'message': 'Email already exists'}, HTTPStatus.BAD_REQUEST
        if User.query.filter_by(phonenumber=phonenumber).first():
            return {'message': 'Phone number already exists'}, HTTPStatus.BAD_REQUEST
        
        # Create new user
        new_user = User(
            username=data.get('username'),
            email=data.get('email'),
            password_hash=generate_password_hash(data.get('password')),
            firstname=data.get('first_name'),
            lastname=data.get('last_name'),
            phonenumber=data.get('phonenumber'),
            country_id=data.get('country_id'),
            state_id=data.get('state_id'),
            is_admin=data.get('is_admin'),
        )

        new_user.save()

        return new_user, HTTPStatus.CREATED
    
@auth_namespace.route('/login/')
class Login(Resource):
    @auth_namespace.expect(login_model)
    def post(self):
        """Authenticate user using JWT authentication"""

        data = request.get_json()

        login = data.get('login')
        password = data.get('password')

        user=User.query.filter((User.username == login) | (User.email == login)).first()

        if user is None:
            return {'message': 'Invalid username or email'}, HTTPStatus.UNAUTHORIZED

        if not check_password_hash(user.password_hash, password):
            return {'message': 'Invalid password'}, HTTPStatus.UNAUTHORIZED
        
        user.is_active = True
        user.save()

        access_token = create_access_token(identity=user.username)
        refresh_token = create_refresh_token(identity=user.username)

        response = {
            'access_token': access_token,
            'refresh_token': refresh_token
        }

        return response, HTTPStatus.OK
    
@auth_namespace.route('/logout/')
class Logout(Resource):
    @jwt_required()
    def post(self):
        """Log out user"""
        username=get_jwt_identity()

        # Fetch the current user's data from the database
        user = User.query.filter_by(username=username).first()

        if user:
            # Set the user's is_active field to False
            user.is_active = False
            user.save()

        get_token = get_jwt()
        
        logout_user(get_token)
        # Return a successful logout message
        return {'message': f'User {username} logged out successfully'}, HTTPStatus.OK
    
@auth_namespace.route('/refresh/')
class Refresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        """Get the refresh code of user"""
        username=get_jwt_identity()

        access_token=create_access_token(identity=username)

        return {"access_token":access_token}, HTTPStatus.OK
    
@auth_namespace.route('/update/')
class UpdateUser(Resource):
    
    @auth_namespace.expect(user_update_model)
    @auth_namespace.marshal_with(user_model)
    @jwt_required()
    def put(self):
        """Update a user"""
        username=get_jwt_identity()
        user=User.query.filter_by(username=username).first()

        if not user:
            return {'message': 'User not found'}, HTTPStatus.NOT_FOUND

        data = request.get_json()

        # Update the user's information
        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)
        user.phonenumber = data.get('phonenumber', user.phonenumber)
        user.country = data.get('country', user.country)
        user.state = data.get('state', user.state)

        if 'image_file' in request.files:
            file = request.files['image_file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                user.image_file = filename  

        # Commit the changes to the database
        user.save()

        return {'message': 'User information updated successfully'}, HTTPStatus.OK
    
@auth_namespace.route('/admin/update/<int:user_id>/')
class AdminUpdateUser(Resource):
    
    @auth_namespace.expect(admin_update_model)
    @jwt_required()
    def put(self, user_id):
        """Admin update user information"""
        # Here you should check if the current user is an admin
        username = get_jwt_identity()
        user = User.query.filter_by(username=username).first()

        if not user or not user.is_admin:
            return {'message': 'Admins only'}, HTTPStatus.FORBIDDEN

        # Fetch the user to be updated from the database
        user = User.query.get(user_id)

        if not user:
            return {'message': 'User not found'}, HTTPStatus.NOT_FOUND

        # Get the JSON data from the request
        data = request.get_json()

        # Update the user's admin-related information
        user.is_admin = data.get('is_admin', user.is_admin)
        user.is_verified = data.get('is_verified', user.is_verified)
        user.is_banned = data.get('is_banned', user.is_banned)

        # Commit the changes to the database
        user.save()

        return {'message': 'User information updated successfully'}, HTTPStatus.OK
