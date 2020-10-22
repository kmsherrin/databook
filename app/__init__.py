from app.config import Config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flaskext.markdown import Markdown
from flask_migrate import Migrate
import threading

db = SQLAlchemy()
bcrypt = Bcrypt()

migrate = Migrate()

login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

mail = Mail()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    from app.users.routes import users
    from app.posts.routes import posts
    from app.datasets.routes import datasets
    from app.main.routes import main
    from app.errors.handlers import errors

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(datasets)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    migrate.init_app(app, db)

    Markdown(app, output_format='html5')
    lock = threading.Lock()
    with app.app_context():
        with lock:
            db.create_all()

    return app
