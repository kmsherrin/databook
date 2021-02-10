"""

Set up the configuration settings for the flask app, this class is passed into the Flask app constructor as the config_class

"""

import os

class TestConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    print(os.environ.get('CI'))
    if os.environ.get('CI') == True:
        SQLALCHEMY_DATABASE_URI = os.environ.get('INPUT_TEST_SQLALCHEMY_DATABASE_URI')
    else:
        SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_SQLALCHEMY_DATABASE_URI')

    SQLALCHEMY_TRACK_MODIFICATIONS = False


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
