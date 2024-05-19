from flask_restx import Namespace, Resource, fields
from ...models.review import Review, Experience
from ...models.users import User
from ...models.post import Post
from flask_jwt_extended import jwt_required, get_jwt_identity
from http import HTTPStatus

review_namespace = Namespace('review', description='Review namespace')

review_model = review_namespace.model(
    'Review',{
        'id': fields.Integer(description='ID'),
        'content': fields.String(description='A Content', required=True),
        'star_rating': fields.Integer(description='Rating', required=True),
        'user_id':fields.Integer(description='User ID', required=True), 
        'author_id': fields.Integer(description='Author ID', required=True)
    }
)

exp_model = review_namespace.model(
    'Experience',{
        'id': fields.Integer(description='ID'),
        'content': fields.String(description='A Content', required=True),
        'star_rating': fields.Integer(description='Rating', required=True),
        'user_id':fields.Integer(description='User ID', required=True),
    }
)

@review_namespace.route('/experience')
class CreateGEtExperience(Resource):

    @review_namespace.marshal_with(exp_model)
    @jwt_required()
    def get(self):
        """Get the list of experience"""
        experiences = Experience.query.all()

        return experiences, HTTPStatus.OK

    @review_namespace.expect(exp_model)
    @review_namespace.marshal_with(exp_model)
    @jwt_required()
    def post(self):
        """Create a new experience"""
        username = get_jwt_identity()
        user = User.query.filter_by(username=username).first()

        if not user:
            return {'Message':"User not found"}, HTTPStatus.NOT_FOUND
        
        data = review_namespace.payload

        # Validate star_rating
        star_rating = data.get('star_rating')
        if star_rating is None or not (1 <= star_rating <= 5):
            return {'Message': "Star rating must be between 1 and 5."}, HTTPStatus.BAD_REQUEST

        new_post = Experience(
            content=data['content'],
            star_rating=star_rating,
            user_id=user.id
        )

        new_post.save()

        return new_post, HTTPStatus.CREATED

@review_namespace.route('/experience/subpar')
class BadExperience(Resource):
    @review_namespace.marshal_with(exp_model)
    @jwt_required()
    def get(self):
        """Get the list of experiences with star rating less than 4"""
        experiences = Experience.query.filter(Experience.star_rating < 4).all()

        return experiences, HTTPStatus.OK
    
@review_namespace.route('/experience/par')
class GoodExperience(Resource):
    @review_namespace.marshal_with(exp_model)
    @jwt_required()
    def get(self):
        """Get the list of experiences with star rating greater than 4"""
        experiences = Experience.query.filter(Experience.star_rating > 4).all()

        return experiences, HTTPStatus.OK

@review_namespace.route('/review')
class GetReviewList(Resource):
    @review_namespace.marshal_with(review_model)
    @jwt_required()
    def get(self):
        """Get a list of all the review"""
        reviews = Review.query.all()

        return reviews, HTTPStatus.OK
    
@review_namespace.route('/user/<int:author_id>')
class CreateReview(Resource):

    @review_namespace.expect(review_model)
    @review_namespace.marshal_with(review_model)
    @jwt_required()
    def post(self, author_id):
        """Create a new review"""
        username = get_jwt_identity()
        user = User.query.filter_by(username=username).first()
        
        if not user:
            return {'Message': "User not found"}, HTTPStatus.NOT_FOUND
        
        author = User.query.get_or_404(author_id)
        
        
        data = review_namespace.payload
        
        # Validate star_rating
        star_rating = data.get('star_rating')
        if star_rating is None or not (1 <= star_rating <= 5):
            return {'Message': "Star rating must be between 1 and 5."}, HTTPStatus.BAD_REQUEST

        # Ensure the user is not reviewing their own post
        if author.id == user.id:
            return {'Message': "You cannot review your own post"}, HTTPStatus.FORBIDDEN
        
        new_review = Review(
            content=data['content'],
            star_rating=star_rating,
            user_id=user.id,
            author_id=author.id
        )

        new_review.save()

        return new_review, HTTPStatus.CREATED
    
@review_namespace.route('/user/reviews/<int:review_id>')
class GetUserReview(Resource):
    @review_namespace.marshal_with(review_model)
    @jwt_required()
    def get(self, review_id):
        """Get Reviews of a particular User"""
        reviews = Review.query.filter_by(author_id=review_id).all()

        if not reviews:
            return {'message': 'No reviews found for this user'}, HTTPStatus.NOT_FOUND

        return reviews, HTTPStatus.OK

@review_namespace.route('/review/<int:review_id>')
class GetOneReview(Resource):

    @review_namespace.marshal_with(review_model)
    @jwt_required()
    def get(self, review_id):
        """Get a specific review"""
        reviews = Review.query.filter_by(id=review_id).all()

        if not reviews:
            return {'message': 'No reviews found for this user'}, HTTPStatus.NOT_FOUND

        return reviews, HTTPStatus.OK
    @review_namespace.expect(review_model)
    @review_namespace.marshal_with(review_model)
    @jwt_required()
    def put(self, review_id):
        """Update a specific review"""
        username = get_jwt_identity()

        user = User.query.filter_by(username=username).first()

        if not user:
            return {"message":"You are not permitted to do this"}, HTTPStatus.BAD_REQUEST
        
        review = Review.query.filter_by(id=review_id).first()

        if not review:
            return {"message":"review not found"}, HTTPStatus.NOT_FOUND
        
        if review.user_id != user.id:
            return {"message":"You are not permitted"}, HTTPStatus.FORBIDDEN
        
        data = review_namespace.payload

        star_rating = data.get('star_rating')
        if star_rating is None or not (1 <= star_rating <= 5):
            return {'Message': "Star rating must be between 1 and 5."}, HTTPStatus.BAD_REQUEST

        
        review.content = data['content']
        review.star_rating = star_rating

        review.update()

        return review, HTTPStatus.OK
    
    @review_namespace.marshal_with(review_model)
    @jwt_required()
    def delete(self, review_id):
        """Delete a specific review"""
        username = get_jwt_identity()

        user = User.query.filter_by(username=username).first()

        if not user:
            return {"message":"You are not permitted to do this"}, HTTPStatus.BAD_REQUEST
        
        review = Review.query.filter_by(id=review_id).first()

        if not review:
            return {"message":"review not found"}, HTTPStatus.NOT_FOUND
        
        if review.user_id != user.id:
            return {"message":"You are not permitted"}, HTTPStatus.FORBIDDEN

        review.delete()

        return {"Message":"Successfully Deleted!"}, HTTPStatus.OK

