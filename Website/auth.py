"""
Created by Jesse Scully
Date: 15/09/2025
Influenced by: Python Website Full Tutorial by Tech With Tim
Link: https://www.youtube.com/watch?v=dam0GPOAvVI
"""

from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
# Allow to hash a password
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    # Check if details were sent
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Check if details are valid
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category ='success')
                # Remember user is logged in until web page is refreshed or browsing history is cleared
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, please try again.', category='error')
        else:
            flash('Email does not exist.', category='error')


    return render_template("login.html", user = current_user)

@auth.route('/logout')
# Cannot access function unless user is logged in
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    # Send data if website initiates a POST request
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()

        # Ensure we are not signing up another user with the same email
        if user:
            flash('Email already exists!', category='error')
        # Ensure password criteria is met
        elif len(email) < 4:
            flash('Email must be longer than 3 characters', category='err')
        elif len(first_name) < 2:
            flash('First name must be longer than 1 character', category='err')
        elif password != password2:
            flash('Passwords don\'t match', category='err')
        elif len(password) < 7:
            flash('Password must be greater than 6 characters', category='err')
        else:
            # Create new user with specific parameters
            new_user = User(email=email, 
                            first_name=first_name,
                            # Use hashing, salts and key stretching to encrypt passwords
                            password=generate_password_hash(password, method='pbkdf2:sha256', salt_length=16))
            # Add new user to database
            db.session.add(new_user)
            db.session.commit()
            flash('Account created!', category='success')
            # Redirect back to home page once account is created
            return redirect(url_for('views.home'))


    return render_template("sign_up.html", user=current_user)

