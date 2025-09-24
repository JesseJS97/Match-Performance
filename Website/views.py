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

@views.route('/dashboard')
@login_required
def dashboard():
    return render_template("dashboard.html")