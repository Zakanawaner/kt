import re

from flask import current_app, render_template
from flask_mail import Message

from database import Player


def sendWeeklyMail():
    mailManager = current_app.config['mailManager']
    sender = current_app.config['MAIL_USERNAME']
    for recipient in Player.query.filter_by(subscribed=True).filter_by(allowSharing=True).all():
        if recipient.email:
            msg = Message(
                "Your weekly Kill Team Data",
                sender=sender,
                recipients=[recipient.email]
            )
            body = render_template('weeklyMailTemplate.html', username=recipient.username)
            msg.html = body
            mailManager.send(msg)


def subscribeUser(pl, form):
    if 'email' in form.keys():
        if checkEmail(form['email']):
            pl.subscribed = True
            pl.email = form['email']
            current_app.config['database'].session.add(pl)
            current_app.config['database'].session.commit()
            sendSubConfirmation(pl)
            return True
    return False


def sendSubConfirmation(pl):
    msg = Message(
        "Thanks for subscribe!",
        sender=current_app.config['MAIL_USERNAME'],
        recipients=[pl.email]
    )
    body = render_template('subConfirmationMailTemplate.html', username=pl.username)
    msg.html = body
    current_app.config['mailManager'].send(msg)


def unSubscribeUser(pl):
    pl.subscribed = False
    old_email = pl.email
    pl.email = None
    current_app.config['database'].session.add(pl)
    current_app.config['database'].session.commit()
    sendUnSubConfirmation(pl, old_email)
    return True


def sendUnSubConfirmation(pl, email):
    msg = Message(
        "Unsubscribed",
        sender=current_app.config['MAIL_USERNAME'],
        recipients=[email]
    )
    body = render_template('unSubConfirmationMailTemplate.html', username=pl.username)
    msg.html = body
    current_app.config['mailManager'].send(msg)


def checkEmail(email):
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    return re.search(regex, email)
