from flask_restx import Namespace, Resource, fields
from ...models.enum import State, Country
from ...models.users import User
from http import HTTPStatus
from flask_jwt_extended import jwt_required, get_jwt_identity

country_namespace = Namespace('country', description='A namespace for country of Enum')

state_model = country_namespace.model(
    'State', {
        'id': fields.Integer(description='Id of the state'),
        'name': fields.String(description='Name of the state', required=True),
        'country_id': fields.Integer(description='Country ID', required=True)
    }
)

country_model = country_namespace.model(
    'Country', {
        'id': fields.Integer(description='Id of the country'),
        'name': fields.String(description='Name of the country', required=True)
    }
)

@country_namespace.route('/states/')
class CreateGetState(Resource):
    @country_namespace.marshal_with(state_model)
    @jwt_required()
    def get(self):
        """Getting list of states"""
        state = State.query.all()

        return state, HTTPStatus.OK

    @country_namespace.expect(state_model)
    @country_namespace.marshal_with(state_model)
    @jwt_required()
    def post(self):
        """Creating new State"""
        username = get_jwt_identity()
        current_user = User.query.filter_by(username=username).first()

        if current_user is None or current_user.is_admin != 'admin':
            return {"message": "You are not allowed"}, HTTPStatus.FORBIDDEN
        
        data = country_namespace.payload

        new_post = State(
            name = data['name'],
            country_id = data['country_id']
        )

        new_post.save()

        return new_post, HTTPStatus.CREATED


@country_namespace.route('/state/<int:state_id>/')
class DelUpdateState(Resource):

    @country_namespace.marshal_with(state_model)
    @jwt_required()
    def delete(self, state_id):
        """Deleting State"""
        username = get_jwt_identity()

        current_user = User.query.filter_by(username=username).first()

        if current_user is None or current_user.is_admin != 'admin':
            return {"message": "You are not allowed"}, HTTPStatus.FORBIDDEN
        
        state = State.get_by_id(state_id)
        
        state.delete()

        return {"message": "State deleted successfully"}, HTTPStatus.OK
        

@country_namespace.route('/country/')
class CreateGetCountry(Resource):
    @country_namespace.marshal_with(country_model)
    def get(self):
        """Fetching list of country"""
        countrys = Country.query.all()

        return countrys, HTTPStatus.OK

    @country_namespace.expect(country_model)
    @country_namespace.marshal_with(country_model)
    @jwt_required()
    def post(self):
        """Creating a new country"""
        username = get_jwt_identity()
        current_user = User.query.filter_by(username=username).first()

        if current_user is None or current_user.is_admin != 'admin':
            return {"message": "You are not allowed"}, HTTPStatus.FORBIDDEN
        
        data = country_namespace.payload

        new_post = Country(
            name = data['name']
        )

        new_post.save()

        return new_post, HTTPStatus.CREATED
        

@country_namespace.route('/country/<int:country_id>/')
class DelUpdateCountry(Resource):
    @country_namespace.marshal_with(country_model)
    @jwt_required()
    def delete(self, country_id):
        """Deleting a country"""
        username = get_jwt_identity()

        current_user = User.query.filter_by(username=username).first()

        if current_user is None or current_user.is_admin != 'admin':
            return {"message": "You are not allowed"}, HTTPStatus.FORBIDDEN
        
        country = Country.get_by_id(country_id)
        
        country.delete()

        return {"message": "Country deleted successfully"}, HTTPStatus.OK

@country_namespace.route('/country/<int:country_id>/states/')
class GetAllCategory(Resource):
    @country_namespace.marshal_with(country_model)
    @jwt_required()
    def get(self, country_id):
        """Fetching list of a Country with State"""
        country = Country.get_by_id(country_id)

        if country is None:
            return {"message": "Country not found"}, HTTPStatus.NOT_FOUND

        country_info = country.states

        return country_info, HTTPStatus.OK