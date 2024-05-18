from app.models import User

def get_user_image_file(user_id):
    user = User.query.get(user_id)
    if user:
        return user.image_file
    return None 

