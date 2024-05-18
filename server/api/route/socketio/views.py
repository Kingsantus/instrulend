from flask_restx import Namespace, Resource

message_namespace = Namespace('message', description='Message namespace')

@message_namespace.route('/')
class Message(Resource):
    def get(self):
        """Return all messages"""
        pass

    def post(self):
        """Create a new message"""
        pass

@message_namespace.route('/<int:message_id>')
class Message(Resource):
    def get(self, message_id):
        """Return a message"""
        pass

    def post(self, message_id):
        """create a message"""
        pass
    
    def delete(self, message_id):
        """Delete a message"""
        pass