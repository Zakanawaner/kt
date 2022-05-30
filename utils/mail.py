import re

from flask import current_app, render_template
from flask_mail import Message

from database import Player, Game, GameType
from datetime import datetime, timedelta


def sendWeeklyMail():
    mailManager = current_app.config['mailManager']
    data = current_app.config['dataManager']
    sender = current_app.config['MAIL_USERNAME']

    openPlay = GameType.query.filter_by(name=data['gameType']['open']).first()
    matchedPlay = GameType.query.filter_by(name=data['gameType']['matched']).first()
    narrativePlay = GameType.query.filter_by(name=data['gameType']['narrative']).first()
    games = {
        'open': Game.query.filter_by(gameType=openPlay.id).filter(
            Game.date >= datetime.now() - timedelta(days=7)).all() if openPlay else [],
        'matched': Game.query.filter_by(gameType=matchedPlay.id).filter(
            Game.date >= datetime.now() - timedelta(days=7)).all() if matchedPlay else [],
        'narrative': Game.query.filter_by(gameType=narrativePlay.id).filter(
            Game.date >= datetime.now() - timedelta(days=7)).all() if narrativePlay else [],
    }
    factionsOpen = {}
    for game in games['open']:
        if not game.tie:
            if game.winFaction[0].shortName in factionsOpen.keys():
                factionsOpen[game.winFaction[0].shortName]['wins'] += 1
            else:
                factionsOpen[game.winFaction[0].shortName] = {
                    'wins': 1,
                    'loses': 0,
                    'ties': 0,
                    'name': game.winFaction[0].name
                }
            if game.losFaction[0].shortName in factionsOpen.keys():
                factionsOpen[game.losFaction[0].shortName]['loses'] += 1
            else:
                factionsOpen[game.losFaction[0].shortName] = {
                    'wins': 0,
                    'loses': 1,
                    'ties': 0,
                    'name': game.losFaction[0].name
                }
        else:
            if game.winFaction[0].shortName in factionsOpen.keys():
                factionsOpen[game.winFaction[0].shortName]['ties'] += 1
            else:
                factionsOpen[game.winFaction[0].shortName] = {
                    'wins': 0,
                    'loses': 0,
                    'ties': 1,
                    'name': game.winFaction[0].name
                }
            if game.losFaction[0].shortName in factionsOpen.keys():
                factionsOpen[game.losFaction[0].shortName]['loses'] += 1
            else:
                factionsOpen[game.losFaction[0].shortName] = {
                    'wins': 0,
                    'loses': 0,
                    'ties': 1,
                    'name': game.losFaction[0].name
                }
    factionsMatched = {}
    for game in games['matched']:
        if not game.tie:
            if game.winFaction[0].shortName in factionsMatched.keys():
                factionsMatched[game.winFaction[0].shortName]['wins'] += 1
            else:
                factionsMatched[game.winFaction[0].shortName] = {
                    'wins': 1,
                    'loses': 0,
                    'ties': 0,
                    'name': game.winFaction[0].name
                }
            if game.losFaction[0].shortName in factionsMatched.keys():
                factionsMatched[game.losFaction[0].shortName]['loses'] += 1
            else:
                factionsMatched[game.losFaction[0].shortName] = {
                    'wins': 0,
                    'loses': 1,
                    'ties': 0,
                    'name': game.losFaction[0].name
                }
        else:
            if game.winFaction[0].shortName in factionsMatched.keys():
                factionsMatched[game.winFaction[0].shortName]['ties'] += 1
            else:
                factionsMatched[game.winFaction[0].shortName] = {
                    'wins': 0,
                    'loses': 0,
                    'ties': 1,
                    'name': game.winFaction[0].name
                }
            if game.losFaction[0].shortName in factionsMatched.keys():
                factionsMatched[game.losFaction[0].shortName]['loses'] += 1
            else:
                factionsMatched[game.losFaction[0].shortName] = {
                    'wins': 0,
                    'loses': 0,
                    'ties': 1,
                    'name': game.losFaction[0].name
                }
    factionsNarrative = {}
    for game in games['narrative']:
        if not game.tie:
            if game.winFaction[0].shortName in factionsNarrative.keys():
                factionsNarrative[game.winFaction[0].shortName]['wins'] += 1
            else:
                factionsNarrative[game.winFaction[0].shortName] = {
                    'wins': 1,
                    'loses': 0,
                    'ties': 0,
                    'name': game.winFaction[0].name
                }
            if game.losFaction[0].shortName in factionsNarrative.keys():
                factionsNarrative[game.losFaction[0].shortName]['loses'] += 1
            else:
                factionsNarrative[game.losFaction[0].shortName] = {
                    'wins': 0,
                    'loses': 1,
                    'ties': 0,
                    'name': game.losFaction[0].name
                }
        else:
            if game.winFaction[0].shortName in factionsNarrative.keys():
                factionsNarrative[game.winFaction[0].shortName]['ties'] += 1
            else:
                factionsNarrative[game.winFaction[0].shortName] = {
                    'wins': 0,
                    'loses': 0,
                    'ties': 1,
                    'name': game.winFaction[0].name
                }
            if game.losFaction[0].shortName in factionsNarrative.keys():
                factionsNarrative[game.losFaction[0].shortName]['loses'] += 1
            else:
                factionsNarrative[game.losFaction[0].shortName] = {
                    'wins': 0,
                    'loses': 0,
                    'ties': 1,
                    'name': game.losFaction[0].name
                }
    factions = {
        'open': factionsOpen,
        'matched': factionsMatched,
        'narrative': factionsNarrative
    }
    for gt in factions.keys():
        for fct in factions[gt].keys():
            wins = factions[gt][fct]['wins']
            loses = factions[gt][fct]['loses']
            ties = factions[gt][fct]['ties']
            try:
                factions[gt][fct]['winRate'] = wins * 100 / (wins + loses + ties)
                factions[gt][fct]['loseRate'] = loses * 100 / (wins + loses + ties)
                factions[gt][fct]['tieRate'] = ties * 100 / (wins + loses + ties)
            except ZeroDivisionError:
                factions[gt][fct]['winRate'] = 0
                factions[gt][fct]['loseRate'] = 0
                factions[gt][fct]['tieRate'] = 0
    factions['open'] = dict(sorted(factions['open'].items(), key=lambda item: item[1]['winRate'], reverse=True))
    factions['matched'] = dict(sorted(factions['matched'].items(), key=lambda item: item[1]['winRate'], reverse=True))
    factions['narrative'] = dict(sorted(factions['narrative'].items(), key=lambda item: item[1]['winRate'], reverse=True))
    for recipient in Player.query.filter_by(subscribed=True).filter_by(allowSharing=True).all():
        if recipient.email:
            msg = Message(
                "Your weekly Kill Team Data",
                sender=sender,
                recipients=[recipient.email]
            )
            body = render_template('weeklyMailTemplate.html', username=recipient.username, games=games, factions=factions)
            msg.html = body
            mailManager.send(msg)
    return games, factions


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
