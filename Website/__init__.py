"""
Created by Jesse Scully
Date: 15/09/2025
Influenced by: Python Website Full Tutorial by Tech With Tim
Link: https://www.youtube.com/watch?v=dam0GPOAvVI
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
# Help to manage all login related topics
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    # Create a secret key
    app.config['SECRET_KEY'] = 'asdhiu1235'
    # Direct WHERE to create the database
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_NAME}"
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # Import models BEFORE we initialise the database
    from .models import User

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # Tell flask how to load in a User
    @login_manager.user_loader
    def load_user(id):
        # Check primary key for users: their ID
        return User.query.get(int(id))

    return app

# Check if database exists and create one if none exists
def create_database(app):
    if not path.exists(DB_NAME):
        with app.app_context():
            db.create_all()
        print('Created DB!')


