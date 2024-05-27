from flask_restx import Namespace, Resource, fields
from ...models.messages import Chat, Message
from ...models.users import User
from http import HTTPStatus
from flask_jwt_extended import jwt_required, get_jwt_identity


message_namespace = Namespace('message', description='Message namespace')

chat_model = message_namespace.model(
    'Chat',{
        'id': fields.String(description='ID of chat'),
        'user1_id':fields.Integer(description='User ID', required=True), 
        'user2_id': fields.Integer(description='Chat ID', required=True)
    }
)

message_model = message_namespace.model(
    'Message',{
        'id': fields.Integer(description='ID of message'),
        'content': fields.String(description='A Content', required=True),
        'chat_id': fields.String(description='A chat ID', required=True),
        'user_id': fields.Integer(description='the user ID', required=True)
    }
)

@message_namespace.route('/chats')
class GetChat(Resource):
    @message_namespace.marshal_with(chat_model)
    def get(self):
        """Return all messages"""
        chats = Chat.query.all()

        return chats, HTTPStatus.OK
    
@message_namespace.route('/chat/<int:user_id>')
class CreateChat(Resource):

    @message_namespace.expect(chat_model)
    @message_namespace.marshal_with(chat_model)
    @jwt_required()
    def post(self, user_id):
        """Create a new message"""
        username = get_jwt_identity()
        user = User.query.filter_by(username=username).first()
        if not user:
            return {"message": "User not found"}, HTTPStatus.UNAUTHORIZED
        user2 = User.query.filter_by(id=user_id).first()
        if not user2:
            return {"message": "User not found"}, HTTPStatus.UNAUTHORIZED
        
        if user.id == user2.id:
            return {"message": "You cannot chat with yourself"}, HTTPStatus.BAD_REQUEST
        
        
        user1_id, user2_id = sorted([str(user.id), str(user2.id)])
        
        chat_id = f"{user1_id}_{user2_id}"
        existing_chat = Chat.query.filter_by(id=chat_id).first()
        if existing_chat:
            return {"message": "Chat already exists", "chat_id": chat_id}, HTTPStatus.CONFLICT
        
        chat = Chat(
            id=chat_id,
            user1_id=user1_id,
            user2_id=user2_id
        )

        chat.save()

        return chat, HTTPStatus.CREATED
    
@message_namespace.route('/chat/<string:chat_id>')
class GetDeleteChat(Resource):

    @message_namespace.marshal_with(chat_model)
    @jwt_required()
    def get(self, chat_id):
        """Return a particular chat"""
        username = get_jwt_identity()

        user = User.query.filter_by(username=username).first()

        if not user:
            return {"message": "User not found"}, HTTPStatus.UNAUTHORIZED
        
        chat = Chat.query.get_or_404(chat_id)

        return chat, HTTPStatus.OK

    @message_namespace.marshal_with(chat_model)
    @jwt_required()    
    def delete(self, chat_id):
        """Delete Chat"""
        username = get_jwt_identity()

        user = User.query.filter_by(username=username).first()

        if not user:
            return {"message": "User not found"}, HTTPStatus.UNAUTHORIZED
        
        chat = Chat.query.get_or_404(chat_id)

        user_ids = chat_id.split("_")
        if str(user.id) not in user_ids:
            return {"message": "You are not authorized to delete this chat"}, HTTPStatus.FORBIDDEN
        
        chat.delete()

        return {"message": "Chat successfully deleted"}, HTTPStatus.OK
    
@message_namespace.route('/user/<int:user_id>/chats')
class GetUserChats(Resource):
    @message_namespace.marshal_with(message_model)
    @jwt_required()
    def get(self, user_id):
        """Return all the chat a user engage"""
        username = get_jwt_identity()
        user = User.query.filter_by(username=username).first()
        if not user:
            return {"message": "User not found"}, HTTPStatus.UNAUTHORIZED
        
        chats = Chat.query.filter((Chat.user1_id == user_id)|(Chat.user2_id == user_id)).all()

        if not chats:
            return {"message": "No chats found"}, HTTPStatus.NOT_FOUND
        
        return chats, HTTPStatus.OK

@message_namespace.route('/create/<string:chat_id>')
class CreateMessage(Resource):
    @message_namespace.expect(message_model)
    @message_namespace.marshal_with(message_model)
    @jwt_required()
    def post(self, chat_id):
        """create a message"""
        username = get_jwt_identity()
        user = User.query.filter_by(username=username).first()

        if not user:
            return {"message": "User not found"}, HTTPStatus.UNAUTHORIZED
        
        chat = Chat.query.get_or_404(chat_id)

        data = message_namespace.payload
        
        message = Message(
            content=data['content'],
            chat_id=chat_id,
            user_id=user.id
        )

        message.save()

        from ....app import socketio

        socketio.emit('new_message', data, broadcast=True)

        return message, HTTPStatus.CREATED


@message_namespace.route('/chats/<string:chat_id>/user/<int:user_id>')
class GetMessageForAChat(Resource):
    @message_namespace.marshal_with(message_model)
    @jwt_required()
    def get(self, chat_id, user_id):
        """Get messages of a user from a particular chat id"""
        username = get_jwt_identity()
        user = User.query.filter_by(username=username).first()
        if not user:
            return {"message": "User not found"}, HTTPStatus.UNAUTHORIZED
        
        chat = Message.query.filter_by(chat_id=chat_id).first()
        if not chat:
            return {"message": "Chat not found"}, HTTPStatus.NOT_FOUND
        user = Message.query.filter_by(user_id=user_id).first()
        if not user:
            return {"message": "User not found"}, HTTPStatus.NOT_FOUND

        messages = Message.query.filter_by(chat_id=chat_id).filter_by(user_id=user_id).all()


        if not messages:
            return {"message": "No messages found"}, HTTPStatus.NOT_FOUND
        
        return messages, HTTPStatus.OK
    
@message_namespace.route('/chats/messages/<string:chat_id>')
class GetChatMessage(Resource):
    @message_namespace.marshal_with(message_model)
    @jwt_required()
    def get(self, chat_id):
        """Get Messages in a Chat"""
        username = get_jwt_identity()
        user = User.query.filter_by(username=username).first()
        if not user:
            return {"message": "User not found"}, HTTPStatus.UNAUTHORIZED
        
        chat = Message.query.filter_by(chat_id=chat_id).first()
        if not chat:
            return {"message": "Chat not found"}, HTTPStatus.NOT_FOUND
        
        messages = Message.query.filter_by(chat_id=chat_id).order_by(Message.date_created.desc()).all()

        if not messages:
            return {"message": "No messages found"}, HTTPStatus.NOT_FOUND
        
        return messages, HTTPStatus.OK
    
@message_namespace.route('/chats/<string:chat_id>/personal')
class GetPersonalMessage(Resource):
    @message_namespace.marshal_with(message_model)
    @jwt_required()
    def get(self, chat_id):
        """Get Messages in a Chat"""
        username = get_jwt_identity()
        user = User.query.filter_by(username=username).first()
        if not user:
            return {"message": "User not found"}, HTTPStatus.UNAUTHORIZED
        
        chat = Message.query.filter_by(chat_id=chat_id).first()
        if not chat:
            return {"message": "Chat not found"}, HTTPStatus.NOT_FOUND
        
        messages = Message.query.filter_by(chat_id=chat_id).filter_by(user_id=user.id).order_by(Message.date_created.desc()).all()
        if not messages:
            return {"message": "No messages found"}, HTTPStatus.NOT_FOUND
        
        return messages, HTTPStatus.OK
    
@message_namespace.route('/chats/<string:chat_id>/messages/<int:message_id>')
class GetUpdateDeleteMessage(Resource):
    @message_namespace.marshal_with(message_model)
    @jwt_required()
    def get(self, chat_id, message_id):
        """Get Messages in a Chat"""
        username = get_jwt_identity()
        user = User.query.filter_by(username=username).first()
        if not user:
            return {"message": "User not found"}, HTTPStatus.UNAUTHORIZED
        
        chat = Message.query.filter_by(chat_id=chat_id).first()
        if not chat:
            return {"message": "Chat not found"}, HTTPStatus.NOT_FOUND
        
        message = Message.query.filter_by(chat_id=chat_id).filter_by(id=message_id).first()
        if not message:
            return {"message": "Message not found"}, HTTPStatus.NOT_FOUND
        
        return message, HTTPStatus.OK
    
    @message_namespace.marshal_with(message_model)
    @jwt_required()
    def put(self, chat_id, message_id):
        """Update message of a user"""
        username = get_jwt_identity()
        user = User.query.filter_by(username=username).first()
        if not user:
            return {"message": "User not found"}, HTTPStatus.UNAUTHORIZED
        
        
        chat = Message.query.filter_by(chat_id=chat_id).first()
        if not chat:
            return {"message": "Chat not found"}, HTTPStatus.NOT_FOUND
        
        if user.id != chat.user_id:
            return {"message": "You are not authorized to update this message"}, HTTPStatus.FORBIDDEN
        
        message = Message.query.filter_by(chat_id=chat_id).filter_by(id=message_id).first()
        if not message:
            return {"message": "Message not found"}, HTTPStatus.NOT_FOUND
        
        data = message_namespace.payload
        
        message.content = data['content']

        message.update()

        from ....app import socketio
        socketio.emit('new_message', data, broadcast=True)

        return message, HTTPStatus.OK
    
    @message_namespace.marshal_with(message_model)
    @jwt_required()
    def delete(self, chat_id, message_id):
        """Update message of a user"""
        username = get_jwt_identity()
        user = User.query.filter_by(username=username).first()
        if not user:
            return {"message": "User not found"}, HTTPStatus.UNAUTHORIZED
        
        
        chat = Message.query.filter_by(chat_id=chat_id).first()
        if not chat:
            return {"message": "Chat not found"}, HTTPStatus.NOT_FOUND
        
        if user.id != chat.user_id:
            return {"message": "You are not authorized to delete this message"}, HTTPStatus.FORBIDDEN
        
        message = Message.query.filter_by(chat_id=chat_id).filter_by(id=message_id).first()
        if not message:
            return {"message": "Message not found"}, HTTPStatus.NOT_FOUND
        
        message.delete()

        return {"message":"Successfully deleted"}, HTTPStatus.OK