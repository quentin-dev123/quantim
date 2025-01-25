# Quantix
### Works like a personal agenda
> This project is still under developpement

### Manage source code versioning ###
Use of standard "*[feature branch](https://www.atlassian.com/git/tutorials/comparing-workflows/feature-branch-workflow)*" workflow:

![feature branch workflow](./ressources/feature_branch.png)
- main branch is reflecting at all time the "production" version
- each new feature work should be implemented in a dedicated branch starting from latest main version:
    ```
    git checkout -b new_feature
- before merging back the new feature to main you need to re-synch feature branch with main making sure you re-sync local repository with github version:
    ```
    git checkout main
    git pull
    git checkout feature_branch
    git merge main
    ```
- merge new feature to main branch once all cleaned up and ready to ship in production
    ```
    git checkout main
    git merge feature_branch
    ```

> Same approach can be used with contributor branches which resync then merge to deliver work done once finalized.


### After DB changes
to manage changes made on the database structure on the running environment you need to keep track of those change and prepare migrations scripts.
These can be automativally generated.

To do so, after each change in models.py, run:
>flask db migrate -m "comment"

then commit all changes includint the new files created in the folder migrations.

To apply the last changes on the db on a running environment or to create a new empty DB with latest structure for your local devs/test, run:
>flask db upgrade

## Run the application ##
### Prepare running environment ###

You need to install python virtual environment

```
python -m venv .venv
```
or if it is already created make sure to activate the virtual environment
```
[windows]>.venv\Script\activate
[linux]>.venev/bin/activate
```

### Install or update python modules ###

```
pip install -r requirements.txt
```

To run the application first set environment variable:
- **FLASK_APP**: path to the python script to launch the application

```
export FLASK_APP=quantix.py
```

and create in application folder a file named .env containing:

```
export GIT_REPO_PATH=<path to application folder>
export GIT_REPO_BRANCH=main
export DEV_DATABASE_URL=sqlite://<absolute path to sqllite file>
```
> for windows it should look like sqlite:///C:\\\\path\\\\to\\\\foo.db
> for linux it should look like sqlite:////the_path/to_the_folder/the_db.sqlite

Finally launch it with
```
flask run
```