import pronotepy, datetime, colorist
# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
from flask import current_app
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
# from routes import app
from colorist import hex

"""client = pronotepy.Client(
        'https://pronote.fis.edu.hk/eleve.html',
        username=input("Username:"),
        password=input("Password:"),
    )
homeworks = client.homework(date_from=datetime.date(2025, 3, 1))
for i in homeworks:
    hex(f"{i.subject.name} :", i.background_color)
    print(f"\x1b[4m	Pour: {i.date}\x1b[24m")
    print(f"{i.description}")
    print()

pdf_link = client.generate_timetable_pdf(datetime.date(2025, 3, 2))
print(pdf_link)"""

"""with app.app_context():
    message = Mail(
        from_email='from_email@example.com',
        to_emails='to@example.com',
        subject='Sending with Twilio SendGrid is Fun',
        html_content='<strong>and easy to do anywhere, even with Python</strong>')
    sg = SendGridAPIClient(current_app.config["SENDGRID_API_KEY"])
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)"""

import smtplib, ssl

port = 465  # For SSL
smtp_server = "quantix.pythonanywhere.com"
sender_email = "quentin16666@gmail.com"  # Enter your address
receiver_email = "quentinbardes.perso@gmail.com"  # Enter receiver address
password = input("Type your password and press enter: ")
message = """\
Subject: Hi there

This message is sent from Python."""

context = ssl.create_default_context()
with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message)