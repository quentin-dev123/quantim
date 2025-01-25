from . import db
from enum import Enum
from flask_login import UserMixin

R_SUBJECT_MAX_SIZE=100
R_CONTENT_MAX_SIZE=500

class Tag(Enum):
    URGENT = 'Urgent'
    TODO = 'ToDo'

class Reminder(db.Model):
    __tablename__ = 'reminders'
    reminder_id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(R_SUBJECT_MAX_SIZE), nullable=True)
    content = db.Column(db.String(R_CONTENT_MAX_SIZE), nullable=True)
    date = db.Column(db.DateTime, nullable=True)
    tag = db.Column(db.Enum(Tag))
    
    def to_json(self):
        js = {
            'id': self.reminder_id,
            'subject': self.subject,
            'content': self.content,
            'date': self.date.isoformat(),
            'tag': self.tag
        }
        return js 

class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
