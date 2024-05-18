from flask import Blueprint, render_template, redirect, url_for, abort
from flask_login import login_required, current_user
from app.models import Chat, Message, Post
from datetime import datetime, timedelta
from sqlalchemy import or_
from app import db

messages = Blueprint('messages', __name__)

@messages.route('/create_chat/<int:author_id>', methods=['GET', 'POST'])
@login_required
def create_chat(author_id):
    # Get the current user's ID
    current_user_id = current_user.id
    
    # Ensure the author exists
    author = Post.query.get_or_404(author_id)

    # Sort the IDs to create a unique chat ID
    user1_id, user2_id = sorted([str(current_user_id), str(author_id)])
    chat_id = f"{user1_id}_{user2_id}"

    # Create an initial message
    initial_message_content = f"I am interested in your post: {author.title}, let's chat"
    initial_message = Message(chat_id=chat_id, user_id=current_user_id, content=initial_message_content, timestamp=datetime.utcnow())
    db.session.add(initial_message)
    db.session.commit()
    
    # Check if the chat already exists, if not, create it
    chat = Chat.query.filter_by(id=chat_id).first()
    if not chat:
        chat = Chat(id=chat_id, user1_id=user1_id, user2_id=user2_id)
        db.session.add(chat)
        db.session.commit()

    # Redirect to the chat page
    return redirect(url_for('messages.chats', chat_id=chat_id))

@messages.route('/chats', methods=['GET', 'POST'])
@login_required
def chats():
    # Retrieve all chats where the current user is a participant
    chats = Chat.query.filter(or_(Chat.user1_id == current_user.id, Chat.user2_id == current_user.id)).all()

    # Prepare a dictionary to store messages for each chat
    chat_messages = {}
    for chat in chats:
        # Retrieve messages associated with the chat
        messages = Message.query.filter_by(chat_id=chat.id).all()
        # Store messages in the dictionary with chat_id as key
        chat_messages[chat.id] = messages
    
    # Pass the current date and time to the template
    current_datetime = datetime.now()
    timedelta_class = timedelta
    current_user_id = current_user.id


    # Render the template with the user's chats and associated messages
    return render_template('message.html', chats=chats, chat_messages=chat_messages, current_datetime=current_datetime, timedelta_class=timedelta_class, current_user_id=current_user_id)

@messages.route('/chat/<chat_id>', methods=['GET'])
@login_required
def chat(chat_id):
    # Retrieve the chat based on the chat ID
    chat = Chat.query.get_or_404(chat_id)
    
    # Check if the current user is one of the participants in the chat
    if current_user.id not in [chat.user1_id, chat.user2_id]:
        abort(403)  # Access forbidden
    else:
        # Fetch messages related to the chat
        messages = Message.query.filter_by(chat_id=chat_id).all()
    
    # Render the chat template with messages
    return render_template('message.html', chat=chat, messages=messages)