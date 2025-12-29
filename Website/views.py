"""
Created by Jesse Scully
Date: 15/09/2025
Influenced by: Python Website Full Tutorial by Tech With Tim
Link: https://www.youtube.com/watch?v=dam0GPOAvVI
"""

from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, request
from flask_login import login_required, current_user
from .models import Note, User_details
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/home', methods=['GET', 'POST'])
# Navigate to dashboard if button is pressed
@login_required
def home():
    if request.method == 'POST':
        return redirect(url_for('views.dashboard'))
    return render_template("home.html", boolean = True)

# Establish the dashboard
@views.route('/dashboard')
@login_required
def dashboard():
    # Get details from profile edit page
    player = User_details.query.first()
    return render_template('dashboard.html', player=player)

# Designate a route to go to the performance entry edit page
@views.route('/performance_entry')
@login_required
def pe_route():
    return render_template('performance_entry.html')

# Designate a route to go to the coaching entry edit page
@views.route('/coaching_entry')
@login_required
def ce_route():
    return render_template('coaching_entry.html')

# Designate a route to go back to the dashboard that can be used by multiple pages
@views.route('/c_dashboard', methods=["GET","POST"])
@login_required
def to_dashboard():
    return redirect(url_for('views.dashboard'))

# Designate a route to go to the profile edit page
# Retrieve data
@views.route('/profile_edit')
@login_required
def render_profile_edit():
    return render_template('profile_edit.html')

# Code influenced by: https://www.digitalocean.com/community/tutorials/how-to-use-web-forms-in-a-flask-application?
# Submit profile details, save data and redirect to the dashboard
@views.route('/dashboard/edit', methods=['POST'])
def edit_details():
    if request.method == 'POST':
        player_name = request.form.get('player_name')
        player_description = request.form.get('player_description')

        player = User_details.query.first()

        # Insert a brand new entry for player
        if player is None:
            player = User_details(name=player_name, description=player_description)
            db.session.add(player)
        # If not empty, replace it with the new entry
        else:
            player.name = player_name
            player.description = player_description

        db.session.commit()
        return redirect(url_for('views.dashboard'))
