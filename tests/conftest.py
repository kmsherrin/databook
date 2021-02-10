"""
I have based this off of the Flask docs on setting up a pytest fixture which will serve as the 
testing base app for the suite of tests
"""

import os
import tempfile
import sys
import pytest
#topdir = os.path.join(os.path.dirname(__file__), "..")
#sys.path.append(topdir)
from app.config import TestConfig
from app import create_app
from app import db as _db 
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from sqlalchemy.orm import sessionmaker

from app import create_app, db

@pytest.fixture(scope='session')
def app():
    return create_app(config_class=TestConfig)


@pytest.fixture(scope='session')
def client(app):
    return app.test_client()


@pytest.fixture(scope='session')
def _db(app):
    '''
    Provide the transactional fixtures with access to the database via a Flask-SQLAlchemy
    database connection.
    '''
    db = SQLAlchemy(app=app)
    db.drop_all()
    db.create_all()

    def teardown():
        db.drop_all()

    return db