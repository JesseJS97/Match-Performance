"""
Created by Jesse Scully
Date: 15/09/2025
Influenced by: Python Website Full Tutorial by Tech With Tim
Link: https://www.youtube.com/watch?v=dam0GPOAvVI
"""

from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Note
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

@views.route('/delete-note', methods=['POST'])
# Define a function to delete a note
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    # Ensure signed in user owns note can only delete the note
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

# Designate a route to go to the dashboard page
@views.route('/dashboard',methods=["GET","POST"])
@login_required
def dashboard():
    if request.method == 'POST':
        return redirect(url_for('dashboard_edit.html'))
    return render_template("dashboard.html")

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
@views.route('/profile_edit', methods=["GET","POST"])
@login_required
def render_profile_edit():
    return render_template('profile_edit.html')