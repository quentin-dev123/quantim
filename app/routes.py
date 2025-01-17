#------------------------------------------------------
# Define all entry points (Web pages & API endpoints)
#------------------------------------------------------
import os
from flask import jsonify, abort, request, render_template, redirect, current_app
from git import Repo
from . import helpers, create_app

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

#------------------------------------------------------
# API
@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

#------------------------------------------------------
# WEB

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