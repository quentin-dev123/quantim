#------------------------------------------------------
# Define all entry points (Web pages & API endpoints)
#------------------------------------------------------
import os, pronotepy, random, click
import datetime as d
from flask import jsonify, json, abort, request, render_template, redirect, current_app, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from git import Repo
from flask_bcrypt import Bcrypt 
from . import helpers, create_app, db, swagger
from datetime import datetime, timedelta
from operator import attrgetter
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from sqlalchemy import func
from uuid import uuid4

from .models import Tag, Subject, Reminder, Pronote_homework, User, Otp, Pat, Token


app = create_app(os.getenv('FLASK_CONFIG') or 'default')

"""
To-do list :
    - Send emails when reminders are due soon
    - Finish swagger
    - Make tag and subject editable
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
    return render_template('agenda.html', title="Agenda Personnel")

@app.route('/debug')
def debug():
    return render_template("debug.html")

@app.route('/add_reminder')
@login_required
def add_reminder():
    return render_template("add_reminder.html")

@app.route('/test/<file>')
def test(file):
    return render_template(file)

#------------------------------------------------------
# API ~~ CRUD functions

@app.route("/api/reminder/recover_pronote")
@login_required
def recover_homeworks(): # Recover all PRONOTE
    """Endpoint to recover PRONOTE homeworks
    ---
    tags:
      - Reminder CRUD operations
    description: Endpoint recovering all deleted PRONOTE homeworks linked to your account (must be logged in and have a linked PRONOTE account)
    responses:
      200:
        description: A list of all thee recovered reminders sorted chronologically by date property
        schema:
          type: array
          items:
            $ref: '#/definitions/Reminder'
      401:
        description: You are unauthenticated (you haven't linked your account to a PRONOTE account)
        schema:
          type: string
          example: No PRONOTE account linked to your account
      500:
        description: An error ocurred internally. This isn't planned and can have many causes
    """
    if current_user.pronote_username is not None:
        homeworks = Pronote_homework.query.filter_by(hidden=True, user_id=current_user.id)
        reminders = []
        for homework in homeworks:
            subject = Subject.query.get(homework.subject_id)
            reminder = Reminder(
                content=homework.content, 
                date=homework.date,
                user=current_user,
                user_id=current_user.id,
                tag_id=current_user.pronote_tag_id,
                subject_id=subject.id
            )
            db.session.add(reminder)
            db.session.commit()
            homework.hidden = False
            homework.reminder = reminder
            reminder.pronote = homework
            db.session.commit()
            reminders.append(reminder)
        sorted_rems = sorted(reminders, key=attrgetter('date'))
        return jsonify([r.to_json() for r in sorted_rems]), 200
    return "No PRONOTE account linked to your account", 401

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
    reminders = Reminder.query.get(rem_id)
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
      500:
        description: An error ocurred internally. This isn't planned and can have many causes
    """
    if current_user.pronote_username is not None:
        client = pronotepy.Client(
            'https://pronote.fis.edu.hk/eleve.html',
            username=current_user.pronote_username,
            password=current_user.pronote_password,
        )
        homeworks = client.homework(date_from=d.date.today())
        for homework in homeworks:
            my_homework = Pronote_homework.query.filter_by(
                content=homework.description, 
                user_id=current_user.id,
            ).first()
            if my_homework is None:
                subject = Subject.query.filter_by(content=homework.subject.name, user_id=current_user.id).first()
                if subject is None:
                    bgColor = helpers.adjust_color_brightness(homework.background_color, -35)
                    subject = Subject(
                        content=homework.subject.name, 
                        bg_color=bgColor,
                        user=current_user,
                        user_id=current_user.id
                    )
                    db.session.add(subject)
                    db.session.commit()
                reminder = Reminder(
                    content=homework.description, 
                    date=homework.date,
                    done = False,
                    user=current_user,
                    user_id=current_user.id,
                    tag_id=current_user.pronote_tag_id,
                    subject_id=subject.id
                )
                db.session.add(reminder)
                db.session.commit()
                my_homework = Pronote_homework(
                    content=homework.description, 
                    date=homework.date,
                    hidden=False,
                    reminder=reminder,
                    user_id=current_user.id,
                    tag_id=current_user.pronote_tag_id,
                    subject_id=subject.id
                )
                db.session.add(my_homework)
                reminder.pronote = my_homework
                db.session.commit()
    reminders = Reminder.query.filter_by(user_id=current_user.id).all()
    sorted_rems = sorted(reminders, key=attrgetter('date'))
    return jsonify([r.to_json() for r in sorted_rems]), 200

@app.route("/api/reminder/sort/<property>")
@login_required
def get_sorted_reminders(property): # Read all (sorted)
    """Endpoint to read reminders sorted with a certain property
    ---
    tags:
      - Reminder CRUD operations
    description: Endpoint returning all reminders linked to your account with a certain property (by default is sorted by date) (must be logged in)
    parameters:
      - name: property
        in: path
        type: string
        enum: ['tag_id', 'subject_id', 'date', 'content', 'id']
        required: true
    responses:
      200:
        description: A list of all reminders sorted by a property
        schema:
          type: array
          items:
            $ref: '#/definitions/Reminder'
      404:
        description: The specified property was not found
        schema:
          type: string
          example: Property not found
      500:
        description: An error ocurred internally. This isn't planned and can have many causes
    """
    if property in ["tag_id", "subject_id", "date", "content", "id"]:
        reminders = Reminder.query.filter_by(user_id=current_user.id).all()
        sorted_rems = sorted(reminders, key=attrgetter(property))
        return jsonify([r.to_json() for r in sorted_rems]), 200
    return "Property not found", 404

@app.route("/api/reminder/filter/<property>/<property_value>")
@login_required
def get_filtered_reminders(property, property_value): # Read all (filtered)
    """Endpoint to read reminders filtered 
    ---
    tags:
      - Reminder CRUD operations
    description: Endpoint returning all reminders  linked to your account filtered with a certain property (must be logged in)
    parameters:
      - name: property
        in: path
        type: string
        enum: ['tag_id', 'subject_id', 'date', 'content', 'id']
        required: true
      - name: property_value
        in: path
        type: string
        required: true
    responses:
      200:
        description: A list of all reminders filtered by a property
        schema:
          type: array
          items:
            $ref: '#/definitions/Reminder'
      404:
        description: The specified property/property_id was not found
        schema:
          type: string
          example: Property not found
      500:
        description: An error ocurred internally. This isn't planned and can have many causes
    """
    if property in ["tag_id", "subject_id", "date", "content", "id"]:
        reminders = Reminder.query.filter_by(user_id=current_user.id, done=False).all()
        filtered_rems = filter(lambda rem: getattr(rem, property) == type(getattr(rem, property))(property_value), reminders)
        sorted_rems = sorted(filtered_rems, key=attrgetter('date'))
        return jsonify([r.to_json() for r in sorted_rems]), 200
    return "Property not found", 404
    
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
                        done=False,
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
def delete_reminder(rem_id): # Delete one
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
    reminder = Reminder.query.get(rem_id)
    if reminder:
        if reminder.user_id == current_user.id: # Layer of security
            if reminder.pronote_id is not None:
                pronote = reminder.pronote
                pronote.hidden = True
                pronote.reminder = None
            db.session.delete(reminder)
            db.session.commit()
            return "Reminder deleted succesfully", 200
        else:
            return "Not logged in the right account", 403
    else:
        return "Reminder not found", 404
    
@app.route("/api/reminder", methods=["DELETE"])
@login_required
def delete_reminders(): # Delete all
    """Endpoint to delete reminders
    ---
    tags:
      - Reminder CRUD operations
    description: Endpoint deleting all reminders linked to your account (must be logged in)
    responses:
      200:
        description: A confirmation message
        schema:
          type: string
          example: Reminders deleted succesfully
      500:
        description: An error ocurred internally. This isn't planned and can have many causes
    """
    reminders = Reminder.query.filter_by(user_id=current_user.id).all()
    for reminder in reminders:
        if reminder.pronote_id is not None:
            pronote = reminder.pronote
            pronote.hidden = True
            pronote.reminder = None
        db.session.delete(reminder)
    db.session.commit()
    return "Reminders deleted succesfully", 200

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

@app.route("/api/reminder/done/<int:rem_id>/<status>")
@login_required
def mark_rem_as_done(rem_id, status): # Mark one as done
    """Endpoint to mark as done a reminder
    ---
    tags:
      - Reminder CRUD operations
    description: Endpoint to mark as done a reminder with a specified id (must be logged in)
    parameters:
      - name: rem_id
        in: path
        type: integer
        required: true
      - name: status
        in: path
        type: string
        enum: ['True', 'False']
        required: true
    responses:
      200:
        description: A validation message
        schema:
          type: string
          example: Reminder marked as done
      400:
        description: The status argument is invalid
        schema:
          type: string
          example: Invalid argument status. Must be included in ['True', 'False']
      403:
        description: The reminder you're trying to access doesn't belong to you
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
    reminder = Reminder.query.get(rem_id)
    if reminder is not None:
        if reminder.user_id == current_user.id: # Layer of security
            if status in ["True", "False"]:
                if reminder.pronote_id is not None:
                    client = pronotepy.Client(
                        'https://pronote.fis.edu.hk/eleve.html',
                        username=current_user.pronote_username,
                        password=current_user.pronote_password,
                    )
                    homeworks = client.homework(date_from=reminder.date.date())
                    homeworks = list(filter(lambda hw: hw.description == reminder.content and hw.date == reminder.date.date(), homeworks))
                    homework = homeworks[0]
                    homework.set_done(status == "True")
                reminder.done = (status == "True")
                db.session.commit()
                return "Reminder marked as done succesfully", 200
            return "Invalid argument status. Must be included in ['True', 'False']", 400
        return "Not logged in the right account", 403
    return "Reminder not found", 404

@app.route("/send_reminders")
def send_reminders(): # Send email when due soon
    args = request.args
    if args and args.get("pat"):
        pat = Pat.query.filter_by(name="send_reminders").first()
        request_pat = args.get("pat")
        if bcrypt.check_password_hash(pat.val, request_pat):
            today = d.date.today()
            tomorrow = today + timedelta(days=1)
            emails_sent = 0
            for user in User.query.filter_by(active=True, accept_mail=True).all():
                reminders = Reminder.query.filter(Reminder.user_id==user.id, func.DATE(Reminder.date) == tomorrow).all()
                print(Reminder.query.get(1).date.date())
                print(tomorrow)
                if reminders:
                    message = f"""
<h1>Bonjour {user.username},<br>
Vous avez un ou plusieurs devoir à faire pour demain.</h1>
<h2>Le(s) voici :</h2>
"""
                    for reminder in reminders:
                        subject = Subject.query.get(reminder.subject_id)
                        tag = Tag.query.get(reminder.tag_id)
                        message += f"""
<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Anaheim"> <!-- Google fonts -->
  <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Architects%20Daughter"> <!--Google fonts -->
<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet"> <!-- Google icons -->
<div style="padding: 10px;">     
<table style="
        background-color: {subject.bg_color};
        width: 21vw;
        height: 102px;
        border-radius: 15px;
        overflow: auto;
        color: #fff;
        vertical-align: middle;  
        text-align: center;
        ">
  <tr>
    <td>
      <a style="padding: 7px;
        padding-right: 10px;
        padding-left: 10px;
        border-radius: 20px;
        font-size: 13px;
        
        background-color: {tag.bg_color};">{tag.content}</a>
    </td>
    <td style="font-family: 'Anaheim', sans-serif;
        font-size: 13px;
        padding-left: 0px;
position: relative;">Pour : Demain
    <a href="https://quantix.pythonanywhere.com/agenda">
    <img style="width: 15px;
    height: 15px;
    height: 1vh;
    
    position: absolute;
    top: 5; 
    right: 5;
    cursor: pointer;" src="https://quantix.pythonanywhere.com/static/images/open_icon.png">
    </a>
</td>
  </tr>
  <tr>
    <td colspan="2" style="font-family: 'Architects Daughter', sans-serif;
        font-size: 23px;
        font-weight: bold;
        line-height: 0.1;"
        color:white>{subject.content}</td>
  </tr>
  <tr>
    <td colspan="2">{reminder.content}</td>
  </tr>
</table>
</div>
"""
                    message += """
<h4>Merci Beaucoup d'utiliser notre site !<br>Sincèrement, <br>Quentin de chez Quantix.</h4>
<p>P.S. : Mon équipe et moi (nous sommes 2) travaillons d'arrache pied pour vous apporter le meilleur service possible</p>
"""
                    mail = Mail(
                        from_email='quantix.agenda@gmail.com',
                        to_emails=user.email,
                        subject="Devoir(s) à faire pour demain",
                        html_content=message
                    )
                    sg = SendGridAPIClient(current_app.config["SENDGRID_API_KEY"])
                    response = sg.send(mail)
                    emails_sent += 1
            return f"Sucesfully sent {emails_sent} email(s)!", 200
        return "Invalid PAT (Personnal Authorisation Token)", 403
    return "Invalid args to request, no PAT", 401

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

@app.route("/api/subject")
@login_required
def get_subjects(): # Read all
    """Endpoint to read subjects
    ---
    tags:
      - Subject CRUD operations
    description: Endpoint returning all subjects linked to your account (must be logged in)
    responses:
      200:
        description: A list of all subjects 
        schema:
          type: array
          items:
            $ref: '#/definitions/Subject'
      500:
        description: An error ocurred internally. This isn't planned and can have many causes
    """
    subjects = Subject.query.filter_by(user_id=current_user.id).all()
    return jsonify([s.to_json() for s in subjects])

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
        username = data.get("username")
        if User.query.filter_by(email=email).first() is None:
            if User.query.filter_by(username=username).first() is None:
                if data.get("password1") == data.get("password2"):
                    user = User(
                        username=username,
                        email=email,
                        password=bcrypt.generate_password_hash(data.get("password1")).decode('utf-8'),
                        active=False,
                        accept_mail = data.get("accept_notif")
                    )
                    db.session.add(user)
                    db.session.commit()
                    return jsonify({"message": "Registering done succesfully", "user_id": user.id}), 200 # Error here ~Probably~
                else:
                    return jsonify({"message": "Les mots de passe ne correspondent pas."}), 400
            end_of_sentence = "ce username."
        else:
            end_of_sentence = "cette adresse email."
        response = {
            "message": f"Un compte existe déjà avec {end_of_sentence}",
            "link_href": "/login",
            "link_display":"Se connecter"
        }
        return jsonify(response), 400
    return render_template("register.html")

@app.route('/otp')
def create_otp():
    args = request.args
    if args and args.get("ui"):
        user_id = args.get("ui")
        user = User.query.get_or_404(user_id)
        if not user.active:
            otp = Otp.query.filter_by(user_id=user.id).first()
            if otp is not None:
                db.session.delete(otp)
                db.session.commit()
            otp=Otp(
                value=random.randrange(100000, 1000000),
                expiry=helpers.add_seconds(datetime.now(), 10 * 60), # Set the expiry date to 10 min from now
                user_id=user.id
            )
            db.session.add(otp)
            db.session.commit()
            message = Mail(
                from_email='quantix.agenda@gmail.com',
                to_emails=user.email,
                subject="Requête d'inscription sur Quantix",
                html_content=render_template("verify_email.html", username=user.username, email=user.email, otp=otp.value)
            )
            sg = SendGridAPIClient(current_app.config["SENDGRID_API_KEY"])
            response = sg.send(message)
            return render_template("otp.html", otp_id=otp.id), 200
        return "<h1>403</h1>Account already activated", 403
    return "<h1>400</h1>Invalid arguments to request", 400
 
@app.route('/otp', methods=["POST"])
def validate_otp():
    data = json.loads(request.data)
    otp_id = data.get("otp_id")
    otp_value = int(data.get("otp"))
    print(otp_value)
    otp = Otp.query.get_or_404(otp_id)
    print(otp.value)
    if otp.expiry > datetime.now():
        if otp.value == otp_value:
            user = User.query.get_or_404(otp.user_id)
            user.active = True
            db.session.commit()
            return "Sucessfully activated account", 200
        return "Wrong OTP", 400
    return "OTP sent too late", 403
 
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = json.loads(request.data)
        username = data.get('username')
        try:
            user = User.query.filter_by(
                username=username).first()
            if user.active:
                if bcrypt.check_password_hash(user.password, data.get('password')):
                    login_user(user)
                    return jsonify({"message": "Logged in successfully"}), 200
                raise AttributeError
            response = {
                "message": "Votre compte n'est pas activé.",
                "link_href": f"/otp?ui={user.id}",
                "link_display":"L'activer"
            }
            return jsonify(response), 400
        except AttributeError:
            response = {"message": "Le username ou le mot de passe est incorrect."}
            return jsonify(response), 400
    return render_template("login.html")
 
 
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route("/delete_account")
@login_required
def delete_account():
    tables = [Tag, Subject, Reminder, Pronote_homework, Otp]
    for table in tables:
        table.query.filter_by(user_id=current_user.id).delete()
    db.session.delete(User.query.get(current_user.id))
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/forgot_password")
def forgot_pw_page():
    return render_template("forgot_pw.html")

@app.route("/forgot_password", methods=["POST"])
def forgot_pw_mail():
    data = json.loads(request.data)
    email = data.get('email')
    user = User.query.filter_by(email=email).first()
    if user is not None:
        Token.query.filter_by(user_id=user.id).delete()
        token = Token(
            val=str(uuid4()),
            expiry=helpers.add_seconds(datetime.now(), 10 * 60), # Set the expiry date to 10 min from now
            user_id=user.id
        )
        db.session.add(token)
        db.session.commit()
        message = Mail(
                from_email='quantix.agenda@gmail.com',
                to_emails=email,
                subject="Mot de passe oublié",
                html_content=render_template("forgot_pw_mail.html", user=user, token=token.val)
            )
        sg = SendGridAPIClient(current_app.config["SENDGRID_API_KEY"])
        sg.send(message)
        return "Email envoyé avec succès", 200
    return jsonify({"message": "L'adresse email ne correspond à aucun compte"}), 404

@app.route("/reset_password")
def reset_pw_page():
    args = request.args
    if args and args.get("token"):
        request_token = args.get("token")
        token = Token.query.filter_by(val=request_token).first()
        if token is not None:
            if token.expiry > datetime.now():
                Token.query.filter_by(user_id=token.user_id).delete()
                return render_template("reset_pw.html", token=token.val), 200
            return "Identification token expired (too late)", 403
        return "Invalid token", 401
    return "Token argument not found", 404

@app.route("/reset_password", methods=["POST"])
def reset_pw():
    data = json.loads(request.data)
    if data and data.get("token"):
        request_token = data.get("token")
        token = Token.query.filter_by(val=request_token).first()
        if token is not None:
            if data.get('password1') == data.get('password2'):
                user = User.query.get(token.user_id)
                if not bcrypt.check_password_hash(user.password, data.get('password2')):
                    user.password = bcrypt.generate_password_hash(data.get("password2")).decode('utf-8')
                    db.session.commit()
                    return "Password modified succesfully", 200
                return jsonify({"message": "Votre nouveau mot de passe ne peut pas être votre ancien mot de passe"}), 403 # new password can't be old password
            return jsonify({"message": "Les deux mots de passe ne sont pas identique"}), 400 # the two passwords aren't the same
        return jsonify({"message": "Reéssayez plus tard (le token de la requête est incorrect)"}), 403 # request header token is invalid
    return jsonify({"message": "Reéssayez plus tard (aucun token fourni)"}), 401 # request header token is not provided
                

            
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


#------------------------------------------------------
# Other
@app.cli.command('clear')
def drop_tables():
    tables = [Tag, Subject, Reminder, Pronote_homework, User, Otp, Pat, Token]
    for table in tables:
        db.session.query(table).delete()
    db.session.commit()
    print("Tables cleared succesfully")


@app.cli.command('sandbox')
def sandbox():
    print(type(Reminder.query.get(1).date))
    print('Success')

@app.cli.command("create_pat")
@click.option('--value')
def create_pat(value):
    pat_value = bcrypt.generate_password_hash(value).decode('utf-8')
    pat = Pat(name="send_reminders", val=pat_value)
    db.session.add(pat)
    db.session.commit()
    click.echo(Pat.query.get(pat.id).name)
    return "Added succesfully"


