"""
Created by Jesse Scully
Date: 17/09/2025
Influenced by: Python Website Full Tutorial by Tech With Tim
Link: https://www.youtube.com/watch?v=dam0GPOAvVI
"""

from . import db
# Give user object some things for our flask login
from flask_login import UserMixin
from sqlalchemy.sql import func

# Setup Note model to conform to the below format
class Note(db.Model):
    # System will ensure ids are unique automatically
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    # Using func module will ensure default time will be the present
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    # Assign a foreign key for a one to many relationship - one User to many different Notes
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

# Setup User model to conform to the below format
class User(db.Model, UserMixin):
    # Define a schema for some objects that need to be stored in our database
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')
