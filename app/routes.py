#------------------------------------------------------
# Define all entry points (Web pages & API endpoints)
#------------------------------------------------------
import os, pronotepy, random, click, requests
import datetime as d
from flask import jsonify, json, abort, request, render_template, redirect, current_app, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from git import Repo
from flask_bcrypt import Bcrypt 
from . import helpers, create_app, db, swagger
from datetime import datetime, timedelta, date
from operator import attrgetter
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from sqlalchemy import func
from uuid import uuid4
from flasgger import swag_from

from .models import Tag, Subject, Reminder, Pronote_homework, User, Otp, Pat, Token, Friendship, Mail_log


app = create_app(os.getenv('FLASK_CONFIG') or 'default')

"""
To-do list :
    - Finish swagger 
    - Make it possible to send reminders to other persons/users
    - Make it possible to pin a reminder (done, need to use that in read operations of remiders)
    - Change approach of filter and sort reminders (make one function with arguments)
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
@app.route("/api/reminder/<int:rem_id>")
@login_required
@swag_from('swagger/reminders/get_reminder.yml')
def get_reminder(rem_id): # Read one
    reminders = Reminder.query.get(rem_id)
    if reminders is not None:
        if reminders.user_id == current_user.id:
            return jsonify(reminders.to_json()), 200
        return "Not logged into the account of the reminder", 403
    return "Reminder not found", 404
    
@app.route("/api/reminder/recover_pronote")
@login_required
@swag_from('swagger/reminders/recover_homeworks.yml')
def recover_homeworks(): # Recover all PRONOTE
    if current_user.pronote_tag_id is not None:
        homeworks = Pronote_homework.query.filter_by(hidden=True, user_id=current_user.id)
        reminders = []
        for homework in homeworks:
            subject = Subject.query.get(homework.subject_id)
            reminder = Reminder(
                content=homework.content, 
                date=homework.date,
                done=False,
                pinned=False,
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
    return "No PRONOTE homeworks ever fetched from your account", 401
    
@app.route("/api/reminder")
@login_required
@swag_from('swagger/reminders/get_reminders.yml')
def get_reminders(): # Read all
    args = request.args
    sort = args.get("sort")
    filter = args.get("filter")
    f_value = args.get("f_value")
    reminders = Reminder.query.filter(Reminder.user_id == current_user.id, func.DATE(Reminder.date) > date.today() - timedelta(days=1)).all()
    print(reminders)
    if None not in [filter, f_value]:
        reminders = filter(lambda rem: getattr(rem, f_value) == f_value, reminders)
    if sort is not None:
        if sort in ["tag_id", "subject_id", "date", "content", "id"]:
            reminders = sorted(reminders, key=attrgetter(sort))
        else:
            return "Sorting property of reminder is invalid", 400
    else:
        reminders = sorted(reminders, key=attrgetter('date'))
    reminders = sorted(reminders, key=attrgetter('pinned'), reverse=True)
    old_rems = Reminder.query.filter(Reminder.user_id == current_user.id, func.DATE(Reminder.date) < date.today() - timedelta(days=2))
    old_rems.delete()
    db.session.commit()
    return jsonify([r.to_json() for r in reminders]), 200

@app.route("/api/reminder/sort/<property>")
@login_required
@swag_from('swagger/reminders/get_sorted_reminders.yml')
def get_sorted_reminders(property): # Read all (sorted)
    if property in ["tag_id", "subject_id", "date", "content", "id"]:
        reminders = Reminder.query.filter_by(user_id=current_user.id).all()
        sorted_rems = sorted(reminders, key=attrgetter(property))
        return jsonify([r.to_json() for r in sorted_rems]), 200
    return "Property not found", 404

@app.route("/api/reminder/filter/<property>/<property_value>")
@login_required
@swag_from('swagger/reminders/get_filtered_reminders.yml')
def get_filtered_reminders(property, property_value): # Read all (filtered)
    if property in ["tag_id", "subject_id", "date", "content", "id"]:
        reminders = Reminder.query.filter_by(user_id=current_user.id).all()
        filtered_rems = filter(lambda rem: getattr(rem, property) == type(getattr(rem, property))(property_value), reminders)
        sorted_rems = sorted(filtered_rems, key=attrgetter('date'))
        return jsonify([r.to_json() for r in sorted_rems]), 200
    return "Property not found", 404
    
@app.route("/api/reminder", methods=["POST"])
@login_required
@swag_from('swagger/reminders/create_reminders.yml')
def create_reminders(): # Create
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
                        pinned=False,
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
@swag_from('swagger/reminders/delete_reminder.yml')
def delete_reminder(rem_id): # Delete one
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
@swag_from('swagger/reminders/delete_reminders.yml')
def delete_reminders(): # Delete all
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
@swag_from('swagger/reminders/update_reminders.yml')
def update_reminders(rem_id): # Update
    data = json.loads(request.data)
    db_reminder = Reminder.query.get(rem_id)
    if db_reminder:
        if db_reminder.user_id == current_user.id:
            db_reminder.content = data.get("content")
            db_reminder.date = datetime.strptime(data.get("date"), "%Y-%m-%d")
            db_reminder.tag_id = data.get("tag_id")
            db_reminder.subject_id = data.get("subject_id")
            db.session.commit()
            return "Reminder updated succesfully", 200
        return "Not logged in the account of the reminder", 403
    return "Reminder not found", 404

@app.route("/api/reminder/done/<int:rem_id>/<status>", methods=["PATCH"])
@login_required
@swag_from('swagger/reminders/mark_rem_as_done.yml')
def mark_rem_as_done(rem_id, status): # Mark one as done
    reminder = Reminder.query.get(rem_id)
    if reminder is not None:
        if reminder.user_id == current_user.id: # Layer of security
            if status in ["True", "False"]:
                reminder.done = (status == "True")
                db.session.commit()
                return "Reminder marked as done succesfully", 200
            return "Invalid argument status. Must be included in ['True', 'False']", 400
        return "Not logged in the right account", 403
    return "Reminder not found", 404

@app.route("/api/reminder/pinned/<int:rem_id>/<status>", methods=["PATCH"])
@login_required
@swag_from('swagger/reminders/mark_rem_as_pinned.yml')
def mark_rem_as_pinned(rem_id, status): # Mark one as pinned
    reminder = Reminder.query.get(rem_id)
    if reminder is not None:
        if reminder.user_id == current_user.id: # Layer of security
            if status in ["True", "False"]:
                reminder.pinned= (status == "True")
                db.session.commit()
                return "Reminder marked as pinned (or not) succesfully", 200
            return "Invalid argument status. Must be included in ['True', 'False']", 400
        return "Not logged in the right account", 403
    return "Reminder not found", 404

@app.route("/send_reminders")
@swag_from('swagger/reminders/send_reminders.yml')
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
                reminders = Reminder.query.filter(Reminder.user_id==user.id, func.DATE(Reminder.date) == tomorrow, Reminder.done == False).all()
                if reminders:
                    subjects = []
                    tags = []
                    for reminder in reminders:
                        subject = Subject.query.get(reminder.subject_id)
                        subjects.append(subject)
                        tag = Tag.query.get(reminder.tag_id)
                        tags.append(tag)
                    mail = Mail(
                        from_email=current_app.config["BASE_EMAIL"],
                        to_emails=user.email,
                        subject="Devoir(s) à faire pour demain",
                        html_content=render_template(
                            "due_rem_mail.html", 
                            subjects=subjects, 
                            reminders=reminders, 
                            tags=tags,
                            user=user,
                            base_url=current_app.config["BASE_URL"]
                        )
                    )
                    sg = SendGridAPIClient(current_app.config["SENDGRID_API_KEY"])
                    response = sg.send(mail)
                    emails_sent += 1
            return f"Sucesfully sent {emails_sent} email(s)!", 200
        return "Invalid PAT (Personnal Authorisation Token)", 403
    return "Invalid args to request, no PAT", 401

@app.route("/fetch_from_pronote")
@login_required
def fetch_pronote_page():
    if None not in [current_user.pronote_url, current_user.pronote_username]:
        return render_template("login_pronote.html", url=current_user.pronote_url, username=current_user.pronote_username)
    return render_template("login_pronote.html", url="", username="")


@app.route("/api/subject/<int:subject_id>")
@login_required
@swag_from('swagger/subject/get_subject.yml')
def get_subject(subject_id): # Read one
    subject = Subject.query.get(subject_id)
    if subject:
        if subject.user_id == current_user.id:
            return jsonify(subject.to_json()), 200
        return "Not logged in the account of the subject", 403
    return "Subject not found", 404

@app.route("/api/subject")
@login_required
@swag_from('swagger/subject/get_subjects.yml')
def get_subjects(): # Read all
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

@app.route("/api/subject/<int:sub_id>", methods=["PUT"])
@login_required
@swag_from('swagger/subject/update_subjects.yml')
def update_subjects(sub_id): # Update
    data = json.loads(request.data)
    db_subject = Subject.query.get(sub_id)
    if db_subject is not None:
        if db_subject.user_id == current_user.id:
            db_subject.content = data.get("content")
            db_subject.bg_color = data.get("bgColor")
            db.session.commit()
            return "Subject updated succesfully", 200
        return "Not logged in the account of the subject", 403
    return "Subject not found", 404
        
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

@app.route("/api/tag/<int:tag_id>", methods=["PUT"])
@login_required
@swag_from('swagger/tag/update_tags.yml')
def update_tags(tag_id): # Update
    data = json.loads(request.data)
    db_tag = Tag.query.get(tag_id)
    if db_tag is not None:
        if db_tag.user_id == current_user.id:
            db_tag.content = data.get("content")
            db_tag.bg_color = data.get("bgColor")
            db.session.commit()
            return "Tag updated succesfully", 200
        return "Not logged in the account of the tag", 403
    return "Tag not found", 404
        
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
# User
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
                from_email=current_app.config["BASE_EMAIL"],
                to_emails=user.email,
                subject="Requête d'inscription sur Quantim",
                html_content=render_template(
                    "verify_email.html", 
                    username=user.username, 
                    email=user.email, 
                    otp=otp.value, 
                    base_url=current_app.config["BASE_URL"])
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
    otp = Otp.query.get_or_404(otp_id)
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

@app.route("/account", methods=["DELETE"])
@login_required
@swag_from('swagger/user/delete_account.yml')
def delete_account():
    tables = [Tag, Subject, Reminder, Pronote_homework, Otp, Token, Friendship, Mail_log]
    for table in tables:
        if table == Friendship:
            table.query.filter_by(uid=current_user.id).delete()
            table.query.filter_by(fid=current_user.id).delete()
        else:
            table.query.filter_by(user_id=current_user.id).delete()
    db.session.delete(User.query.get(current_user.id))
    db.session.commit()
    logout_user()
    return "Account deleted succesfully", 200
    
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
                from_email=current_app.config["BASE_EMAIL"],
                to_emails=email,
                subject="Mot de passe oublié",
                html_content=render_template(
                    "forgot_pw_mail.html", 
                    user=user, 
                    token=token.val, 
                    base_url=current_app.config["BASE_URL"]
                )
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


#------------------------------------------------------
# Friend
@app.route("/add_friend")
@login_required
def add_friend_page():
    return render_template("add_friend.html")

@app.route("/friend", methods=["POST"])
@login_required
def add_friend():
    data = json.loads(request.data)
    if data and data.get("username"):
        f_username = data.get("username")
        friend = User.query.filter_by(username=f_username).first()
        if friend is not None:
            if friend.id != current_user.id:
                if Friendship.query.filter_by(fid=friend.id).first() is None:
                    message = Mail(
                            from_email=current_app.config["BASE_EMAIL"],
                            to_emails=friend.email,
                            subject="Requête d'amitié",
                            html_content=f"<a href='{current_app.config['BASE_URL']}/friend_back?id={current_user.id}'>clique</a>" # CHANGER CECI !!!
                        )
                    sg = SendGridAPIClient(current_app.config["SENDGRID_API_KEY"])
                    sg.send(message)
                    friendship = Friendship(
                        uid = current_user.id,
                        user = current_user,
                        fid = friend.id,
                        friend = friend
                    )
                    db.session.add(friendship)
                    db.session.commit()
                    return "Sent a friend request succesfully", 200
                return jsonify({"message": "You're not allowed to become friends with that person because you already are"}), 403
            return jsonify({"message": "You're not allowed to become friends with that person because it's you"}), 403
        return jsonify({"message": "The user with the specified username was not found"}), 404
    return "Missing or invalid data sent", 400

@app.route("/friend_back")
@login_required
def friend_back_page():
    args = request.args
    friend_id = args.get("id")
    if None not in [args, friend_id]: 
        friend = User.query.get(friend_id)
        if friend is not None:
            return render_template("friend_back.html", id=friend_id, username=friend.username), 200
        return "A user with the specified id was not found", 404
    return "Missing or invalid data sent", 400

@app.route("/friend_back", methods=["POST"])
@login_required
@swag_from('swagger/friend/friend_back.yml')
def friend_back():
    data = json.loads(request.data)
    friend_id = data.get("id")
    username = data.get("username")
    if None not in [data, friend_id, username]:
        if current_user.username == username:
            friend = User.query.get(friend_id)
            if friend is not None:
                if friend.id != current_user.id:
                    friendship = Friendship.query.filter_by(fid=current_user.id, uid=friend_id).first()
                    if friendship is not None:
                        new_friendship = Friendship(
                            uid = current_user.id,
                            user = current_user,
                            fid = friend.id,
                            friend = friend
                        )
                        db.session.add(new_friendship)
                        db.session.commit()
                        message = Mail(
                            from_email=current_app.config["BASE_EMAIL"],
                            to_emails=friend.email,
                            subject="Requête d'amitié",
                            html_content=f"L'utilisateur {friend.username} a accepté votre requête d'amitié" # CHANGER CECI !!!
                        )
                        sg = SendGridAPIClient(current_app.config["SENDGRID_API_KEY"])
                        sg.send(message)
                        return f"Sucessfully friended back {friend.username}, I declare you now BFF", 200
                    return jsonify({"message" : "You aren't allowed to friend back this user because they never friended you"}), 403
                return jsonify({"message" : "Vous ne pouvez pas devenir ami avec cette personne car c'est vous"}), 403
            return jsonify({"message" : "The user with the specified id was not found"}), 404
        return jsonify({"message": "Le username ne correspond pas à celui de votre compte"}), 401
    return "Missing or invalid data sent", 400

@app.route("/friendship_tester")
@login_required
@swag_from('swagger/friend/friendship_tester.yml')
def friendship_tester():
    args = request.args
    id = args.get("id")
    if args and id is not None:
        friend = User.query.get(id)
        if friend is not None:
            friendship_a = Friendship.query.filter_by(uid=current_user.id, fid=id).first()
            friendship_b = Friendship.query.filter_by(uid=id, fid=current_user.id).first()
            if friendship_a is not None:
                if friendship_b is not None:
                    return "Clearly two BFFs", 200
                return "That user is not friend with you ):", 400
            return "You are not friend with that user ):", 400
        return "A user with the specified id was not found", 404
    return "Missing or invalid data sent", 401

@app.route("/send_reminder")
@login_required
def send_rem_to_friend():
    args = request.args
    friend_id = args.get("f_id")
    rem_id = args.get("r_id")
    if None not in [args, friend_id, rem_id]:
        friend = User.query.get(friend_id)
        if friend is not None:
            reminder = Reminder.query.get(rem_id)    
            if reminder is not None:    
                friendship_a = Friendship.query.filter_by(uid=current_user.id, fid=friend_id).first()
                friendship_b = Friendship.query.filter_by(uid=friend_id, fid=current_user.id).first()
                if None not in [friendship_a, friendship_b]:
                    if friend.friend_tag_id is None:
                        tag = Tag(
                            content="d'un ami", 
                            bg_color="#2951BD",
                            user=friend,
                            user_id=friend.id
                        )
                        db.session.add(tag)
                        db.session.commit()
                        friend.friend_tag_id = tag.id
                    subject = Subject.query.get(reminder.subject_id)
                    f_subject = Subject(
                        content=subject.content, 
                        bg_color=subject.bg_color,
                        user=friend,
                        user_id=friend.id
                    )
                    db.session.add(f_subject)
                    db.session.commit()
                    f_reminder = Reminder(
                        content=reminder.content, 
                        date=reminder.date,
                        done = False,
                        pinned = False,
                        user=friend,
                        user_id=friend.id,
                        tag_id=friend.friend_tag_id,
                        subject_id=f_subject.id
                    )
                    db.session.add(f_reminder)
                    db.session.commit()
                    return "Reminder sent succesfully", 200
                return "You can't send a reminder to that person because you are not friends", 403
            return "Reminder with specified id was not found", 404
        return "Friend with specified id was not found", 404
    return "Missing or invalid data sent", 400

@app.route("/friends")
@login_required
@swag_from('swagger/friend/get_friends.yml')
def get_friends():
    friends = []
    for friendship in Friendship.query.filter_by(uid=current_user.id).all():
        friend = User.query.get(friendship.fid)
        if Friendship.query.filter_by(uid=friend.id, fid=current_user.id).first() is not None:
            friends.append(friend)
    return [f.to_json() for f in friends], 200

#------------------------------------------------------
# Miscellaneous
@app.route("/fetch_from_pronote", methods=["POST"])
@login_required
@swag_from('swagger/miscellaneous/fetch_pronote.yml')
def fetch_pronote():
    if request.data:
        data = json.loads(request.data)
        url = data.get('pronote_url')
        username = data.get('username')
        password = data.get('password')
        if None not in [username, password, url]:
            try:
                client = pronotepy.Client(
                    pronote_url=url,
                    username=username,
                    password=password,
                )
                if current_user.pronote_tag_id is None:
                    tag = Tag(
                        content="de PRONOTE", 
                        bg_color="#009853",
                        user=current_user,
                        user_id=current_user.id
                    )
                    db.session.add(tag)
                    db.session.commit()
                    current_user.pronote_tag_id = tag.id
                current_user.pronote_url = url
                current_user.pronote_username = username
                db.session.commit()
            except pronotepy.CryptoError:
                return jsonify({"message": "Le mot de passe ou l'identifiant est incorrect"}), 403  # the client has failed to log in
            except (requests.exceptions.SSLError, pronotepy.exceptions.PronoteAPIError):
                return jsonify({"message": "La page PRONOTE n'a pas été trouvé (lien invalide)"}), 404
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
                        pinned=False,
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
            return "Homeworks fetched succesfully", 200
        return "Invalid request (one or more arguments in body are missing or invalid)", 400
    return "Missing body argument - No data sent", 401

@app.route("/send_feedback", methods=["POST"])
@login_required
@swag_from('swagger/miscellaneous/send_feedback.yml')
def send_feedback():
    if request.data:
        data = json.loads(request.data)
        anonymous = data.get("anonymous")
        content = data.get("content")
        if None not in [anonymous, content] and type(anonymous) == bool:
            mail = "<h1>"
            if not anonymous:
                mail += f"Retour de l'utilisateur : {current_user.username}"
            else: 
                mail += "Retour d'un utilisateur anonyme"
            mail += "</h1><hr>" + content
            message = Mail(
                from_email=current_app.config["BASE_EMAIL"],
                to_emails=current_app.config["BASE_EMAIL"],
                subject="Retour d'utilisateur",
                html_content=mail
            )
            sg = SendGridAPIClient(current_app.config["SENDGRID_API_KEY"])
            sg.send(message)
            mail_log = Mail_log(
                date = datetime.now(),
                user_id = current_user.id,
                user=current_user
            )
            db.session.add(mail_log)
            db.session.commit()
            return "Succesfully sent feedback", 200
        return "Missing or invalid data sent", 400
    return "Argument body was not found (no data sent)", 400

#------------------------------------------------------
# Commands
@app.cli.command('clear')
def drop_tables():
    tables = [Tag, Subject, Reminder, Pronote_homework, User, Otp, Pat, Token, Friendship, Mail_log]
    for table in tables:
        db.session.query(table).delete()
    db.session.commit()
    print("Tables cleared succesfully")


@app.cli.command('sandbox')
def sandbox():
    db.session.query(Pat).delete()
    print('Success')

@app.cli.command('test')
def sandbox():
    print(User.query.get(1).reminders)

@app.cli.command("create_pat")
@click.option('--value')
def create_pat(value):
    pat_value = bcrypt.generate_password_hash(value).decode('utf-8')
    pat = Pat(name="send_reminders", val=pat_value)
    db.session.add(pat)
    db.session.commit()
    click.echo(f"Added succesfully a pat with a name of: {Pat.query.get(pat.id).name}")
    return "Added succesfully"


