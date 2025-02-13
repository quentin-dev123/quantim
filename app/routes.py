#------------------------------------------------------
# Define all entry points (Web pages & API endpoints)
#------------------------------------------------------
import os
from flask import jsonify, json, abort, request, render_template, redirect, current_app, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from git import Repo
from flask_bcrypt import Bcrypt 
from . import helpers, create_app, db, swagger
from datetime import datetime
from operator import attrgetter

from .models import Tag, Subject, Reminder, User


app = create_app(os.getenv('FLASK_CONFIG') or 'default')

"""
To-do list :
    - Bcrypt scurity
    - * Relationship between user and reminder --- Done in models.py, need to apply to routes.py
    - * Create add reminder functionnality 
    - * Change approach for frontend to get reminders (need to use fetch)
    - Send email verification 
    - Ask for username and email rather than just email

* Priority/important
"""

#------------------------------------------------------
# HOME SITE
@app.route("/")
@app.route("/index")
@app.route("/home")
def home():
    return render_template("home.html")

#------------------------------------------------------
# WEB
@app.route('/agenda')
@login_required
def agenda():
    reminders = Reminder.query.all()
    return render_template('agenda.html', title="Agenda Personnel", user="test", reminders=reminders)

@app.route('/add_reminder')
@login_required
def add_reminder():
    return render_template("add_reminder.html")
#------------------------------------------------------
# API ~~ CRUD functions
@app.route("/api/reminder/<int:rem_id>")
@login_required
def get_reminder(rem_id): # Read
    """Example endpoint returning a list of colors by palette
    This is using docstrings for specifications.
    ---
    parameters:
      - name: palette
        in: path
        type: string
        enum: ['all', 'rgb', 'cmyk']
        required: true
        default: all
    definitions:
      Palette:
        type: object
        properties:
          palette_name:
            type: array
            items:
              $ref: '#/definitions/Color'
      Color:
        type: string
    responses:
      200:
        description: A list of colors (may be filtered by palette)
        schema:
          $ref: '#/definitions/Palette'
        examples:
          rgb: ['red', 'green', 'blue']
    """
    reminders = Reminder.query.filter_by(reminder_id=rem_id).first()
    if reminders is not None:
        if reminders.user_id == current_user.id:
            return jsonify(reminders.to_json()), 200
        else:
            return jsonify({"message": "Not logged into the account of the reminder"}), 403
    else:
        return jsonify({"message": "Reminder not found"}), 404
    
@app.route("/api/reminder")
@login_required
def get_reminders(): # Read
    """API returning all reminders linked to your account
    ---
    parameters:
      - name: palette
        in: path
        type: string
        enum: ['all', 'rgb', 'cmyk']
        required: true
        default: all
    definitions:
      Palette:
        type: object
        properties:
          palette_name:
            type: array
            items:
              $ref: '#/definitions/Color'
      Color:
        type: string
    responses:
      200:
        description: A list of colors (may be filtered by palette)
        schema:
          $ref: '#/definitions/Palette'
        examples:
          rgb: ['red', 'green', 'blue']
    """
    reminders = Reminder.query.filter_by(user_id=current_user.id).all()
    sorted_rems = sorted(reminders, key=attrgetter('date'))
    return jsonify([r.to_json() for r in sorted_rems]), 200
    
@app.route("/api/reminder", methods=["POST"])
@login_required
def create_reminders(): # Create
    data = json.loads(request.data)
    reminder = Reminder(
        content=data.get("content"), 
        date=datetime.strptime(data.get("date"), "%Y-%m-%d"),
        user=current_user,
        user_id=current_user.id,
        tag_id=data.get("tag_id"),
        subject_id=data.get("subject_id")
    )
    db.session.add(reminder)
    db.session.commit()
    return jsonify({"message": "Reminder created succesfully"}), 200

@app.route("/api/reminder/<int:rem_id>", methods=["DELETE"])
@login_required
def delete_reminders(rem_id): # Delete
    reminder = Reminder.query.filter_by(reminder_id=rem_id).first()
    if reminder:
        if reminder.user_id == current_user.id: # Layer of security
            db.session.delete(reminder)
            db.session.commit()
            return jsonify({"message":"Reminder deleted succesfully"}), 200
        else:
            return jsonify({"message": "Not logged in the right account"}), 403
    else:
        return jsonify({"message": "Reminder not found"}), 404

@app.route("/api/reminder/<int:rem_id>", methods=["PUT"])
@login_required
def update_reminders(rem_id): # Update ~~ Not complete
    data = json.loads(request.data)
    reminder = Reminder(
        content=data.get("content"), 
        date=datetime.strptime(data.get("date"), "%Y-%m-%d"),
        user=current_user,
        user_id=current_user.id,
        tag_id=data.get("tag_id"),
        subject_id=data.get("subject_id")
    )
    db_reminder = Reminder.query.get(rem_id)
    if db_reminder.user_id == current_user.id:
        db_reminder.update(reminder)
        db.session.commit()
        return jsonify({"message": "Reminder updated succesfully"}), 200
    return jsonify({"message": "Not loggedi in the account of the reminder"}), 403


@app.route("/api/subject", methods=["GET", "POST"])
@login_required
def subjects():
    if request.method == "GET":
        subjects = Subject.query.filter_by(user_id=current_user.id).all()
        return jsonify([s.to_json() for s in subjects])
    data = json.loads(request.data)
    if Subject.query.filter_by(content=data.get("content"), user_id=current_user.id).first() is None:
        subject = Subject(
            content=data.get("content"), 
            bg_color=data.get("bg_color"),
            user=current_user,
            user_id=current_user.id
        )
        db.session.add(subject)
        db.session.commit()
        return jsonify(subject.to_json()), 200
    else:
        return jsonify({"message": "Une matière avec le même nom existe déjà"}), 400
        
@app.route("/api/tag", methods=["GET", "POST"]) 
@login_required
def tags():
    if request.method == "GET":
        tags = Tag.query.filter_by(user_id=current_user.id).all()
        return jsonify([t.to_json() for t in tags])
    data = json.loads(request.data)
    if Tag.query.filter_by(content=data.get("content"), user_id=current_user.id).first() is None:
        tag = Tag(
            content=data.get("content"), 
            bg_color=data.get("bg_color"),
            user=current_user,
            user_id=current_user.id
        )
        db.session.add(tag)
        db.session.commit()
        return jsonify(tag.to_json()), 200
    else:
        return jsonify({"message": "Un tag avec le même nom existe déjà"}), 400
    
@app.route("/api/reminder/delete/<int:reminderId>", methods=["POST"])
@login_required
def delete_reminder(reminderId):
    reminder = Reminder.query.filter_by(reminder_id=reminderId).first()
    if reminder:
        if reminder.user_id == current_user.id: # Layer of security
            db.session.delete(reminder)
            db.session.commit()
            return jsonify({"message":"Reminder deleted succesfully"}), 200
        else:
            return jsonify({"message": "Not logged in the right account"}), 403
    else:
        return jsonify({"message": "Reminder not found"}), 404
        
#------------------------------------------------------
# Auto deploy
@app.route('/api/push_version', methods=['POST'])
def git_webhook():
    x_hub_signature = request.headers.get('X-Hub-Signature')
    helpers.verify_signature(request.data, current_app.config['GIT_REPO_SECRET'],x_hub_signature)
    repo = Repo(current_app.config['GIT_REPO_PATH'])
    origin = repo.remotes.origin
    origin.pull(current_app.config['GIT_REPO_BRANCH'])
    return 'Updated PythonAnywhere successfully', 200

#------------------------------------------------------
# User Verification
login_manager = LoginManager()
login_manager.init_app(app)
bcrypt = Bcrypt(app)

@login_manager.user_loader
def loader_user(user_id):
    return User.query.get(user_id)
    
@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        data = json.loads(request.data)
        email = data.get('email')
        if User.query.filter_by(username=email).first() is None:
            if data.get("password1") == data.get("password2"):
                user = User(username=email,
                            password=bcrypt.generate_password_hash(data.get("password1")).decode('utf-8'))
                db.session.add(user)
                db.session.commit()
                return jsonify({"message": "Account created successfully"}), 200 # Error here ~Probably~
            else:
                return jsonify({"message": "Les mots de passe ne correspondent pas."}), 400
        else:
            response = {
                "message": "Un compte existe déjà avec cette adresse email. ",
                "link_href": "/login",
                "link_display":"Se connecter"
            }
            return jsonify(response), 400
    return render_template("register.html")
 
 
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = json.loads(request.data)
        email = data.get('email')
        try:
            user = User.query.filter_by(
                username=email).first()
            if bcrypt.check_password_hash(user.password, data.get('password')):
                login_user(user)
                return jsonify({"message": "Logged in successfully"}), 200
            raise AttributeError
        except AttributeError:
            response = {"message": "L'adresse email ou le mot de passe est incorrect."}
            return jsonify(response), 400
    return render_template("login.html")
 
 
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('login'))
