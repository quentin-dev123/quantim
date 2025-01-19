#------------------------------------------------------
# Define all entry points (Web pages & API endpoints)
#------------------------------------------------------
import os
from flask import jsonify, abort, request, render_template, redirect, current_app
from git import Repo
from . import helpers, create_app

from .models import Tag, Reminder

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

#------------------------------------------------------
# WEB
@app.route('/')
@app.route('/index')
def index():
    reminders = Reminder.query.all()
    return render_template('index.html', title="Agenda Personnel", user="test", reminders=reminders)

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