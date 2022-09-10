import json
import secrets
import names
import os

from flask import current_app
from database import db
from bpAuth import loginManager, jwt
from bpSched import scheduler
from bpMail import mailManager
from bpI18n import babel

from utils.dataHandlers import *
from utils.decorators import *
from utils.auth import *
from utils.faction import *
from utils.mission import *
from utils.player import *
from utils.games import *
from utils.secondary import *
from utils.general import *
from utils.cardGenerator import *
from utils.twitter import *
# from utils.mathHammer import * TODO


################
# APP Function #
def createApp(app):
    config = json.load(open("secret/config.json"))

    app.config["SECRET_KEY"] = handleSecretKey()
    app.config['PORT'] = config['port']
    app.config['HOST'] = config['host']

    app.config["JWT_SECRET_KEY"] = handleSecretKey()
    app.config["JWT_TOKEN_LOCATION"] = ["cookies"]

    app.config["SQLALCHEMY_DATABASE_URI"] = config['db-uri']
    app.config["SQLALCHEMY_BINDS"] = {'db_uri_2': config['db-uri-2']}

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = config['mail']
    app.config['MAIL_PASSWORD'] = config['mail-pass']
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_ASCII_ATTACHMENTS'] = True

    app.config['BABEL_TRANSLATION_DIRECTORIES'] = 'languages'

    mailManager.init_app(app)
    app.config['mailManager'] = mailManager
    scheduler.init_app(app)
    app.config["scheduler"] = scheduler
    loginManager.init_app(app)
    app.config["loginManager"] = loginManager
    jwt.init_app(app)
    app.config["jwt"] = jwt
    db.init_app(app)
    app.config["database"] = db
    babel.init_app(app)
    app.config["babel"] = babel

    app.config['twitterClient'] = TwitterClient()
    app.config["cardGenerator"] = CardGenerator()
    # app.config['mathHammer'] = MathHammer() TODO
    app.config["dataManager"] = json.load(open("hard/data.json"))

    return app


def createDatabase(app):
    with app.app_context():
        if os.path.exists('database.txt'):
            pass
        else:
            createTables(app.config['database'])
            file = open('database.txt', 'w')
            file.write("Database Created")
            file.close()


###################
# Admin functions #
def randomize_data():
    factions = [
        "Space Marines",
        "Grey Knights",
        "Imperial Guard",
        "Veteran Guard",
        "Forge World",
        "Hunter Clade",
        "Ecclesiarchy",
        "Talons of the Emperor",
        "Traitor Space Marines",
        "Death Guard",
        "Thousand Sons",
        "Chaos Daemons",
        "Craftworlds",
        "Commorites",
        "Troupe",
        "Greenskins",
        "Kommandos",
        "Tomb World",
        "Hunter Cadre",
        "Cadre Mercenary",
        "Hive Fleet",
        "Brood Coven",
    ]
    secondaries = [
        "Headhunter",
        "Challenge",
        "Rout",
        "Execution",
        "Deadly Marksman",
        "Rob and Ransack",
        "Seize Ground",
        "Hold the Line",
        "Protect Assets",
        "Damage Limitation",
        "Plant Banner",
        "Central Control",
        "Capture Hostage and Infiltrate",
        "Behind Enemy Lines",
        "Upload Viral Code",
        "Implant",
        "Sabotage",
        "Interloper",
        "Mark Target",
        "Triangulate",
        "Vantage",
        "Retrieval",
        "Overrun"
    ]
    tournaments = [
        'Open play',
        'Matched play',
        'Narrative play'
    ]
    players = [names.get_full_name() for i in range(0, 3)]
    players.append('mariofelectronica')
    for i in range(0, 10):
        d = random.randint(int(time.time()) - 31556926, int(time.time()) + 31556926)
        datetime.fromtimestamp(d)
        ok = False
        while not ok:
            playersName = [random.choice(players), random.choice(players)]
            if playersName[0] != playersName[1]:
                ok = True
        ok = False
        while not ok:
            secondaries0 = [random.choice(secondaries), random.choice(secondaries), random.choice(secondaries)]
            if secondaries0[0] != secondaries0[1] != secondaries0[2]:
                ok = True
        ok = False
        while not ok:
            secondaries1 = [random.choice(secondaries), random.choice(secondaries), random.choice(secondaries)]
            if secondaries1[0] != secondaries1[1] != secondaries1[2]:
                ok = True
        response = {
            'tournament': random.choice(tournaments),
            'gameType': random.choice(tournaments),
            'edition': random.choice(["KT 2021 - Open", "KT 2022 - Into the Dark"]),
            'timestamp': int(time.time()) - 31556926 + i,
            'mission': random.choice([
                {
                    "code": 1.1,
                    "name": "Loot and Salvage",
                },
                {
                    "code": 1.2,
                    "name": "Consecration",
                },
                {
                    "code": 1.3,
                    "name": "Awaken the data Spirits",
                },
                {
                    "code": 2.1,
                    "name": "Escalating Hostilities",
                },
                {
                    "code": 2.2,
                    "name": "Seize Ground",
                },
                {
                    "code": 2.3,
                    "name": "Domination",
                },
                {
                    "code": 3.1,
                    "name": "Secure Archeotech",
                },
                {
                    "code": 3.2,
                    "name": "Duel of wits",
                },
                {
                    "code": 3.3,
                    "name": "Master the terminals",
                },
            ]),
            'rollOffWinner': random.choice(playersName),
            'rollOffWinnerSelection': random.choice(["attacker", "defender"]),
            playersName[0]: {
                'steamId': '76561198294376529' if playersName[0] == 'mariofelectronica' else 0,
                'initiative': [random.choice([True, False]),
                               random.choice([True, False]),
                               random.choice([True, False]),
                               random.choice([True, False])],
                'scouting': random.choice(["Fortify", "Infiltrate", "Recon"]),
                'faction': random.choice(factions) if playersName[0] != '1003' else random.choice(
                    ["Forge World", "Death Guard"]),
                'primaries': {
                    'first': random.randint(0, 4),
                    'second': random.randint(0, 4),
                    'third': random.randint(0, 4),
                    'fourth': random.randint(0, 4),
                },
                'secondaries': {
                    'first': {
                        'name': secondaries0[0],
                        'score': random.randint(0, 2),
                        'first': 0,
                        'second': 0,
                        'third': 0,
                        'fourth': 0,
                    },
                    'second': {
                        'name': secondaries0[1],
                        'score': random.randint(0, 2),
                        'first': 0,
                        'second': 0,
                        'third': 0,
                        'fourth': 0,
                    },
                    'third': {
                        'name': secondaries0[2],
                        'score': random.randint(0, 2),
                        'first': 0,
                        'second': 0,
                        'third': 0,
                        'fourth': 0,
                    },
                }
            },
            playersName[1]: {
                'steamId': '76561198294376529' if playersName[1] == 'mariofelectronica' else 0,
                'initiative': [random.choice([True, False]),
                               random.choice([True, False]),
                               random.choice([True, False]),
                               random.choice([True, False])],
                'scouting': random.choice(["Fortify", "Infiltrate", "Recon"]),
                'faction': random.choice(factions) if playersName[1] != '1003' else random.choice(
                    ["Forge World", "Death Guard"]),
                'primaries': {
                    'first': random.randint(0, 4),
                    'second': random.randint(0, 4),
                    'third': random.randint(0, 4),
                    'fourth': random.randint(0, 4),
                },
                'secondaries': {
                    'first': {
                        'name': secondaries1[0],
                        'score': random.randint(0, 2),
                        'first': 0,
                        'second': 0,
                        'third': 0,
                        'fourth': 0,
                    },
                    'second': {
                        'name': secondaries1[1],
                        'score': random.randint(0, 2),
                        'first': 0,
                        'second': 0,
                        'third': 0,
                        'fourth': 0,
                    },
                    'third': {
                        'name': secondaries1[2],
                        'score': random.randint(0, 2),
                        'first': 0,
                        'second': 0,
                        'third': 0,
                        'fourth': 0,
                    },
                }
            }
        }
        response[playersName[0]]['primaries']['total'] = response[playersName[0]]['primaries']['first'] + \
                                                         response[playersName[0]]['primaries']['second'] + \
                                                         response[playersName[0]]['primaries']['third'] + \
                                                         response[playersName[0]]['primaries']['fourth']
        response[playersName[1]]['primaries']['total'] = response[playersName[1]]['primaries']['first'] + \
                                                         response[playersName[1]]['primaries']['second'] + \
                                                         response[playersName[1]]['primaries']['third'] + \
                                                         response[playersName[1]]['primaries']['fourth']
        response[playersName[0]]['secondaries']['total'] = response[playersName[0]]['secondaries']['first']['score'] + \
                                                           response[playersName[0]]['secondaries']['second']['score'] + \
                                                           response[playersName[0]]['secondaries']['third']['score']
        response[playersName[1]]['secondaries']['total'] = response[playersName[1]]['secondaries']['first']['score'] + \
                                                           response[playersName[1]]['secondaries']['second']['score'] + \
                                                           response[playersName[1]]['secondaries']['third']['score']
        response[playersName[0]]['total'] = response[playersName[0]]['primaries']['total'] + \
                                            response[playersName[0]]['secondaries']['total']
        response[playersName[1]]['total'] = response[playersName[1]]['primaries']['total'] + \
                                            response[playersName[1]]['secondaries']['total']
        if response[playersName[1]]['total'] > response[playersName[0]]['total']:
            response['winner'] = playersName[1]
            response['loser'] = playersName[0]
            response['tie'] = False
        elif response[playersName[1]]['total'] < response[playersName[0]]['total']:
            response['winner'] = playersName[0]
            response['loser'] = playersName[1]
            response['tie'] = False
        else:
            response['winner'] = playersName[0]
            response['loser'] = playersName[1]
            response['tie'] = True

        return handleGameData(response, current_app.config['database'])
    return None


def addNewUpdate(form):
    if not Update.query.filter_by(name=form['name']).first():
        lastUpd = Update.query.filter(Update.date < datetime.strptime(form['date'], '%Y-%m-%d')).order_by(desc(Update.date)).first()
        upd = Update(
            name=form['name'],
            date=datetime.strptime(form['date'], '%Y-%m-%d'),
            dateEnd=datetime.strptime('3000-01-01', '%Y-%m-%d'),
            factionAffected=form['faction'],
            description=form['desc'],
        )
        lastUpd.dateEnd = datetime.strptime(form['date'], '%Y-%m-%d')
        db.session.add(lastUpd)
        db.session.add(upd)
        db.session.commit()


def getUpdates():
    upd = Update.query.order_by(desc(Update.date)).all()
    return upd


def handleSecretKey():
    keys = json.load(open("secret/config.json"))
    if keys['secret-key']:
        return keys['secret-key']
    else:
        key = secrets.token_hex(16)
        keys['secret-key'] = key
        json.dump(keys, open("secret/config.json", 'w'), indent=4)
        return key
