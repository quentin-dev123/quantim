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
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(R_CONTENT_MAX_SIZE), nullable=True)
    date = db.Column(db.DateTime, nullable=True)
    done = db.Column(db.Boolean)
    pinned = db.Column(db.Boolean)
    # --- Relationships --- 
    pronote_id = db.mapped_column(db.ForeignKey("Pronote_homework.id"))
    pronote = db.relationship("Pronote_homework", back_populates="reminder")
    tag_id = db.Column(db.Integer, db.ForeignKey('Tags.id'))
    subject_id = db.Column(db.Integer, db.ForeignKey('Subjects.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    
    def to_json(self):
        js = {
            'id': self.id,
            'content': self.content,
            'date': self.date.isoformat(),
            'done': self.done,
            'tag_id': self.tag_id,
            'user_id': self.user_id,
            'subject_id': self.subject_id,
            'pronote_id': self.pronote_id
        }
        return js 
    
class Pronote_homework(db.Model):
    __tablename__ = 'Pronote_homework'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(R_CONTENT_MAX_SIZE), nullable=True)
    date = db.Column(db.DateTime, nullable=True)
    hidden = db.Column(db.Boolean)
    # --- Relationships --- 
    reminder = db.relationship("Reminder", uselist=False, back_populates="pronote")
    tag_id = db.Column(db.Integer, db.ForeignKey('Tags.id'))
    subject_id = db.Column(db.Integer, db.ForeignKey('Subjects.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    def to_json(self):
        js = {
            'id': self.id,
            'content': self.content,
            'date': self.date.isoformat(),
            'tag_id': self.tag_id,
            'user_id': self.user_id,
            'subject_id': self.subject_id,
            'reminder': self.reminder.to_json()
        }
        return js 

class User(UserMixin, db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True, nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    active = db.Column(db.Boolean)
    accept_mail = db.Column(db.Boolean)
    # --- PRONOTE --- 
    pronote_tag_id = db.Column(db.Integer, nullable=True)
    pronote_username = db.Column(db.String(250), nullable=True)
    pronote_url = db.Column(db.String(250), nullable=True)
    # --- Relationships --- 
    reminders = db.relationship("Reminder", backref="user")
    tags = db.relationship("Tag", backref="user")
    subjects = db.relationship("Subject", backref="user")
    otp = db.relationship("Otp", backref="user")
    token = db.relationship("Token", backref="user")
    mail_log = db.relationship("Mail_log", backref="user")
    friendeds = db.relationship("Friendship", foreign_keys="[Friendship.uid]", backref="user")
    frienders = db.relationship("Friendship", foreign_keys="[Friendship.fid]", backref="friend")

class Otp(db.Model):
    __tablename__ = 'Otp'
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer, nullable=False)
    expiry = db.Column(db.DateTime, nullable=False)
    # --- Relationships --- 
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))

class Pat(db.Model):
    __tablename__ = 'Pat'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    val = db.Column(db.String(250), nullable=False)

class Token(db.Model):
    __tablename__ = 'Token'
    id = db.Column(db.Integer, primary_key=True)
    val = db.Column(db.String(250), nullable=False)
    expiry = db.Column(db.DateTime, nullable=False)
    # --- Relationships --- 
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))

class Friendship(db.Model):
    __tablename__ = 'Friendship'
    id = db.Column(db.Integer, primary_key=True)
    # --- Relationships --- 
    uid = db.Column(db.Integer, db.ForeignKey('Users.id'))
    fid = db.Column(db.Integer, db.ForeignKey('Users.id'))

class Mail_log(db.Model):
    __tablename__ = 'Mail_log'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    # --- Relationships --- 
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
