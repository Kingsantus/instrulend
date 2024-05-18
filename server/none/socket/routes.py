from flask_socketio import emit
from app import socketio, db
from flask_login import current_user
from datetime import datetime
from .utils import get_user_image_file
from app.models import Message

# SocketIO event handler for new messages
@socketio.on('send_message')
def handle_message(data):
    content = data['content']
    chat_id = data['chat_id']
    user_id = current_user.id
    timestamp = datetime.utcnow()
    user_image_file = get_user_image_file(user_id)
    timestamp_str = timestamp.strftime('%H:%M')

    # Save the message to the database
    message = Message(content=content, chat_id=chat_id, user_id=user_id, timestamp=timestamp)
    db.session.add(message)
    db.session.commit()
    # Emit a 'receive_message' event to all clients
    emit('receive_message', {'content': content, 'chat_id': chat_id, 'user_image_file': user_image_file, 'timestamp': timestamp_str}, broadcast=True)