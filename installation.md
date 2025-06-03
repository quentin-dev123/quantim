# Quantim


## Works like a personal agenda

---


### Manage source code versioning ###
Use of standard "*[feature branch](https://www.atlassian.com/git/tutorials/comparing-workflows/feature-branch-workflow)*" workflow:

![feature branch workflow](./ressources/feature_branch.png)
- main branch is reflecting at all time the "production" version
- each new feature work should be implemented in a dedicated branch starting from latest main version:
    ```
    git checkout -b new_feature
    ```
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

## The Database:

### Setting up DB
First, initialize the db and migrations (the tool to manage changes to the database structure):
```
flask db init
```

If you get this error: 
```
Error: Directory migrations already exists and is not empty
```

You'll need to erase migrations and redo db init: 
```
rm -rf migrations
flask db init
```

Then remove the migrations folder (even if you just deleted it like detailed above) :
```
rm -rf migrations
```

Now you can pull the correct one from GitHub:
```
git stash # Cancel your changes (deleting migrations)
git pull # This isn't necessary, you may already be up to date 
```

Now, update your db with the correct version: 
```
flask db upgrade
```

That's it, your database is up to date. Now you'll need to keep up with every new version of the db structure 

### After DB structure changes

to manage changes made on the database structure on the running environment you need to keep track of those change and prepare migrations scripts.
These can be automativally generated.

To do so, after each change in models.py, run:
```
flask db migrate -m "comment"
```

then commit all changes includint the new files created in the folder migrations.

To apply the last changes on the db on a running environment or to create a new empty DB with latest structure for your local devs/test, run:
```
flask db upgrade
```
### Keeping the DB up to date
Note:
When you do a ```git pull```, you need to look if the commit(s) message(s) contain db upgrade needed. In that case,
you need to logically upgrade your database, which can be done with : 
```
flask db upgrade
```

> This upgrade is necessary when changes have been made to the structure of the db.

## Run the application ##

### Prepare running environment ###

You need to install python virtual environment

```
python -m venv .venv
```
or if it is already created make sure to activate the virtual environment
```
[windows]>.venv\Script\activate
[linux]>.venv/bin/activate
```

### Install or update python modules ###

```
pip install -r requirements.txt
```

To run the application first set environment variable:
- **FLASK_APP**: path to the python script to launch the application

```
export FLASK_APP=quantim.py
```

and create in application folder a file named .env containing:

```
export GIT_REPO_PATH=<path to application folder>
export GIT_REPO_BRANCH=main
export BASE_URL='<base url used (if running local, usually is : http://127.0.0.1:5000)>'
export SENDGRID_API_KEY='<your sendgrid api key>'
export DEV_DATABASE_URL=sqlite://<absolute path to sqllite file>
```
> for windows it should look like sqlite:///C:\\\\path\\\\to\\\\foo.db
> for linux it should look like sqlite:////the_path/to_the_folder/the_db.sqlite

Finally launch it with
```
flask run
```

 If you get an error, it's possible you'll have to set FLASK_APP explicitly in the terminal:
```
export FLASK_APP=quantim.py
```
