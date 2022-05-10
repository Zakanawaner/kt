import json
import secrets
import random
import names
import os

from database import db
from bpAuth import loginManager, jwt
from bpSched import scheduler
from bpMail import mailManager

from utils.dataHandlers import *
from utils.decorators import *
from utils.auth import *
from utils.faction import *
from utils.mission import *
from utils.player import *
from utils.games import *
from utils.secondary import *
from utils.general import *


################
# APP Function #
def createApp(app):
    app.config["SECRET_KEY"] = handleSecretKey()

    app.config["JWT_SECRET_KEY"] = handleSecretKey()
    app.config["JWT_TOKEN_LOCATION"] = ["cookies"]

    app.config["SQLALCHEMY_DATABASE_URI"] = json.load(open("secret/keys.json"))['db-dev-uri']
    # app.config["SQLALCHEMY_DATABASE_URI"] = json.load(open("secret/keys.json"))['db-prod-uri']
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = json.load(open("secret/keys.json"))['mail']
    app.config['MAIL_PASSWORD'] = json.load(open("secret/keys.json"))['mail-pass']
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_ASCII_ATTACHMENTS'] = True

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

    return app


def createDatabase(app):
    with app.app_context():
        if os.path.exists('database.txt'):
            pass
        else:
            createTables(db)
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
    factions = [
        "Space Marines",
        "Grey Knights",
        "Imperial Guard",
        "Veteran Guard",
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
    secondaries = [
        "Headhunter",
        "Challenge",
        "Rout",
        "Execution",
        "Deadly Marksman",
        "Rob and Ransack",
    ]
    tournaments = [
        'Open play',
        'Matched play',
        'Narrative play'
    ]
    players = [names.get_full_name() for i in range(0, 3)]
    players.append('mariofelectronica')
    for i in range(0, 400):
        d = random.randint(int(time.time()), int(time.time()) + 31556926)
        datetime.fromtimestamp(d)
        ok = False
        while not ok:
            playersName = [random.choice(players), random.choice(players)]
            if playersName[0] != playersName[1]:
                ok = True
        response = {
            'tournament': random.choice(tournaments),
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
                        'name': random.choice(secondaries),
                        'score': random.randint(0, 2),
                        'first': 0,
                        'second': 0,
                        'third': 0,
                        'fourth': 0,
                    },
                    'second': {
                        'name': random.choice(secondaries),
                        'score': random.randint(0, 2),
                        'first': 0,
                        'second': 0,
                        'third': 0,
                        'fourth': 0,
                    },
                    'third': {
                        'name': random.choice(secondaries),
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
                        'name': random.choice(secondaries),
                        'score': random.randint(0, 2),
                        'first': 0,
                        'second': 0,
                        'third': 0,
                        'fourth': 0,
                    },
                    'second': {
                        'name': random.choice(secondaries),
                        'score': random.randint(0, 2),
                        'first': 0,
                        'second': 0,
                        'third': 0,
                        'fourth': 0,
                    },
                    'third': {
                        'name': random.choice(secondaries),
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

        response = handleFactions(db, response, 'winner')
        response = handleFactions(db, response, 'loser')
        response = handleSecondaries(db, response, 'winner')
        response = handleSecondaries(db, response, 'loser')
        response = handleMission(db, response)
        response = handleTournament(db, response)

        game = Game(
            date=datetime.fromtimestamp(d),
            timestamp=response['timestamp'],
            tournament=response['tournament'].id,
            mission=[response['mission']] if response['mission'] else [],
            initFirst=[response[response['winner']]['faction']] if response[response['winner']]['initiative'][0] else [
                response[response['loser']]['faction']],
            initSecond=[response[response['winner']]['faction']] if response[response['winner']]['initiative'][1] else [
                response[response['loser']]['faction']],
            initThird=[response[response['winner']]['faction']] if response[response['winner']]['initiative'][2] else [
                response[response['loser']]['faction']],
            initFourth=[response[response['winner']]['faction']] if response[response['winner']]['initiative'][3] else [
                response[response['loser']]['faction']],
            winner=response['winner'],
            winnerId=response[response['winner']]['steamId'],
            winFaction=[response[response['winner']]['faction']] if response[response['winner']]['faction'] else [],
            winScouting=response[response['winner']]['scouting'],
            winTotal=response[response['winner']]['total'],
            winPrimary=response[response['winner']]['primaries']['total'],
            winPrimaryFirst=response[response['winner']]['primaries']['first'],
            winPrimarySecond=response[response['winner']]['primaries']['second'],
            winPrimaryThird=response[response['winner']]['primaries']['third'],
            winPrimaryFourth=response[response['winner']]['primaries']['fourth'],
            winSecondary=response[response['winner']]['secondaries']['total'],
            winSecondaryFirst=[response[response['winner']]['secondaries']['first']['name']],
            winSecondaryFirstScoreTurn1=response[response['winner']]['secondaries']['first']['first'],
            winSecondaryFirstScoreTurn2=response[response['winner']]['secondaries']['first']['second'],
            winSecondaryFirstScoreTurn3=response[response['winner']]['secondaries']['first']['third'],
            winSecondaryFirstScoreTurn4=response[response['winner']]['secondaries']['first']['fourth'],
            winSecondaryFirstScore=response[response['winner']]['secondaries']['first']['score'],
            winSecondarySecond=[response[response['winner']]['secondaries']['second']['name']],
            winSecondarySecondScoreTurn1=response[response['winner']]['secondaries']['second']['first'],
            winSecondarySecondScoreTurn2=response[response['winner']]['secondaries']['second']['second'],
            winSecondarySecondScoreTurn3=response[response['winner']]['secondaries']['second']['third'],
            winSecondarySecondScoreTurn4=response[response['winner']]['secondaries']['second']['fourth'],
            winSecondarySecondScore=response[response['winner']]['secondaries']['second']['score'],
            winSecondaryThird=[response[response['winner']]['secondaries']['third']['name']],
            winSecondaryThirdScoreTurn1=response[response['winner']]['secondaries']['third']['first'],
            winSecondaryThirdScoreTurn2=response[response['winner']]['secondaries']['third']['second'],
            winSecondaryThirdScoreTurn3=response[response['winner']]['secondaries']['third']['third'],
            winSecondaryThirdScoreTurn4=response[response['winner']]['secondaries']['third']['fourth'],
            winSecondaryThirdScore=response[response['winner']]['secondaries']['third']['score'],
            loser=response['loser'],
            loserId=response[response['loser']]['steamId'],
            losFaction=[response[response['loser']]['faction']] if response[response['loser']]['faction'] else [],
            losScouting=response[response['loser']]['scouting'],
            losTotal=response[response['loser']]['total'],
            losPrimary=response[response['loser']]['primaries']['total'],
            losPrimaryFirst=response[response['loser']]['primaries']['first'],
            losPrimarySecond=response[response['loser']]['primaries']['second'],
            losPrimaryThird=response[response['loser']]['primaries']['third'],
            losPrimaryFourth=response[response['loser']]['primaries']['fourth'],
            losSecondary=response[response['loser']]['secondaries']['total'],
            losSecondaryFirst=[response[response['loser']]['secondaries']['first']['name']],
            losSecondaryFirstScoreTurn1=response[response['loser']]['secondaries']['first']['first'],
            losSecondaryFirstScoreTurn2=response[response['loser']]['secondaries']['first']['second'],
            losSecondaryFirstScoreTurn3=response[response['loser']]['secondaries']['first']['third'],
            losSecondaryFirstScoreTurn4=response[response['loser']]['secondaries']['first']['fourth'],
            losSecondaryFirstScore=response[response['loser']]['secondaries']['first']['score'],
            losSecondarySecond=[response[response['loser']]['secondaries']['second']['name']],
            losSecondarySecondScoreTurn1=response[response['loser']]['secondaries']['second']['first'],
            losSecondarySecondScoreTurn2=response[response['loser']]['secondaries']['second']['second'],
            losSecondarySecondScoreTurn3=response[response['loser']]['secondaries']['second']['third'],
            losSecondarySecondScoreTurn4=response[response['loser']]['secondaries']['second']['fourth'],
            losSecondarySecondScore=response[response['loser']]['secondaries']['second']['score'],
            losSecondaryThird=[response[response['loser']]['secondaries']['third']['name']],
            losSecondaryThirdScoreTurn1=response[response['loser']]['secondaries']['third']['first'],
            losSecondaryThirdScoreTurn2=response[response['loser']]['secondaries']['third']['second'],
            losSecondaryThirdScoreTurn3=response[response['loser']]['secondaries']['third']['third'],
            losSecondaryThirdScoreTurn4=response[response['loser']]['secondaries']['third']['fourth'],
            losSecondaryThirdScore=response[response['loser']]['secondaries']['third']['score'],
            rollOffWinner=[
                response[response['rollOffWinner']]['faction']] if 'rollOffWinner' in response.keys() else [],
            rollOffSelection=response['rollOffWinnerSelection'] if 'rollOffWinnerSelection' in response.keys() else '',
            tie=response['tie']
        )
        response['tournament'].games.append(game)
        if response['tie']:
            response[response['winner']]['faction'].gamesTied.append(game)
            if response[response['winner']]['faction'] != response[response['loser']]['faction']:
                response[response['loser']]['faction'].gamesTied.append(game)
        else:
            response[response['winner']]['faction'].gamesWon.append(game)
            response[response['loser']]['faction'].gamesLost.append(game)
        db.session.add(response[response['winner']]['faction'])
        db.session.add(response[response['loser']]['faction'])
        db.session.add(response['tournament'])
        db.session.add(game)
        db.session.commit()


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
    upd.append((Update(id=0, name="All Time", date=datetime.fromtimestamp(0))))
    return upd


def handleSecretKey():
    keys = json.load(open("secret/keys.json"))
    if keys['secret-key']:
        return keys['secret-key']
    else:
        key = secrets.token_hex(16)
        keys['secret-key'] = key
        json.dump(keys, open("secret/keys.json", 'w'), indent=4)
        return key

