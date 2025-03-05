#------------------------------------------------------
# Define all entry points (Web pages & API endpoints)
#------------------------------------------------------
import os, pronotepy
from flask import jsonify, json, abort, request, render_template, redirect, current_app, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from git import Repo
from flask_bcrypt import Bcrypt 
from . import helpers, create_app, db, swagger
from datetime import datetime, date
from operator import attrgetter
from types import NoneType

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
def get_reminder(rem_id): # Read one
    """Endpoint to read a reminder
    ---
    tags:
      - Reminder CRUD operations
    description: Endpoint returning reminder with a specified id (must be logged in)
    parameters:
      - name: rem_id
        in: path
        type: integer
        required: true
    definitions:
      Reminder:
        type: object
        properties:
          id:
            type: integer
            example: 1478
          user_id: 
            type: integer
            example: 3927
          tag_id: 
            type: integer
            example: 8370
          subject_id: 
            type: integer
            example: 9239
          date: 
            type: string
            example: 2026-12-31T00:00:00
          content: 
            type: string
            example: Create an account on quantix.pythonanywhere.com
    responses:
      200:
        description: A reminder object
        schema:
          $ref: '#/definitions/Reminder'
        examples:
          application/json: {
            "content": "An example content of a reminder",
            "date": "2027-02-24T00:00:00",
            "id": 54,
            "subject_id": 36,
            "tag_id": 29,
            "user_id": 167
          }
      403:
        description: The reminder with the specified id belongs to someone else
        schema:
          type: string
          example: Not logged into the account of the reminder
      404:
        description: The reminder with the specified id was not found
        schema:
          type: string
          example: Reminder not found
      500:
        description: An error ocurred internally. This isn't planned and can have many causes
    """
    reminders = Reminder.query.filter_by(reminder_id=rem_id).first()
    if reminders is not None:
        if reminders.user_id == current_user.id:
            return jsonify(reminders.to_json()), 200
        else:
            return "Not logged into the account of the reminder", 403
    else:
        return "Reminder not found", 404
    
@app.route("/api/reminder")
@login_required
def get_reminders(): # Read all
    """Endpoint to read reminders
    ---
    tags:
      - Reminder CRUD operations
    description: Endpoint returning all reminders linked to your account (must be logged in)
    responses:
      200:
        description: A list of all reminders sorted chronologically by date property
        schema:
        type: array
        items:
          $ref: '#/definitions/Reminder'
        examples:
          application/json: [{
            "content": "An example content of a reminder",
            "date": "2027-02-24T00:00:00",
            "id": 54,
            "subject_id": 36,
            "tag_id": 29,
            "user_id": 167
          },
          {
            "content": "An other example content of a reminder",
            "date": "2028-02-24T00:00:00",
            "id": 55,
            "subject_id": 78,
            "tag_id": 5,
            "user_id": 167
          }]
      500:
        description: An error ocurred internally. This isn't planned and can have many causes
    """
    if current_user.pronote_username is not None:
        client = pronotepy.Client(
                'https://pronote.fis.edu.hk/eleve.html',
                username=current_user.pronote_username,
                password=current_user.pronote_password,
            )
        homeworks = client.homework(date_from=date.today())
        def adjust_color_brightness(color, percent):
            num = int(color[1:], 16)
            amt = round(2.55 * percent)
            r = (num >> 16) + amt
            g = ((num >> 8) & 0x00FF) + amt
            b = (num & 0x0000FF) + amt
        
            # Clamp the values to the range [0, 255]
            r = max(0, min(255, r))
            g = max(0, min(255, g))
            b = max(0, min(255, b))
        
            # Format the result as a hexadecimal color
            return f"#{(r << 16 | g << 8 | b):06x}"
        for homework in homeworks:
            reminder = Reminder.query.filter_by(
                content=homework.description, 
                #date=homework.date,
                user_id=current_user.id,
                tag_id=current_user.pronote_tag_id
            ).first()
            if reminder is None:
                subject = Subject.query.filter_by(content=homework.subject.name, user_id=current_user.id).first()
                if subject is None:
                    bgColor = adjust_color_brightness(homework.background_color, -35)
                    subject = Subject(
                        content=homework.subject.name, 
                        bg_color=bgColor,
                        user=current_user,
                        user_id=current_user.id
                    )
                    db.session.add(subject)
                    db.session.commit()
                tag =  Tag.query.filter_by(id=current_user.pronote_tag_id).first()
                reminder = Reminder(
                    content=homework.description, 
                    date=homework.date,
                    user=current_user,
                    user_id=current_user.id,
                    tag_id=current_user.pronote_tag_id,
                    subject_id=subject.id
                )
                db.session.add(reminder)
                db.session.commit()
    reminders = Reminder.query.filter_by(user_id=current_user.id).all()
    sorted_rems = sorted(reminders, key=attrgetter('date'))
    return jsonify([r.to_json() for r in sorted_rems]), 200
    
@app.route("/api/reminder", methods=["POST"])
@login_required
def create_reminders(): # Create
    """Endpoint to create reminders
    ---
    tags:
      - Reminder CRUD operations
    description: Endpoint to create new reminders linked to your account (must be logged in)
    parameters:
      - name: body
        in: body
        required: True
        schema:
          type: object
          properties:
            content:
              type: string
              example: Have a good day :)
            date:
              type: string
              example: 2027-01-01T00:00:00
            subject_id:
              type: integer
              example: 8888
            tag_id:
              type: integer
              example: 1234
    responses:
      200:
        description: Returns the newly created reminder
        schema:
          $ref: '#/definitions/Reminder'
        examples:
          application/json: {
            "content": "Don't forget to smile :)",
            "date": "2025-05-25T00:00:00",
            "id": 1234,
            "subject_id": 5678,
            "tag_id": 8765,
            "user_id": 4321
          }
      404:
        description: Meaning one of the params of the request was not found in the database 
        schema:
          type: object
          properties:
            message:
              type: string
              example: Tag requested not found
      403:
        description: Meaning one of the params of the request was found but doesnt belong to your account
        schema:
          type: object
          properties:
            message:
              type: string
              example: Tag requested not linked to your account
      500:
        description: An error ocurred internally. This isn't planned and can have many causes. Most of the _*time*_ related to format of the date property of the body parameter. Should be YYYY-MM-DD.
    """
    data = json.loads(request.data)
    tag_id=data.get("tag_id")
    subject_id=data.get("subject_id")
    tag=Tag.query.get(tag_id)
    subject=Subject.query.get(subject_id)
    if tag:
        if subject:
            if tag.user_id == current_user.id:
                if subject.user_id == current_user.id:
                    reminder = Reminder(
                        content=data.get("content"), 
                        date=datetime.strptime(data.get("date"), "%Y-%m-%d"),
                        user=current_user,
                        user_id=current_user.id,
                        tag_id=tag_id,
                        subject_id=subject_id
                    )
                    db.session.add(reminder)
                    db.session.commit()
                    return jsonify(reminder.to_json()), 200
                return jsonify({"message": "Subject requested not linked to your account"}), 403
            return jsonify({"message": "Tag requested not linked to your account"}), 403
        return jsonify({"message": "Subject requested not found"}), 404
    return jsonify({"message": "Tag requested not found"}), 404
        

@app.route("/api/reminder/<int:rem_id>", methods=["DELETE"])
@login_required
def delete_reminders(rem_id): # Delete
    """Endpoint to delete a reminder
    ---
    tags:
      - Reminder CRUD operations
    description: Endpoint to delete a reminder with a specified id (must be logged in)
    parameters:
      - name: rem_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: A validation message
        schema:
          type: string
          example: Reminder deleted succesfully
      403:
        description: The reminder you're trying to delete doesn't belong to you
        schema:
          type: string
          example: Not logged into the account of the reminder
      404:
        description: The reminder with the specified id was not found
        schema:
          type: string
          example: Reminder not found
      500:
        description: An error ocurred internally. This isn't planned and can have many causes
    """
    reminder = Reminder.query.filter_by(reminder_id=rem_id).first()
    if reminder:
        if reminder.user_id == current_user.id: # Layer of security
            db.session.delete(reminder)
            db.session.commit()
            return "Reminder deleted succesfully", 200
        else:
            return "Not logged in the right account", 403
    else:
        return "Reminder not found", 404

@app.route("/api/reminder/<int:rem_id>", methods=["PUT"])
@login_required
def update_reminders(rem_id): # Update
    """Endpoint to update a reminder
    ---
    tags:
      - Reminder CRUD operations
    description: Endpoint to update a reminder with a specified id (must be logged in)
    parameters:
      - name: rem_id
        in: path
        type: integer
        required: true
      - name: body
        in: body
        required: True
        schema:
          type: object
          properties:
            content:
              type: string
              example: Don't worry, be happy
            date:
              type: string
              example: 2027-01-01
            subject_id:
              type: integer
              example: 4321
            tag_id:
              type: integer
              example: 1234
    responses:
      200:
        description: A validation message
        schema:
          type: string
          example: Reminder updated succesfully
      403:
        description: The reminder you're trying to update doesn't belong to you
        schema:
          type: string
          example: Not logged into the account of the reminder
      404:
        description: The reminder with the specified id was not found
        schema:
          type: string
          example: Reminder not found
      500:
        description: An error ocurred internally. This isn't planned and can have many causes. Most of the _*time*_ related to format of the date property of the body parameter. Should be YYYY-MM-DD.
    """
    data = json.loads(request.data)
    db_reminder = Reminder.query.get(rem_id)
    if db_reminder:
        if db_reminder.user_id == current_user.id:
            db_reminder.content = data.get("content")
            db_reminder.date = datetime.strptime(data.get("date"), "%Y-%m-%d")
            db_reminder.user = current_user
            db_reminder.user_id = current_user.id
            db_reminder.tag_id = data.get("tag_id")
            db_reminder.subject_id = data.get("subject_id")
            db.session.commit()
            return "Reminder updated succesfully", 200
        return "Not logged in the account of the reminder", 403
    return "Reminder not found", 404


@app.route("/api/subject")
@login_required
def get_subjects(): # Read all
    subjects = Subject.query.filter_by(user_id=current_user.id).all()
    return jsonify([s.to_json() for s in subjects])

@app.route("/api/subject/<int:subject_id>")
@login_required
def get_subject(subject_id): # Read one
    """Endpoint to read a subject
    ---
    tags:
      - Subject CRUD operations
    description: Endpoint returning a subject with a specified id (must be logged in)
    parameters:
      - name: rem_id
        in: path
        type: integer
        required: true
    definitions:
      Subject:
        type: object
        properties:
          id:
            type: integer
            example: 1234
          content: 
            type: string
            example: a good subject
          bg_color: 
            type: string
            example: #ff0000
          user_id: 
            type: integer
            example: 4321
    responses:
      200:
        description: A subject object
        schema:
          $ref: '#/definitions/Subject'
        examples:
          application/json: {
            "id": 54,
            "content": "Coding",
            "bg_color": "#ff0000",
            "user_id": 167
          }
      403:
        description: The subject with the specified id belongs to someone else
        schema:
          type: string
          example: Not logged into the account of the subject
      404:
        description: The subject with the specified id was not found
        schema:
          type: string
          example: Subject not found
      500:
        description: An error ocurred internally. This isn't planned and can have many causes
    """
    subject = Subject.query.get(subject_id)
    if subject:
        if subject.user_id == current_user.id:
            return jsonify(subject.to_json()), 200
        return "Not logged in the account of the subject", 403
    return "Subject not found", 404

@app.route("/api/subject", methods=["POST"])
@login_required
def create_subjects(): # Create 
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
        return "Une matière avec le même nom existe déjà", 400
        
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

@app.route("/login_pronote")
@login_required
def get_login_pronote():
    return render_template("login_pronote.html")

@app.route("/login_pronote", methods=["POST"])
@login_required
def login_pronote():
    """Endpoint to add your PRONOTE credentials
    ---
    tags:
      - User Verification
    description: Endpoint to link your PRONOTE account to get reminders from PRONOTE homeworks. This can also be used to update your credentials. (This function is currently only available for students of FIS Hong Kong)
    parameters:
      - name: body
        in: body
        required: True
        schema:
          type: object
          properties:
            username:
              type: string
              example: AmbitiousDevelopper5498
            password:
              type: string
              example: MySecretPassword
    responses:
      200:
        description: A validation message
        schema:
          type: string
          example: Succesfully logged into PRONOTE
      400:
        description: The credentials you provided are incorrect. Throws an error message (in french)
        schema:
          type: object
          properties:
            message:
              type: string
              example: Le mot de passe ou l'identifiant est incorrect
      500:
        description: An error ocurred internally. This isn't planned and can have many causes.
    """
    if request.data:
        data = json.loads(request.data)
        try:
            client = pronotepy.Client(
                'https://pronote.fis.edu.hk/eleve.html',
                username=data.get('username'),
                password=data.get('password'),
            )
            tag = Tag(
                content="de PRONOTE", 
                bg_color="#009853",
                user=current_user,
                user_id=current_user.id
            )
            db.session.add(tag)
            db.session.commit()
            current_user.pronote_username = client.username
            current_user.pronote_password = client.password
            current_user.pronote_tag_id = tag.id
            db.session.commit()
            return "Succesfully logged into PRONOTE", 200
        except pronotepy.CryptoError:
            return jsonify({"message": "Le mot de passe ou l'identifiant est incorrect"}), 400  # the client has failed to log in
