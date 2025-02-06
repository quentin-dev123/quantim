from . import db
from flask_login import UserMixin

R_SUBJECT_MAX_SIZE=100
R_CONTENT_MAX_SIZE=500

class Subject(db.Model):
    __tablename__ = 'Subjects'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(30), nullable=False)
    bg_color = db.Column(db.String(10), nullable=False)
    # --- Relationships --- 
    reminders = db.relationship("Reminder", backref="subject")
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))

    def to_json(self):
        js = {
            'id': self.id,
            'content': self.content,
            'bg_color': self.bg_color,
            'user_id': self.user_id
        }
        return js 

class Tag(db.Model):
    __tablename__ = 'Tags'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(30), nullable=False)
    bg_color = db.Column(db.String(10), nullable=False)
    # --- Relationships --- 
    reminders = db.relationship("Reminder", backref="tag")
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))

    def to_json(self):
        js = {
            'id': self.id,
            'content': self.content,
            'bg_color': self.bg_color,
            'user_id': self.user_id
        }
        return js 

class Reminder(db.Model):
    __tablename__ = 'Reminders'
    reminder_id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(R_CONTENT_MAX_SIZE), nullable=True)
    date = db.Column(db.DateTime, nullable=True)
    # --- Relationships --- 
    tag_id = db.Column(db.Integer, db.ForeignKey('Tags.id'))
    subject_id = db.Column(db.Integer, db.ForeignKey('Subjects.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    
    def to_json(self):
        js = {
            'id': self.reminder_id,
            'content': self.content,
            'date': self.date.isoformat(),
            'tag_id': self.tag_id,
            'user_id': self.user_id,
            'subject_id': self.subject_id
        }
        return js 

class User(UserMixin, db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    # --- Relationships --- 
    reminders = db.relationship("Reminder", backref="user")
    tags = db.relationship("Tag", backref="user")
    subjects = db.relationship("Subject", backref="user")
