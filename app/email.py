import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import current_app

class Mail:
    def __init__(self, to, subject, body):
        self.to = to
        self.subject = subject
        self.body = body
        self.email = current_app.config["EMAIL_ADRESS"]
        self.password = current_app.config["EMAIL_PASSWORD"]
        self.SMTP_SERVER = "smtp.gmail.com"
        self.SMTP_PORT = 587
        self.msg = None

    def mail_config(self):
        self.msg = MIMEMultipart()
        self.msg["From"] = self.email
        self.msg["To"] = self.to
        self.msg["Subject"] = self.subject

        self.msg.attach(MIMEText(self.body, "plain"))

    def server_connection(self):
        try:
            with smtplib.SMTP(self.SMTP_SERVER, self.SMTP_PORT) as server:
                server.starttls()
                server.login(self.email, self.password)
                server.sendmail(self.email, self.to, self.msg.as_string())
            
            return "Mail sended succesfully via Gmail SMTP server !"
        except Exception as e:
            return f"An error ocurred : {e}"
        
    def send_mail(self):
        self.mail_config()
        response = self.server_connection()
        return response
    

"""
Example of use:

mail = Mail(
    'user@gmail.com',
    'Quantim',
    'Using Quantim is a good idea because it lets you organize your daily tasks'
)
r = mail.send_mail()
print(r)
"""