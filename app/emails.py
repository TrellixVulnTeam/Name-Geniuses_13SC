from flask.ext.mail import Message
from app import mail, app
from threading import Thread
from .decorators import async
from flask import render_template

@async
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=app.config['MAIL_USERNAME']
    )
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()

def newemailsignup(email):
    html=render_template('newregnotification.html', email=email)
    send_email(to="dalec@namegeniuses.com", subject = "New registration",template=html )