#------------------------------------------------------
# Define all entry points (Web pages & API endpoints)
#------------------------------------------------------
import os
from flask import jsonify, abort, request, render_template, redirect, current_app, url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user
from git import Repo
from . import helpers, create_app, db

from .models import Tag, Reminder, Users

from .models import Tag, Reminder

from .models import Tag, Reminder

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

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
def agenda():
    reminders = Reminder.query.all()
    return render_template('agenda.html', title="Agenda Personnel", user="test", reminders=reminders)

#------------------------------------------------------
# API
#--- Claim ------------
@app.route("/api/reminder/list", methods=["GET"])
def get_reminders():
    reminders = Reminder.query.all()
    return jsonify([r.to_json() for r in reminders])


#------------------------------------------------------
# Auto deploy
@app.route('/api/push_version', methods=['POST'])
def git_webhook():
    x_hub_signature = request.headers.get('X-Hub-Signature')
    if request.method == 'POST':
        helpers.verify_signature(request.data, current_app.config['GIT_REPO_SECRET'],x_hub_signature)
        repo = Repo(current_app.config['GIT_REPO_PATH'])
        origin = repo.remotes.origin
        origin.pull(current_app.config['GIT_REPO_BRANCH'])
        return 'Updated PythonAnywhere successfully', 200
    else:
        return 'Wrong event type', 400

#------------------------------------------------------
# User Verification
login_manager = LoginManager()

@login_manager.user_loader
def loader_user(user_id):
    return Users.query.get(user_id)
    
@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user = Users(username=request.form.get("username"),
                     password=request.form.get("password"))
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("sign_up.html")
 
 
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = Users.query.filter_by(
            username=request.form.get("username")).first()
        if user.password == request.form.get("password"):
            login_user(user)
            return redirect(url_for("home"))
    return render_template("login.html")
 
 
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))
