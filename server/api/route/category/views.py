from flask_restx import Namespace, Resource, fields
from ...models.enum import Category, Type
from ...models.users import User
from http import HTTPStatus
from flask_jwt_extended import jwt_required, get_jwt_identity

category_namespace = Namespace('category', description='A namespace for category of Enum')

type_model = category_namespace.model(
    'Type', {
        'id': fields.Integer(description='Id of the type'),
        'name': fields.String(description='Name of the type', required=True),
        'category_id': fields.Integer(description='Country ID', required=True)
    }
)

cat_model = category_namespace.model(
    'Category', {
        'id': fields.Integer(description='Id of the category'),
        'name': fields.String(description='Name of the category', required=True)
    }
)

@category_namespace.route('/category')
class CreateGetCategory(Resource):

    @category_namespace.marshal_with(cat_model)
    @jwt_required()
    def get(self):
        """Fetching List of Categories"""
        categories = Category.query.all()

        return categories, HTTPStatus.OK

    @category_namespace.expect(cat_model)
    @category_namespace.marshal_with(cat_model)
    @jwt_required()
    def post(self):
        """Creating a new category"""
        username = get_jwt_identity()
        current_user = User.query.filter_by(username=username).first()

        if current_user is None or current_user.is_admin != 'admin':
            return {"message": "You are not allowed"}, HTTPStatus.FORBIDDEN
        
        data = category_namespace.payload

        new_post = Category(
            name = data['name']
        )

        new_post.save()

        return new_post, HTTPStatus.CREATED

@category_namespace.route('/category/<int:category_id>')
class DelUpdateCategory(Resource):

    @category_namespace.marshal_with(cat_model)
    @jwt_required()
    def delete(self, category_id):
        """Deleting a category"""
        username = get_jwt_identity()

        current_user = User.query.filter_by(username=username).first()

        if current_user is None or current_user.is_admin != 'admin':
            return {"message": "You are not allowed"}, HTTPStatus.FORBIDDEN
        
        category = Category.get_by_id(category_id)
        
        category.delete()

        return {"message": "Category deleted successfully"}, HTTPStatus.OK

@category_namespace.route('/types')
class CreateGetTypes(Resource):

    @category_namespace.marshal_with(type_model)
    @jwt_required()
    def get(self):
        """Fetching list of types"""
        types = Type.query.all()

        return types, HTTPStatus.OK

    @category_namespace.expect(type_model)
    @category_namespace.marshal_with(type_model)
    @jwt_required()
    def post(self):
        """Creating a new type"""
        username = get_jwt_identity()
        current_user = User.query.filter_by(username=username).first()

        if current_user is None or current_user.is_admin != 'admin':
            return {"message": "You are not allowed"}, HTTPStatus.FORBIDDEN
        
        data = category_namespace.payload

        new_post = Type(
            name = data['name'],
            category_id = data['category_id']
        )

        new_post.save()

        return new_post, HTTPStatus.CREATED

@category_namespace.route('/type/<int:type_id>')
class DelUpdateTypes(Resource):

    @category_namespace.marshal_with(type_model)
    @jwt_required()
    def delete(self, type_id):
        """Deleting a type"""
        username = get_jwt_identity()

        current_user = User.query.filter_by(username=username).first()

        if current_user is None or current_user.is_admin != 'admin':
            return {"message": "You are not allowed"}, HTTPStatus.FORBIDDEN
        
        type = Type.get_by_id(type_id)
        
        type.delete()

        return {"message": "Type deleted successfully"}, HTTPStatus.OK

@category_namespace.route('/category/<int:category_id>/types')
class GetAllCategory(Resource):
    @category_namespace.marshal_with(cat_model)
    @jwt_required()
    def get(self, category_id):
        """Fetching list of a category with types"""
        category = Category.get_by_id(category_id)

        if category is None:
            return {"message": "Category not found"}, HTTPStatus.NOT_FOUND

        category_info = category.types

        return category_info, HTTPStatus.OK
