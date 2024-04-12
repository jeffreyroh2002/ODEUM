from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect  # Import CSRFProtect
from api.config import Config
import os
from flask_cors import CORS

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "users.login"
login_manager.login_message_category = "info"
mail = Mail()

# Initialize CSRFProtect
csrf = CSRFProtect()

def create_app(config_class=Config):
    app = Flask(__name__, static_folder='static')
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    CORS(app)
    
    # Initialize CSRFProtect with the Flask app instance
    csrf.init_app(app)

    # section for importing blueprints
    from api.main.routes import main
    from api.users.routes import users
    from api.tests.routes import tests
    from api.questions.routes import questions
    from api.results.routes import results
    from api.spotify.routes import spotify
    
    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(tests)
    app.register_blueprint(questions)
    app.register_blueprint(results)
    app.register_blueprint(spotify)

    return app