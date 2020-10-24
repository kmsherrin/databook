import secrets
import os
from PIL import Image
from flask_mail import Message
from flask import current_app
from app import mail
import boto3
BUCKET = "databook-profilepicture"

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, file_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + file_ext
    picture_path = os.path.join(current_app.root_path, 'static/images/profile_pictures', picture_fn)

    # Resize the profile picture to a more usable size
    output_size = (130, 130)
    img = Image.open(form_picture)
    img.thumbnail(output_size)
    img.save(picture_path)

    resp = upload_file(picture_path, BUCKET, f'static/images/profile_pictures/{picture_fn}')
    
    os.remove(picture_path)

    return picture_fn


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message(
        subject='Password Reset Request', 
        sender='me@kendall.me',
        recipients=[user.email])
    msg.body = f"To reset your password, visit the following link: {url_for('reset_password', token=token, _external=True)} If you did not make this request simply ignore this email."
    
    mail.send(msg)


def upload_file(file_name, bucket, object_name):
    """
    Function to upload a file to an S3 bucket
    """
    s3_client = boto3.client('s3')
    response = s3_client.upload_file(file_name, bucket, object_name, ExtraArgs={'ACL': 'public-read'})

    return response
