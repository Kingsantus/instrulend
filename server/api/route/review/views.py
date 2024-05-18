from flask_restx import Namespace, Resource

review_namespace = Namespace('review', description='Review namespace')

@review_namespace.route('/expirence')
class Expirence(Resource):
    def get(self):
        """Get the list of expirence"""
        pass

    def post(self):
        """Create a new expirence"""
        pass

@review_namespace.route('/review')
class ReviewList(Resource):
    def get(self):
        """Get a list of all the review"""
        pass

    def post(self):
        """Create a new review"""
        pass

@review_namespace.route('/review/<int:review_id>')
class Review(Resource):
    def get(self, review_id):
        """Get a specific review"""
        pass

    def post(self, review_id):
        """Update a specific review"""
        pass
    
    def delete(self, review_id):
        """Delete a specific review"""
        pass

