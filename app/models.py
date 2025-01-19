from . import db
from enum import Enum

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
            'amount': self.amount,
            'tag': self.tag,
        }
        return js