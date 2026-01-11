"""
Created by Jesse Scully
Date: 15/09/2025
Influenced by: Python Website Full Tutorial by Tech With Tim
Link: https://www.youtube.com/watch?v=dam0GPOAvVI
"""

from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, request
from flask_login import login_required, current_user
from datetime import datetime
from .models import User_details, performance_entries
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
    # Query the entries from the database for only 2025
    all_entries = performance_entries.query.filter(
        performance_entries.time >= datetime(2025, 1, 1),
        performance_entries.time < datetime(2026, 1, 1)
    )
    # Call the calculate win rate function
    win_rate_2025 = calculate_win_rate(all_entries)
    # Call the function for win rates for 2025 chart
    return render_template('dashboard.html', player=player, win_rate_2025=win_rate_2025)

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

# Submit Performance Entries, save data and redirect to dashboard
@views.route('/dashboard/performance_entry', methods=['POST'])
def performance_details():
    player_date = request.form.get('datepicker')
    player_date = datetime.strptime(player_date, '%Y-%m-%d')
    player_wins = int(request.form.get('player_wins', 0))
    player_losses = int(request.form.get('player_losses', 0))
    player_intensity = int(request.form.get('player_intensity', 0))

    # Figure out if the date was inserted in a specific months using if statements
    # For each if statement, add it to the corresponding month and then calculate new monthly win rate

    # Insert as part of the player_performance variable when i write the code in

    # Immediately insert new entries without replacing the original
    player_performance = performance_entries(wins=player_wins, losses=player_losses, intensity=player_intensity, time=player_date)


    db.session.add(player_performance)
    db.session.commit()
    return redirect(url_for('views.dashboard'))

# Create a function that calculates win rates for you
def calculate_win_rate(all_entries):
    wins_by_month = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    games_by_month = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    # How to fill the buckets...
    # Get month from entry date
    # Convert month to array indexd
    # Add session total into that month

    # Calculate the actual 12 winrates
    win_rates = []
    for index in :
        if games_by_month[index] == 0:
            win_rate = 0
        else:
            win_rate = wins_by_month[index] / games_by_month[index]
            win_rates.append(win_rate)
    return win_rates





    # Calculate the win rate for each month
    # Use a for loop



