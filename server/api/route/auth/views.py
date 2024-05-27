from flask_restx import Namespace, Resource, fields
from flask import request, current_app
from ...models.users import User
from ...models.admin import Admin
from werkzeug.security import generate_password_hash, check_password_hash
from http import HTTPStatus
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt
from flask_login import logout_user
from werkzeug.utils import secure_filename
from ...models.enum import State, Country
import os
from .utils import is_email_valid, is_password_valid, is_phone_valid
from .fille import allowed_file, save_picture
from werkzeug.utils import secure_filename
from werkzeug.exceptions import Conflict


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
        'country_id':fields.Integer(description='Country'),
        'image_file':fields.String(description='Image file'),
        'is_active':fields.Boolean(description='Is active'),
        'state_id':fields.Integer(description='State'),
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
        'country_id': fields.Integer(description='Country'),
        'state_id': fields.Integer(description='State'),
        'image_file': fields.String(description='Image file')
    }
)

admin_update_model = auth_namespace.model(
    'AdminUpdate', {
        'is_verified': fields.Boolean(description='Verified status'),
        'is_banned': fields.Boolean(description='Banned status')
    }
)

@auth_namespace.route('/signup/')
class Signup(Resource):
    @auth_namespace.expect(signup_model)
    @auth_namespace.marshal_with(user_model)
    def post(self):
        """Create a new user"""
        data = request.get_json()

        required_fields = ['username', 'email', 'password', 'confirmPassword', 'phonenumber', 'first_name', 'last_name', 'country_id', 'state_id']
        missing_fields = [field for field in required_fields if not data.get(field)]

        if missing_fields:
            return {"message": "Incomplete data", "missing_fields": missing_fields}, HTTPStatus.BAD_REQUEST

        username = data.get('username')
        email = data.get('email')
        if not is_email_valid(email):
            return {"message":"Email address is not valid"}, HTTPStatus.BAD_REQUEST
        password = data.get('password')
        if is_password_valid(password):
            return {"message":"Password is not valid"}, HTTPStatus.BAD_REQUEST
        confirm_password = data.get('confirmPassword')
        phonenumber = data.get('phonenumber')
        if not is_phone_valid(phonenumber):
            return {"message":"Phone number is not valid"}, HTTPStatus.BAD_REQUEST
        country_id = data.get('country_id')
        country = Country.query.filter_by(id=country_id).first()
        if not country:
            return {"message":"Country not found"}, HTTPStatus.BAD_REQUEST
        state_id = data.get('state_id')
        state = State.query.filter_by(id=state_id).first()
        if not state:
            return {"message":"Country not found"}, HTTPStatus.BAD_REQUEST
        

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
        

        try:
            # Create new user
            new_user = User(
                username=data.get('username'),
                email=data.get('email'),
                password_hash=generate_password_hash(data.get('password')),
                firstname=data.get('first_name'),
                lastname=data.get('last_name'),
                phonenumber=data.get('phonenumber'),
                country_id=country.id,
                state_id=state.id,
            )

            new_user.save()
        except Exception as e:
            raise Conflict(f"User exists, try another email, phone number and username")

        return new_user, HTTPStatus.CREATED
    
@auth_namespace.route('/admin/signup/')
class Signup(Resource):
    @auth_namespace.expect(admin_model)
    @auth_namespace.marshal_with(admin_model)
    def post(self):
        """Create a new admin"""
        data = request.get_json()
        required_fields = ['username', 'email', 'password', 'confirmPassword', 'first_name', 'last_name', 'is_admin']
        missing_fields = [field for field in required_fields if not data.get(field)]

        if missing_fields:
            return {"message": "Incomplete data", "missing_fields": missing_fields}, HTTPStatus.BAD_REQUEST

        username = data.get('username')
        email = data.get('email')
        if not is_email_valid(email):
            return {"message":"Email address is not valid"}, HTTPStatus.BAD_REQUEST
        password = data.get('password')
        if not is_password_valid(password):
            return {"message":"Password is not valid"}, HTTPStatus.BAD_REQUEST
        confirm_password = data.get('confirmPassword')

        # Check if passwords match
        if password != confirm_password:
            return {'message': 'Passwords do not match'}, HTTPStatus.BAD_REQUEST

        # Check if username, email, or phonenumber already exist
        if Admin.query.filter_by(username=username).first():
            return {'message': 'Username already exists'}, HTTPStatus.BAD_REQUEST
        if Admin.query.filter_by(email=email).first():
            return {'message': 'Email already exists'}, HTTPStatus.BAD_REQUEST
        
        # Create new user
        new_user = Admin(
            username=data.get('username'),
            email=data.get('email'),
            password_hash=generate_password_hash(data.get('password')),
            firstname=data.get('first_name'),
            lastname=data.get('last_name'),
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
        required_fields = ['login', 'password']
        missing_fields = [field for field in required_fields if not data.get(field)]

        if missing_fields:
            return {"message": "Incomplete data", "missing_fields": missing_fields}, HTTPStatus.BAD_REQUEST

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
    
@auth_namespace.route('/admin/login/')
class Login(Resource):
    @auth_namespace.expect(login_model)
    def post(self):
        """Authenticate admin using JWT authentication"""

        data = request.get_json()
        required_fields = ['login', 'password']
        missing_fields = [field for field in required_fields if not data.get(field)]

        if missing_fields:
            return {"message": "Incomplete data", "missing_fields": missing_fields}, HTTPStatus.BAD_REQUEST

        login = data.get('login')
        password = data.get('password')

        user=Admin.query.filter((Admin.username == login) | (Admin.email == login)).first()

        if user is None:
            return {'message': 'Invalid username or email'}, HTTPStatus.UNAUTHORIZED

        if not check_password_hash(user.password_hash, password):
            return {'message': 'Invalid password'}, HTTPStatus.UNAUTHORIZED

        access_token = create_access_token(identity=user.username)
        refresh_token = create_refresh_token(identity=user.username)

        response = {
            'access_token': access_token,
            'refresh_token': refresh_token
        }

        return response, HTTPStatus.OK
    
@auth_namespace.route('/admin/logout/')
class Logout(Resource):
    @jwt_required()
    def post(self):
        """Log out admin"""
        username=get_jwt_identity()

        # Fetch the current user's data from the database
        user = Admin.query.filter_by(username=username).first()

        if user:
            # Set the user's is_active field to False
            user.is_active = False
            user.save()

        get_token = get_jwt()
        
        logout_user(get_token)
        # Return a successful logout message
        return {'message': f'User {username} logged out successfully'}, HTTPStatus.OK



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
        username = get_jwt_identity()
        user = User.query.filter_by(username=username).first()

        if not user:
            return {'message': 'User not found'}, HTTPStatus.NOT_FOUND

        # Use request.form to get the form data and request.files to get the file
        data = request.form

        # Validate required fields
        required_fields = ['first_name', 'last_name', 'phonenumber', 'country_id', 'state_id']
        missing_fields = [field for field in required_fields if not data.get(field)]

        if missing_fields:
            return {"message": "Incomplete data", "missing_fields": missing_fields}, HTTPStatus.BAD_REQUEST

        # Update user data
        user.first_name = data.get('first_name')
        user.last_name = data.get('last_name')
        user.phonenumber = data.get('phonenumber')
        user.country_id = data.get('country_id')
        user.state_id = data.get('state_id')

        # Handle image file upload
        file = request.files.get('image_file')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            picture_fn = save_picture(file)
            user.image_file = picture_fn

        # Commit the changes to the database
        user.save()

        return {'message': 'User information updated successfully'}, HTTPStatus.OK
    
@auth_namespace.route('/admin/<int:user_id>/')
class AdminUpdateUser(Resource):
    
    @auth_namespace.expect(admin_update_model)
    @jwt_required()
    def put(self, user_id):
        """Admin update user information"""
        # Here you should check if the current user is an admin
        username = get_jwt_identity()
        admin = Admin.query.filter_by(username=username).first()

        if not admin:
            return {'message': 'Admins only'}, HTTPStatus.FORBIDDEN

        # Fetch the user to be updated from the database
        user = User.query.get(user_id)

        if not user:
            return {'message': 'User not found'}, HTTPStatus.NOT_FOUND

        # Get the JSON data from the request
        data = request.get_json()

        required_fields = ['is_verified', 'is_banned']
        missing_fields = [field for field in required_fields if not data.get(field)]

        if missing_fields:
            return {"message": "Incomplete data", "missing_fields": missing_fields}, HTTPStatus.BAD_REQUEST

        # Update the user's admin-related information
        user.is_verified = data.get('is_verified', user.is_verified)
        user.is_banned = data.get('is_banned', user.is_banned)

        # Commit the changes to the database
        user.save()

        return {'message': 'User information updated successfully'}, HTTPStatus.OK
    
    @auth_namespace.marshal_with(user_model)
    @jwt_required()
    def delete(self, user_id):
        """Deleting User after banning them"""
        username = get_jwt_identity()
        admin = Admin.query.filter_by(username=username).first()

        if not admin:
            return {"message":"Your not authorized, Admin only"}, HTTPStatus.FORBIDDEN
        
        user = User.get_by_id(user_id)

        if user.is_banned != True:
            return {"message":"User not banned cannot be deleted"}, HTTPStatus.BAD_REQUEST
        
        user.delete()

        return {"message":"User deleted Successfully"}, HTTPStatus.OK
