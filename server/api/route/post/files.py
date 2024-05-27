from flask import current_app
from PIL import Image
import os, secrets
import time

def allowed_file(filename):
    """Check the extension against the required files to be up dated"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


def save_picture(file):
    """changes the file name to a random string for easy Identification and reduce the size of the picture"""
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(file.filename)
    # Concatenate random hex with a timestamp
    picture_fn = f"{random_hex}_{int(time.time())}{f_ext}"
    picture_path = os.path.join(current_app.config['UPLOAD_FOLDER_POST'], picture_fn)
    
    # Ensure the upload folder exists
    os.makedirs(current_app.config['UPLOAD_FOLDER_POST'], exist_ok=True)
    
    output_size = (800, 800)
    i = Image.open(file)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn