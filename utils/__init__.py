from database import (
    Game, Player, Mission, Rank, Secondary, Faction, Tournament,
    WinRates, MissionRates, SecondaryRates, PlayerMissionRates,
    PlayerWinRates, PlayerWinRatesPlayer, PlayerSecondaryRates,
    PlayerWinRatesAgainst, Operative, Update)
from sqlalchemy import extract, desc, asc, or_
from datetime import datetime
from collections import OrderedDict
from password_strength import PasswordPolicy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user
from functools import wraps
import random
import time
import operator
import names
import uuid
import os


##############
# Decorators #
def only_admin(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.permissions >= 8:
            return func(*args, **kwargs)
    return decorated_view


def only_collaborator(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.permissions >= 7:
            return func(*args, **kwargs)
    return decorated_view


def only_tier6(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.permissions >= 6:
            return func(*args, **kwargs)
    return decorated_view


def only_tier5(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.permissions >= 5:
            return func(*args, **kwargs)
    return decorated_view


def only_tier4(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.permissions >= 4:
            return func(*args, **kwargs)
    return decorated_view


def only_tier3(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.permissions >= 3:
            return func(*args, **kwargs)
    return decorated_view


def only_tier2(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.permissions >= 2:
            return func(*args, **kwargs)
    return decorated_view


def only_tier1(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.permissions >= 1:
            return func(*args, **kwargs)
    return decorated_view


########
# Auth #
def userSignup(db, form):
    if form['password'] == form['password1']:
        policy = PasswordPolicy.from_names(
            length=8,
            uppercase=1,
            numbers=1
        )
        if policy.test(form['password']):
            return 401, None
        hashed_password = generate_password_hash(form['password'], method='sha256')
        if Player.query.filter_by(username=form['username']).first():
            return 402, None
        new_user = Player(publicId=str(uuid.uuid4()),
                          username=form['username'],
                          password=hashed_password,
                          shortName=form['username'].lower().replace(" ", ""),
                          permissions=8 if form['username'] == 'Zakanawaner' else 0,
                          steamLink=False,
                          allowSharing=True,
                          rank=[Rank.query.filter(Rank.score <= 0).first()],
                          score=0,
                          wins=0,
                          ties=0,
                          loses=0)
        db.session.add(new_user)
        db.session.commit()
        return 200, new_user
    else:
        return 403, None


def userLogin(form):
    user = Player.query.filter_by(username=form['username']).first()
    if user:
        if check_password_hash(user.password, form['password']):
            return 200, user
    return 401, None


#####################
# Raw data Handlers #
def handlePlayers(db, response, opt):
    if not Player.query.filter_by(username=response[opt]).first():
        player = Player(
            username=response[opt],
            steamId=response[response[opt]]['steamId'],
            shortName=response[opt].lower().replace(' ', ''),
            score=response[response[opt]]['total'],
            rank=[Rank.query.filter(Rank.score < response[response[opt]]['total']).first()],
            wins=1 if not response['tie'] and opt == "winner" else 0,
            ties=1 if response['tie'] else 0,
            loses=1 if not response['tie'] and opt == "loser" else 0,
        )
    else:
        player = Player.query.filter_by(username=response[opt]).first()
        player.score += response[response[opt]]['total']
        for r in Rank.query.all():
            if player.score > r.score:
                player.rank = [r]
            else:
                break
        player.wins += 1 if not response['tie'] and opt == "winner" else 0
        player.loses += 1 if not response['tie'] and opt == "loser" else 0
        player.ties += 1 if response['tie'] else 0
    db.session.add(player)
    db.session.commit()
    return player


def handleFactions(db, response, opt):
    if 'faction' in response[response[opt]].keys():
        if not Faction.query.filter_by(name=response[response[opt]]['faction']).first():
            faction = Faction(name=response[response[opt]]['faction'],
                              shortName=response[response[opt]]['faction'].lower().replace(' ', ''))
        else:
            faction = Faction.query.filter_by(name=response[response[opt]]['faction']).first()
    else:
        faction = None
    response[response[opt]]['faction'] = faction
    db.session.add(response[response[opt]]['faction']) if response[response[opt]]['faction'] else None
    db.session.commit()
    return response


def handleMission(db, response):
    if 'mission' in response.keys():
        if not Mission.query.filter_by(name=response['mission']['name']).first():
            mission = Mission(name=response['mission']['name'],
                              shortName=response['mission']['name'].lower().replace(' ', ''),
                              code=response['mission']['code'])
        else:
            mission = Mission.query.filter_by(name=response['mission']['name']).first()
    else:
        mission = None
    response['mission'] = mission
    db.session.add(response['mission']) if response['mission'] else None
    db.session.commit()
    return response


def handleSecondaries(db, response, opt):
    if 'secondaries' in response[response[opt]].keys():
        for sec in response[response[opt]]['secondaries']:
            if type(response[response[opt]]['secondaries'][sec]) is dict:
                response[response[opt]]['secondaries'][sec]['name'] = Secondary(
                    name=response[response[opt]]['secondaries'][sec]['name'],
                    shortName=response[response[opt]]['secondaries'][sec]['name'].lower().replace(' ',
                                                                                                  ''), ) if not Secondary.query.filter_by(
                    name=response[response[opt]]['secondaries'][sec]['name']).first() else Secondary.query.filter_by(
                    name=response[response[opt]]['secondaries'][sec]['name']).first()
                db.session.add(response[response[opt]]['secondaries'][sec]['name'])
    db.session.commit()
    return response


def handleTournament(db, response):
    if 'tournament' in response.keys():
        if not Tournament.query.filter_by(name=response['tournament']).first():
            response['tournament'] = Tournament(name=response['tournament'],
                                                shortName=response['tournament'].lower().replace(' ', ''), )
            db.session.add(response['tournament'])
        else:
            response['tournament'] = Tournament.query.filter_by(name=response['tournament']).first()
    db.session.commit()
    return response


def handleOperatives(db, response, pls):
    for pl in pls:
        if 'operatives' in response[response[pl]].keys():
            for op in response[response[pl]]['operatives'].keys():
                weapons = response[response[pl]]['operatives'][op]['desc'].split('Weapons')[1].split('---')[0].split(
                    '\n')
                melee = []
                ranged = []
                for i, weapon in enumerate(weapons):
                    if weapon == '':
                        if i < len(weapons) - 1:
                            if '[' not in weapons[i + 1]:
                                ranged.append(weapons[i + 1])
                    else:
                        if ']M[' in weapon:
                            melee.append(weapon[weapon.find(' ') + 1:])
                        if ']R[' in weapon:
                            ranged.append(weapon[weapon.find(' ') + 1:])
                name = response[response[pl]]['operatives'][op]['desc'].split('\n')[0]
                response[response[pl]]['operatives'][op]['sql'] = Operative.query.filter_by(name=name).filter_by(
                    melee=','.join(melee)).filter_by(ranged=','.join(ranged)).first()
                if not response[response[pl]]['operatives'][op]['sql']:
                    response[response[pl]]['operatives'][op]['sql'] = Operative(
                        name=name,
                        faction=response[response[pl]]['faction'].id,
                        melee=','.join(melee),
                        ranged=','.join(ranged)
                    )
                    db.session.add(response[response[pl]]['operatives'][op]['sql'])
                    db.session.commit()
    return response


def handleGameData(response, db):
    if checkData(response):
        if not Game.query.filter_by(timestamp=response['timestamp']).first():
            response = handleFactions(db, response, 'winner')
            response = handleFactions(db, response, 'loser')
            response = handleSecondaries(db, response, 'winner')
            response = handleSecondaries(db, response, 'loser')
            response = handleMission(db, response)
            response = handleTournament(db, response)
            response = handleOperatives(db, response, ['winner', 'loser'])

            game = Game(
                date=datetime.now(),
                timestamp=response['timestamp'],
                tournament=response['tournament'].id,
                mission=[response['mission']] if response['mission'] else [],
                initFirst=[response[response['winner']]['faction']] if response[response['winner']]['initiative'][
                    0] else [response[response['loser']]['faction']],
                initSecond=[response[response['winner']]['faction']] if response[response['winner']]['initiative'][
                    1] else [response[response['loser']]['faction']],
                initThird=[response[response['winner']]['faction']] if response[response['winner']]['initiative'][
                    2] else [response[response['loser']]['faction']],
                initFourth=[response[response['winner']]['faction']] if response[response['winner']]['initiative'][
                    3] else [response[response['loser']]['faction']],
                winner=response['winner'],
                winnerId=response[response['winner']]['steamId'],
                winFaction=[response[response['winner']]['faction']] if response[response['winner']]['faction'] else [],
                winOperatives=','.join([str(op['sql'].id) for op in
                                        response[response['winner']]['operatives'].values()]) if 'operatives' in
                                                                                                 response[response[
                                                                                                     'winner']].keys() else '',
                winOpKilled=','.join([str(op['roundKilled']) if op['killed'] else '0' for op in
                                      response[response['winner']]['operatives'].values()]) if 'operatives' in response[
                    response['winner']].keys() else '',
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
                losOperatives=','.join(
                    [str(op['sql'].id) for op in response[response['loser']]['operatives'].values()]) if 'operatives' in
                                                                                                         response[
                                                                                                             response[
                                                                                                                 'loser']].keys() else '',
                losOpKilled=','.join([str(op['roundKilled']) if op['killed'] else '0' for op in
                                      response[response['loser']]['operatives'].values()]) if 'operatives' in response[
                    response['loser']].keys() else '',
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
                rollOffSelection=response[
                    'rollOffWinnerSelection'] if 'rollOffWinnerSelection' in response.keys() else '',
                tie=response['tie']
            )

            if response['tie']:
                response[response['winner']]['faction'].gamesTied.append(game)
                if response[response['winner']]['faction'] != response[response['loser']]['faction']:
                    response[response['loser']]['faction'].gamesTied.append(game)
            else:
                response[response['winner']]['faction'].gamesWon.append(game)
                response[response['loser']]['faction'].gamesLost.append(game)

            db.session.add(response[response['winner']]['faction'])
            db.session.add(response[response['loser']]['faction'])
            if 'tournament' in response.keys():
                response['tournament'].games.append(game)
                db.session.add(response['tournament'])
            db.session.add(game)
            db.session.commit()


def checkData(response):
    template = {
        'mission': {
            "code": 1.1,
            "name": "Loot and Salvage",
            'objGuid': ""
        },
        'rollOffWinner': "",
        'rollOffWinnerSelection': "",
        response['winner']: {
            'steamId': 0,
            'initiative': [],
            'scouting': "",
            'faction': "",
            'primaries': {
                'first': 0,
                'second': 0,
                'third': 0,
                'fourth': 0,
                'total': 0,
            },
            'secondaries': {
                'first': {
                    'name': "",
                    'score': 0,
                    'first': 0,
                    'second': 0,
                    'third': 0,
                    'fourth': 0,
                },
                'second': {
                    'name': "",
                    'score': 0,
                    'first': 0,
                    'second': 0,
                    'third': 0,
                    'fourth': 0,
                },
                'third': {
                    'name': "",
                    'score': 0,
                    'first': 0,
                    'second': 0,
                    'third': 0,
                    'fourth': 0,
                },
                'total': 0,
            }
        },
        response['loser']: {
            'steamId': 0,
            'initiative': [],
            'scouting': "",
            'faction': "",
            'primaries': {
                'first': 0,
                'second': 0,
                'third': 0,
                'fourth': 0,
                'total': 0,
            },
            'secondaries': {
                'first': {
                    'name': "",
                    'score': 0,
                    'first': 0,
                    'second': 0,
                    'third': 0,
                    'fourth': 0,
                },
                'second': {
                    'name': "",
                    'score': 0,
                    'first': 0,
                    'second': 0,
                    'third': 0,
                    'fourth': 0,
                },
                'third': {
                    'name': "",
                    'score': 0,
                    'first': 0,
                    'second': 0,
                    'third': 0,
                    'fourth': 0,
                },
                'total': 0,
            }
        }
    }
    if set(template.keys()) <= set(response.keys()):
        if set(template['mission'].keys()) <= set(response['mission'].keys()) and set(
                template[response['winner']].keys()) <= set(response[response['winner']].keys()) and set(
            template[response['loser']].keys()) <= set(response[response['loser']].keys()):
            if set(template[response['winner']]['primaries'].keys()) <= set(
                    response[response['winner']]['primaries'].keys()) and set(
                template[response['loser']]['primaries'].keys()) <= set(
                response[response['loser']]['primaries'].keys()) and set(
                template[response['winner']]['secondaries'].keys()) <= set(
                response[response['winner']]['secondaries'].keys()) and set(
                template[response['loser']]['secondaries'].keys()) <= set(
                response[response['loser']]['secondaries'].keys()):
                if set(template[response['winner']]['secondaries']['first'].keys()) <= set(
                        response[response['winner']]['secondaries']['first'].keys()) and set(
                    template[response['loser']]['secondaries']['first'].keys()) <= set(
                    response[response['loser']]['secondaries']['first'].keys()) and set(
                    template[response['winner']]['secondaries']['second'].keys()) <= set(
                    response[response['winner']]['secondaries']['second'].keys()) and set(
                    template[response['loser']]['secondaries']['second'].keys()) <= set(
                    response[response['loser']]['secondaries']['second'].keys()) and set(
                    template[response['winner']]['secondaries']['third'].keys()) <= set(
                    response[response['winner']]['secondaries']['third'].keys()) and set(
                    template[response['loser']]['secondaries']['third'].keys()) <= set(
                    response[response['loser']]['secondaries']['third'].keys()):
                    return True
    return False


############
# Database #
def createDatabase(db):
    db.create_all()

    db.session.add(Rank(name="Guardsman", shortName="guardsman", score=0))
    db.session.add(Rank(name="Sergeant", shortName="sergeant", score=50))
    db.session.add(Rank(name="Lieutenant", shortName="lieutenant", score=100))
    db.session.add(Rank(name="Captain", shortName="captain", score=200))
    db.session.add(Rank(name="Major", shortName="major", score=400))
    db.session.add(Rank(name="Colonel", shortName="colonel", score=800))
    db.session.add(Rank(name="Major General", shortName="majorgeneral", score=1600))
    db.session.add(Rank(name="Lieutenant General", shortName="lieutenantgeneral", score=3200))
    db.session.add(Rank(name="Marshall", shortName="marshall", score=6400))
    db.session.add(Rank(name="General", shortName="general", score=12800))
    db.session.add(Rank(name="Lord General", shortName="lordgeneral", score=25600))
    db.session.add(Rank(name="Lord General Militant", shortName="lordgeneralmilitant", score=51200))
    db.session.add(Rank(name="Warmaster", shortName="warmaster", score=102400))
    db.session.add(Rank(name="Lord Commander", shortName="lordcommander", score=204800))

    db.session.add(Update(name="First APP launch",
                          date=datetime.fromtimestamp(int(time.time())),
                          dateEnd=datetime.fromtimestamp(int(time.time()) + 31556926),
                          description="First update dated on the web launch day"))

    db.session.commit()


#########
# Games #
def getGames():
    games = Game.query.all()
    return games


def getGame(gm):
    game = {
        'sql': Game.query.filter_by(id=gm).first(),
    }
    game['winner'] = Player.query.filter_by(allowSharing=True).filter_by(steamId=game['sql'].winnerId).first()
    game['loser'] = Player.query.filter_by(allowSharing=True).filter_by(steamId=game['sql'].loserId).first()
    game['winner'] = game['winner'].username if game['winner'] else "Anonymous"
    game['loser'] = game['loser'].username if game['loser'] else "Anonymous"
    game['tournament'] = Tournament.query.filter_by(id=game['sql'].tournament).first()
    return game


###########
# Players #
def updatePlayers(db):
    for player in Player.query.all():
        updatePlayer(db, player.id)


def updatePlayer(db, pl):
    playerGl = {
        'sql': Player.query.filter_by(id=pl).first(),
        'updates': [],
    }
    playerGl['sql'].gamesWon = []
    playerGl['sql'].gamesLost = []
    playerGl['sql'].gamesTied = []
    playerGl['sql'].wins = 0
    playerGl['sql'].loses = 0
    playerGl['sql'].ties = 0
    if playerGl['sql'].steamLink:
        for update in Update.query.all():
            player = {
                'wins': 0,
                'loses': 0,
                'ties': 0,
                'winnerFactions': {},
                'loserFactions': {},
                'tieFactions': {},
                'winnerFactionsAgainst': {},
                'loserFactionsAgainst': {},
                'tieFactionsAgainst': {},
                'winnerMissions': {},
                'loserMissions': {},
                'tieMissions': {},
                'winnerSecondaries': {},
                'loserSecondaries': {},
                'tieSecondaries': {},
                'winnerPlayers': {},
                'loserPlayers': {},
                'tiePlayers': {}
            }
            for game in Game.query.filter(Game.date >= update.date).filter(Game.date <= (update.dateEnd if update.dateEnd else datetime(3000, 9, 25, 0, 0))).filter_by(winnerId=playerGl['sql'].steamId).all():
                otherPl = Player.query.filter_by(steamId=game.loserId).first()
                if game.tie:
                    playerGl['sql'].gamesTied.append(game)
                    playerGl['sql'].ties += 1
                    player['ties'] += 1
                    if otherPl:
                        if otherPl.username not in player['tiePlayers'].keys():
                            player['tiePlayers'][otherPl.username] = 1
                        else:
                            player['tiePlayers'][otherPl.username] += 1
                    if game.winFaction[0].name not in player['tieFactions'].keys():
                        player['tieFactions'][game.winFaction[0].name] = 1
                    else:
                        player['tieFactions'][game.winFaction[0].name] += 1
                    if game.losFaction[0].name not in player['tieFactionsAgainst'].keys():
                        player['tieFactionsAgainst'][game.losFaction[0].name] = 1
                    else:
                        player['tieFactionsAgainst'][game.losFaction[0].name] += 1
                    if game.mission[0].name not in player['tieMissions'].keys():
                        player['tieMissions'][game.mission[0].name] = 1
                    else:
                        player['tieMissions'][game.mission[0].name] += 1
                    if game.winSecondaryFirst[0].name not in player['tieSecondaries'].keys():
                        player['tieSecondaries'][game.winSecondaryFirst[0].name] = 1
                    else:
                        player['tieSecondaries'][game.winSecondaryFirst[0].name] += 1
                    if game.winSecondarySecond[0].name not in player['tieSecondaries'].keys():
                        player['tieSecondaries'][game.winSecondarySecond[0].name] = 1
                    else:
                        player['tieSecondaries'][game.winSecondarySecond[0].name] += 1
                    if game.winSecondaryThird[0].name not in player['tieSecondaries'].keys():
                        player['tieSecondaries'][game.winSecondaryThird[0].name] = 1
                    else:
                        player['tieSecondaries'][game.winSecondaryThird[0].name] += 1
                else:
                    playerGl['sql'].gamesWon.append(game)
                    playerGl['sql'].wins += 1
                    player['wins'] += 1
                    if otherPl:
                        if otherPl.username not in player['winnerPlayers'].keys():
                            player['winnerPlayers'][otherPl.username] = 1
                        else:
                            player['winnerPlayers'][otherPl.username] += 1
                    if game.winFaction[0].name not in player['winnerFactions'].keys():
                        player['winnerFactions'][game.winFaction[0].name] = 1
                    else:
                        player['winnerFactions'][game.winFaction[0].name] += 1
                    if game.losFaction[0].name not in player['winnerFactionsAgainst'].keys():
                        player['winnerFactionsAgainst'][game.losFaction[0].name] = 1
                    else:
                        player['winnerFactionsAgainst'][game.losFaction[0].name] += 1
                    if game.mission[0].name not in player['winnerMissions'].keys():
                        player['winnerMissions'][game.mission[0].name] = 1
                    else:
                        player['winnerMissions'][game.mission[0].name] += 1
                    if game.winSecondaryFirst[0].name not in player['winnerSecondaries'].keys():
                        player['winnerSecondaries'][game.winSecondaryFirst[0].name] = 1
                    else:
                        player['winnerSecondaries'][game.winSecondaryFirst[0].name] += 1
                    if game.winSecondarySecond[0].name not in player['winnerSecondaries'].keys():
                        player['winnerSecondaries'][game.winSecondarySecond[0].name] = 1
                    else:
                        player['winnerSecondaries'][game.winSecondarySecond[0].name] += 1
                    if game.winSecondaryThird[0].name not in player['winnerSecondaries'].keys():
                        player['winnerSecondaries'][game.winSecondaryThird[0].name] = 1
                    else:
                        player['winnerSecondaries'][game.winSecondaryThird[0].name] += 1
                playerGl['sql'].score += game.winTotal
            for game in Game.query.filter(Game.date >= update.date).filter(Game.date <= (update.dateEnd if update.dateEnd else datetime(3000, 9, 25, 0, 0))).filter_by(loserId=playerGl['sql'].steamId).all():
                otherPl = Player.query.filter_by(steamId=game.winnerId).first()
                if game.tie:
                    playerGl['sql'].gamesTied.append(game)
                    playerGl['sql'].ties += 1
                    player['ties'] += 1
                    if otherPl:
                        if otherPl.username not in player['tiePlayers'].keys():
                            player['tiePlayers'][otherPl.username] = 1
                        else:
                            player['tiePlayers'][otherPl.username] += 1
                    if game.winFaction[0].name not in player['tieFactions'].keys():
                        player['tieFactions'][game.winFaction[0].name] = 1
                    else:
                        player['tieFactions'][game.winFaction[0].name] += 1
                    if game.winFaction[0].name not in player['tieFactionsAgainst'].keys():
                        player['tieFactionsAgainst'][game.winFaction[0].name] = 1
                    else:
                        player['tieFactionsAgainst'][game.winFaction[0].name] += 1
                    if game.mission[0].name not in player['tieMissions'].keys():
                        player['tieMissions'][game.mission[0].name] = 1
                    else:
                        player['tieMissions'][game.mission[0].name] += 1
                    if game.losSecondaryFirst[0].name not in player['tieSecondaries'].keys():
                        player['tieSecondaries'][game.losSecondaryFirst[0].name] = 1
                    else:
                        player['tieSecondaries'][game.losSecondaryFirst[0].name] += 1
                    if game.losSecondarySecond[0].name not in player['tieSecondaries'].keys():
                        player['tieSecondaries'][game.losSecondarySecond[0].name] = 1
                    else:
                        player['tieSecondaries'][game.losSecondarySecond[0].name] += 1
                    if game.losSecondaryThird[0].name not in player['tieSecondaries'].keys():
                        player['tieSecondaries'][game.losSecondaryThird[0].name] = 1
                    else:
                        player['tieSecondaries'][game.losSecondaryThird[0].name] += 1
                else:
                    playerGl['sql'].gamesLost.append(game)
                    playerGl['sql'].loses += 1
                    player['loses'] += 1
                    if otherPl:
                        if otherPl.username not in player['loserPlayers'].keys():
                            player['loserPlayers'][otherPl.username] = 1
                        else:
                            player['loserPlayers'][otherPl.username] += 1
                    if game.losFaction[0].name not in player['loserFactions'].keys():
                        player['loserFactions'][game.losFaction[0].name] = 1
                    else:
                        player['loserFactions'][game.losFaction[0].name] += 1
                    if game.winFaction[0].name not in player['loserFactionsAgainst'].keys():
                        player['loserFactionsAgainst'][game.winFaction[0].name] = 1
                    else:
                        player['loserFactionsAgainst'][game.winFaction[0].name] += 1
                    if game.mission[0].name not in player['loserMissions'].keys():
                        player['loserMissions'][game.mission[0].name] = 1
                    else:
                        player['loserMissions'][game.mission[0].name] += 1
                    if game.losSecondaryFirst[0].name not in player['loserSecondaries'].keys():
                        player['loserSecondaries'][game.losSecondaryFirst[0].name] = 1
                    else:
                        player['loserSecondaries'][game.losSecondaryFirst[0].name] += 1
                    if game.losSecondarySecond[0].name not in player['loserSecondaries'].keys():
                        player['loserSecondaries'][game.losSecondarySecond[0].name] = 1
                    else:
                        player['loserSecondaries'][game.losSecondarySecond[0].name] += 1
                    if game.losSecondaryThird[0].name not in player['loserSecondaries'].keys():
                        player['loserSecondaries'][game.losSecondaryThird[0].name] = 1
                    else:
                        player['loserSecondaries'][game.losSecondaryThird[0].name] += 1
                playerGl['sql'].score += game.losTotal
            player['totalGames'] = player['wins'] + player['loses'] + player['ties']
            player['winRate'] = float(
                "{:.2f}".format(player['wins'] * 100 / player['totalGames'] if player['totalGames'] > 0 else 0))
            playerGl['sql'].rank = [Rank.query.filter(Rank.score <= playerGl['sql'].score).order_by(desc(Rank.score)).first()]
            for otherPl in player['winnerPlayers'].keys():
                oPl = Player.query.filter_by(username=otherPl).first()
                tot = player['winnerPlayers'][otherPl] + (
                    player['loserPlayers'][otherPl] if otherPl in player['loserPlayers'].keys() else 0) + (
                          player['tiePlayers'][otherPl] if otherPl in player['tiePlayers'].keys() else 0)
                rate = PlayerWinRatesPlayer.query.filter_by(fromUpdate=update.id).filter_by(player1=playerGl['sql'].id).filter_by(player2=oPl.id).first()
                if not rate:
                    rate = PlayerWinRatesPlayer(
                        player1=playerGl['sql'].id,
                        player2=oPl.id,
                        fromUpdate=update.id,
                    )
                rate.rate1 = float("{:.2f}".format(player['winnerPlayers'][otherPl] * 100 / tot)) if tot > 0 else 0
                db.session.add(rate)
                db.session.commit()
            for otherPl in player['loserPlayers'].keys():
                oPl = Player.query.filter_by(username=otherPl).first()
                tot = player['loserPlayers'][otherPl] + (
                    player['winnerPlayers'][otherPl] if otherPl in player['winnerPlayers'].keys() else 0) + (
                          player['tiePlayers'][otherPl] if otherPl in player['tiePlayers'].keys() else 0)
                rate = PlayerWinRatesPlayer.query.filter_by(fromUpdate=update.id).filter_by(player1=playerGl['sql'].id).filter_by(player2=oPl.id).first()
                if not rate:
                    rate = PlayerWinRatesPlayer(
                        player1=playerGl['sql'].id,
                        player2=oPl.id,
                        fromUpdate=update.id
                    )
                rate.rate2 = float("{:.2f}".format(player['loserPlayers'][otherPl] * 100 / tot)) if tot > 0 else 0
                db.session.add(rate)
                db.session.commit()
            for otherPl in player['tiePlayers'].keys():
                oPl = Player.query.filter_by(username=otherPl).first()
                tot = player['tiePlayers'][otherPl] + (
                    player['winnerPlayers'][otherPl] if otherPl in player['winnerPlayers'].keys() else 0) + (
                          player['loserPlayers'][otherPl] if otherPl in player['loserPlayers'].keys() else 0)
                rate = PlayerWinRatesPlayer.query.filter_by(fromUpdate=update.id).filter_by(player1=playerGl['sql'].id).filter_by(player2=oPl.id).first()
                if not rate:
                    rate = PlayerWinRatesPlayer(
                        player1=playerGl['sql'].id,
                        player2=oPl.id,
                        fromUpdate=update.id
                    )
                rate.rate3 = float("{:.2f}".format(player['tiePlayers'][otherPl] * 100 / tot)) if tot > 0 else 0
                db.session.add(rate)
                db.session.commit()
            for faction in player['winnerFactions'].keys():
                fct = Faction.query.filter_by(name=faction).first()
                tot = player['winnerFactions'][faction] + (
                    player['loserFactions'][faction] if faction in player['loserFactions'].keys() else 0) + (
                          player['tieFactions'][faction] if faction in player['tieFactions'].keys() else 0)
                rate = PlayerWinRates.query.filter_by(fromUpdate=update.id).filter_by(player=playerGl['sql'].id).filter_by(faction=fct.id).first()
                if not rate:
                    rate = PlayerWinRates(
                        player=playerGl['sql'].id,
                        faction=fct.id,
                        fromUpdate=update.id
                    )
                rate.rate1 = float("{:.2f}".format(player['winnerFactions'][faction] * 100 / tot)) if tot > 0 else 0
                db.session.add(rate)
                db.session.commit()
            for faction in player['loserFactions'].keys():
                fct = Faction.query.filter_by(name=faction).first()
                tot = player['loserFactions'][faction] + (
                    player['winnerFactions'][faction] if faction in player['winnerFactions'].keys() else 0) + (
                          player['tieFactions'][faction] if faction in player['tieFactions'].keys() else 0)
                rate = PlayerWinRates.query.filter_by(fromUpdate=update.id).filter_by(player=playerGl['sql'].id).filter_by(faction=fct.id).first()
                if not rate:
                    rate = PlayerWinRates(
                        player=playerGl['sql'].id,
                        faction=fct.id,
                        fromUpdate=update.id
                    )
                rate.rate2 = float("{:.2f}".format(player['loserFactions'][faction] * 100 / tot)) if tot > 0 else 0
                db.session.add(rate)
                db.session.commit()
            for faction in player['tieFactions'].keys():
                fct = Faction.query.filter_by(name=faction).first()
                tot = player['tieFactions'][faction] + (
                    player['winnerFactions'][faction] if faction in player['winnerFactions'].keys() else 0) + (
                          player['loserFactions'][faction] if faction in player['loserFactions'].keys() else 0)
                rate = PlayerWinRates.query.filter_by(fromUpdate=update.id).filter_by(player=playerGl['sql'].id).filter_by(faction=fct.id).first()
                if not rate:
                    rate = PlayerWinRates(
                        player=playerGl['sql'].id,
                        faction=fct.id,
                        fromUpdate=update.id
                    )
                rate.rate3 = float("{:.2f}".format(player['tieFactions'][faction] * 100 / tot)) if tot > 0 else 0
                db.session.add(rate)
                db.session.commit()

            for faction in player['winnerFactionsAgainst'].keys():
                fct = Faction.query.filter_by(name=faction).first()
                tot = player['winnerFactionsAgainst'][faction] + (
                    player['loserFactionsAgainst'][faction] if faction in player['loserFactionsAgainst'].keys() else 0) + (
                          player['tieFactionsAgainst'][faction] if faction in player['tieFactionsAgainst'].keys() else 0)
                rate = PlayerWinRatesAgainst.query.filter_by(fromUpdate=update.id).filter_by(player=playerGl['sql'].id).filter_by(faction=fct.id).first()
                if not rate:
                    rate = PlayerWinRatesAgainst(
                        player=playerGl['sql'].id,
                        faction=fct.id,
                        fromUpdate=update.id
                    )
                rate.rate1 = float("{:.2f}".format(player['winnerFactionsAgainst'][faction] * 100 / tot)) if tot > 0 else 0
                db.session.add(rate)
                db.session.commit()
            for faction in player['loserFactionsAgainst'].keys():
                fct = Faction.query.filter_by(name=faction).first()
                tot = player['loserFactionsAgainst'][faction] + (
                    player['winnerFactionsAgainst'][faction] if faction in player[
                        'winnerFactionsAgainst'].keys() else 0) + (
                          player['tieFactionsAgainst'][faction] if faction in player['tieFactionsAgainst'].keys() else 0)
                rate = PlayerWinRatesAgainst.query.filter_by(fromUpdate=update.id).filter_by(player=playerGl['sql'].id).filter_by(faction=fct.id).first()
                if not rate:
                    rate = PlayerWinRatesAgainst(
                        player=playerGl['sql'].id,
                        faction=fct.id,
                        fromUpdate=update.id
                    )
                rate.rate2 = float("{:.2f}".format(player['loserFactionsAgainst'][faction] * 100 / tot)) if tot > 0 else 0
                db.session.add(rate)
                db.session.commit()
            for faction in player['tieFactionsAgainst'].keys():
                fct = Faction.query.filter_by(name=faction).first()
                tot = player['tieFactionsAgainst'][faction] + (
                    player['winnerFactionsAgainst'][faction] if faction in player[
                        'winnerFactionsAgainst'].keys() else 0) + (
                          player['loserFactionsAgainst'][faction] if faction in player[
                              'loserFactionsAgainst'].keys() else 0)
                rate = PlayerWinRatesAgainst.query.filter_by(fromUpdate=update.id).filter_by(player=playerGl['sql'].id).filter_by(faction=fct.id).first()
                if not rate:
                    rate = PlayerWinRatesAgainst(
                        player=playerGl['sql'].id,
                        faction=fct.id,
                        fromUpdate=update.id
                    )
                rate.rate3 = float("{:.2f}".format(player['tieFactionsAgainst'][faction] * 100 / tot)) if tot > 0 else 0
                db.session.add(rate)
                db.session.commit()

            for mission in player['winnerMissions'].keys():
                fct = Mission.query.filter_by(name=mission).first()
                tot = player['winnerMissions'][mission] + (
                    player['loserMissions'][mission] if mission in player['loserMissions'].keys() else 0) + (
                          player['tieMissions'][mission] if mission in player['tieMissions'].keys() else 0)
                rate = PlayerMissionRates.query.filter_by(fromUpdate=update.id).filter_by(player=playerGl['sql'].id).filter_by(mission=fct.id).first()
                if not rate:
                    rate = PlayerMissionRates(
                        player=playerGl['sql'].id,
                        mission=fct.id,
                        fromUpdate=update.id
                    )
                rate.rate1 = float("{:.2f}".format(player['winnerMissions'][mission] * 100 / tot)) if tot > 0 else 0
                db.session.add(rate)
                db.session.commit()
            for mission in player['loserMissions'].keys():
                fct = Mission.query.filter_by(name=mission).first()
                tot = player['loserMissions'][mission] + (
                    player['winnerMissions'][mission] if mission in player['winnerMissions'].keys() else 0) + (
                          player['tieMissions'][mission] if mission in player['tieMissions'].keys() else 0)
                rate = PlayerMissionRates.query.filter_by(fromUpdate=update.id).filter_by(player=playerGl['sql'].id).filter_by(mission=fct.id).first()
                if not rate:
                    rate = PlayerMissionRates(
                        player=playerGl['sql'].id,
                        mission=fct.id,
                        fromUpdate=update.id
                    )
                rate.rate2 = float("{:.2f}".format(player['loserMissions'][mission] * 100 / tot)) if tot > 0 else 0
                db.session.add(rate)
                db.session.commit()
            for mission in player['tieMissions'].keys():
                fct = Mission.query.filter_by(name=mission).first()
                tot = player['tieMissions'][mission] + (
                    player['winnerMissions'][mission] if mission in player['winnerMissions'].keys() else 0) + (
                          player['loserMissions'][mission] if mission in player['loserMissions'].keys() else 0)
                rate = PlayerMissionRates.query.filter_by(fromUpdate=update.id).filter_by(player=playerGl['sql'].id).filter_by(mission=fct.id).first()
                if not rate:
                    rate = PlayerMissionRates(
                        player=playerGl['sql'].id,
                        mission=fct.id,
                        fromUpdate=update.id
                    )
                rate.rate3 = float("{:.2f}".format(player['tieMissions'][mission] * 100 / tot)) if tot > 0 else 0
                db.session.add(rate)
                db.session.commit()
            for secondary in player['winnerSecondaries'].keys():
                fct = Secondary.query.filter_by(name=secondary).first()
                tot = player['winnerSecondaries'][secondary] + (
                    player['loserSecondaries'][secondary] if secondary in player['loserSecondaries'].keys() else 0) + (
                          player['tieSecondaries'][secondary] if secondary in player['tieSecondaries'].keys() else 0)
                rate = PlayerSecondaryRates.query.filter_by(fromUpdate=update.id).filter_by(player=playerGl['sql'].id).filter_by(secondary=fct.id).first()
                if not rate:
                    rate = PlayerSecondaryRates(
                        player=playerGl['sql'].id,
                        secondary=fct.id,
                        fromUpdate=update.id
                    )
                rate.rate1 = float("{:.2f}".format(player['winnerSecondaries'][secondary] * 100 / tot)) if tot > 0 else 0
                db.session.add(rate)
                db.session.commit()
            for secondary in player['loserSecondaries'].keys():
                fct = Secondary.query.filter_by(name=secondary).first()
                tot = player['loserSecondaries'][secondary] + (
                    player['winnerSecondaries'][secondary] if secondary in player['winnerSecondaries'].keys() else 0) + (
                          player['tieSecondaries'][secondary] if secondary in player['tieSecondaries'].keys() else 0)
                rate = PlayerSecondaryRates.query.filter_by(fromUpdate=update.id).filter_by(player=playerGl['sql'].id).filter_by(secondary=fct.id).first()
                if not rate:
                    rate = PlayerSecondaryRates(
                        player=playerGl['sql'].id,
                        secondary=fct.id,
                        fromUpdate=update.id
                    )
                rate.rate2 = float("{:.2f}".format(player['loserSecondaries'][secondary] * 100 / tot)) if tot > 0 else 0
                db.session.add(rate)
                db.session.commit()
            for secondary in player['tieSecondaries'].keys():
                fct = Secondary.query.filter_by(name=secondary).first()
                tot = player['tieSecondaries'][secondary] + (
                    player['winnerSecondaries'][secondary] if secondary in player['winnerSecondaries'].keys() else 0) + (
                          player['loserSecondaries'][secondary] if secondary in player['loserSecondaries'].keys() else 0)
                rate = PlayerSecondaryRates.query.filter_by(fromUpdate=update.id).filter_by(player=playerGl['sql'].id).filter_by(secondary=fct.id).first()
                if not rate:
                    rate = PlayerSecondaryRates(
                        player=playerGl['sql'].id,
                        secondary=fct.id,
                        fromUpdate=update.id
                    )
                rate.rate3 = float("{:.2f}".format(player['tieSecondaries'][secondary] * 100 / tot)) if tot > 0 else 0
                db.session.add(rate)
                db.session.commit()
            playerGl['updates'].append(player)
        db.session.add(playerGl['sql'])
        db.session.commit()
    return playerGl


def getPlayers():
    players = {}
    for player in Player.query.all():
        playerInd = getPlayer(player.id)
        if playerInd['sql'].steamLink:
            players[playerInd['sql'].shortName] = playerInd
    return [player for player in players.values()]


def getPlayer(pl):
    playerGl = {
        'sql': Player.query.filter_by(id=pl).first(),
        'updates': {}
    }
    if playerGl['sql']:
        if playerGl['sql'].steamLink:
            if playerGl['sql'].allowSharing:
                playerGl['name'] = playerGl['sql'].username
                for update in Update.query.all():
                    player = {
                        'factionRates': [], 'factionRatesAgainst': [],
                        'missionRates': [], 'secondaryRates': [],
                        'playerRates': [],
                    }
                    player['wins'] = len(Game.query.filter(Game.date >= update.date).filter(Game.date <= update.dateEnd).filter_by(winnerId=playerGl['sql'].steamId).filter_by(tie=False).all())
                    player['loses'] = len(Game.query.filter(Game.date >= update.date).filter(Game.date <= update.dateEnd).filter_by(loserId=playerGl['sql'].steamId).filter_by(tie=False).all())
                    player['ties'] = len(Game.query.filter(Game.date >= update.date).filter(Game.date <= update.dateEnd).filter_by(winnerId=playerGl['sql'].steamId).filter_by(tie=True).all()) + len(Game.query.filter(Game.date >= update.date).filter(Game.date <= update.dateEnd).filter_by(loserId=playerGl['sql'].steamId).filter_by(tie=True).all())
                    player['totalGames'] = player['wins'] + player['loses'] + player['ties']
                    player['winRate'] = float(
                        "{:.2f}".format(player['wins'] * 100 / player['totalGames'] if player['totalGames'] > 0 else 0))
                    for rate in PlayerWinRates.query.filter_by(fromUpdate=update.id).filter_by(player=playerGl['sql'].id).order_by(
                            desc(PlayerWinRates.rate1)).all():
                        fct = Faction.query.filter_by(id=rate.faction).first()
                        player['factionRates'].append({
                            'id': fct.id,
                            'name': fct.name,
                            'shortName': fct.shortName,
                            'winRate': rate.rate1 if rate.rate1 else 0,
                            'loseRate': rate.rate2 if rate.rate2 else 0,
                            'tieRate': rate.rate3 if rate.rate3 else 0
                        })
                    for rate in PlayerWinRatesAgainst.query.filter_by(fromUpdate=update.id).filter_by(player=playerGl['sql'].id).order_by(
                            desc(PlayerWinRatesAgainst.rate1)).all():
                        fct = Faction.query.filter_by(id=rate.faction).first()
                        player['factionRatesAgainst'].append({
                            'id': fct.id,
                            'name': fct.name,
                            'shortName': fct.shortName,
                            'winRate': rate.rate1 if rate.rate1 else 0,
                            'loseRate': rate.rate2 if rate.rate2 else 0,
                            'tieRate': rate.rate3 if rate.rate3 else 0
                        })
                    for rate in PlayerMissionRates.query.filter_by(fromUpdate=update.id).filter_by(player=playerGl['sql'].id).order_by(
                            desc(PlayerMissionRates.rate1)).all():
                        ms = Mission.query.filter_by(id=rate.mission).first()
                        player['missionRates'].append({
                            'id': ms.id,
                            'name': ms.name,
                            'shortName': ms.shortName,
                            'winRate': rate.rate1 if rate.rate1 else 0,
                            'loseRate': rate.rate2 if rate.rate2 else 0,
                            'tieRate': rate.rate3 if rate.rate3 else 0
                        })
                    for rate in PlayerSecondaryRates.query.filter_by(fromUpdate=update.id).filter_by(player=playerGl['sql'].id).order_by(
                            desc(PlayerSecondaryRates.rate1)).all():
                        sec = Secondary.query.filter_by(id=rate.secondary).first()
                        player['secondaryRates'].append({
                            'id': sec.id,
                            'name': sec.name,
                            'shortName': sec.shortName,
                            'winRate': rate.rate1 if rate.rate1 else 0,
                            'loseRate': rate.rate2 if rate.rate2 else 0,
                            'tieRate': rate.rate3 if rate.rate3 else 0
                        })
                    for rate in PlayerWinRatesPlayer.query.filter_by(fromUpdate=update.id).filter_by(player1=playerGl['sql'].id).order_by(
                            desc(PlayerWinRatesPlayer.rate1)).all():
                        oPl = Player.query.filter_by(id=rate.player2).first()
                        if oPl.allowSharing:
                            player['playerRates'].append({
                                'id': oPl.id,
                                'name': oPl.username,
                                'winRate': rate.rate1 if rate.rate1 else 0,
                                'loseRate': rate.rate2 if rate.rate2 else 0,
                                'tieRate': rate.rate3 if rate.rate3 else 0
                            })
                    playerGl['updates'][str(update.id)] = player
                player = {
                    'factionRates': [], 'factionRatesAgainst': [],
                    'missionRates': [], 'secondaryRates': [],
                    'playerRates': [],
                }
                player['wins'] = len(
                    Game.query.filter_by(
                        winnerId=playerGl['sql'].steamId).filter_by(tie=False).all())
                player['loses'] = len(
                    Game.query.filter_by(
                        loserId=playerGl['sql'].steamId).filter_by(tie=False).all())
                player['ties'] = len(
                    Game.query.filter_by(
                        winnerId=playerGl['sql'].steamId).filter_by(tie=True).all()) + len(
                    Game.query.filter_by(
                        loserId=playerGl['sql'].steamId).filter_by(tie=True).all())
                player['totalGames'] = player['wins'] + player['loses'] + player['ties']
                player['winRate'] = float(
                    "{:.2f}".format(
                        player['wins'] * 100 / player['totalGames'] if player['totalGames'] > 0 else 0))
                for rate in PlayerWinRates.query.filter_by(
                        player=playerGl['sql'].id).order_by(
                        desc(PlayerWinRates.rate1)).all():
                    fct = Faction.query.filter_by(id=rate.faction).first()
                    player['factionRates'].append({
                        'id': fct.id,
                        'name': fct.name,
                        'shortName': fct.shortName,
                        'winRate': rate.rate1 if rate.rate1 else 0,
                        'loseRate': rate.rate2 if rate.rate2 else 0,
                        'tieRate': rate.rate3 if rate.rate3 else 0
                    })
                for rate in PlayerWinRatesAgainst.query.filter_by(
                        player=playerGl['sql'].id).order_by(
                        desc(PlayerWinRatesAgainst.rate1)).all():
                    fct = Faction.query.filter_by(id=rate.faction).first()
                    player['factionRatesAgainst'].append({
                        'id': fct.id,
                        'name': fct.name,
                        'shortName': fct.shortName,
                        'winRate': rate.rate1 if rate.rate1 else 0,
                        'loseRate': rate.rate2 if rate.rate2 else 0,
                        'tieRate': rate.rate3 if rate.rate3 else 0
                    })
                for rate in PlayerMissionRates.query.filter_by(
                        player=playerGl['sql'].id).order_by(
                        desc(PlayerMissionRates.rate1)).all():
                    ms = Mission.query.filter_by(id=rate.mission).first()
                    player['missionRates'].append({
                        'id': ms.id,
                        'name': ms.name,
                        'shortName': ms.shortName,
                        'winRate': rate.rate1 if rate.rate1 else 0,
                        'loseRate': rate.rate2 if rate.rate2 else 0,
                        'tieRate': rate.rate3 if rate.rate3 else 0
                    })
                for rate in PlayerSecondaryRates.query.filter_by(
                        player=playerGl['sql'].id).order_by(
                        desc(PlayerSecondaryRates.rate1)).all():
                    sec = Secondary.query.filter_by(id=rate.secondary).first()
                    player['secondaryRates'].append({
                        'id': sec.id,
                        'name': sec.name,
                        'shortName': sec.shortName,
                        'winRate': rate.rate1 if rate.rate1 else 0,
                        'loseRate': rate.rate2 if rate.rate2 else 0,
                        'tieRate': rate.rate3 if rate.rate3 else 0
                    })
                for rate in PlayerWinRatesPlayer.query.filter_by(
                        player1=playerGl['sql'].id).order_by(
                        desc(PlayerWinRatesPlayer.rate1)).all():
                    oPl = Player.query.filter_by(id=rate.player2).first()
                    if oPl.allowSharing:
                        player['playerRates'].append({
                            'id': oPl.id,
                            'name': oPl.username,
                            'winRate': rate.rate1 if rate.rate1 else 0,
                            'loseRate': rate.rate2 if rate.rate2 else 0,
                            'tieRate': rate.rate3 if rate.rate3 else 0
                        })
                playerGl['updates'][str(0)] = player
            else:
                playerGl['name'] = "Anonymous"
    return playerGl


def getPlayerById(userId):
    return Player.query.filter_by(id=userId).first()


############
# Factions #
def updateFactions(db):
    for faction in Faction.query.all():
        updateFaction(db, faction.id)


def updateFaction(db, fact):
    factionGl = {'sql': Faction.query.filter_by(id=fact).first(), 'updates': []}
    for update in Update.query.all():
        faction = {
            'bestCounter': {},
            'worstCounter': {},
            'counterRates': {},
            'winnerRates': {},
            'loserRates': {},
            'tieRates': {},
            'bestMission': {},
            'worstMission': {},
            'tieMission': {},
            'bestSecondary': {},
            'worstSecondary': {},
            'tieSecondary': {},
            'tieCounter': {},
            'gamesWon': 0,
            'gamesLost': 0,
            'gamesTie': 0,
            'totalGames': 0,
        }
        for game in factionGl['sql'].gamesWon:
            if update.date <= game.date <= update.dateEnd if update.dateEnd else datetime(3000, 9, 25, 0, 0):
                faction['totalGames'] += 1
                if not game.tie:
                    faction['gamesWon'] += 1
                else:
                    faction['gamesTie'] += 1
                for counter in Faction.query.all():
                    if counter.name not in faction['counterRates'].keys():
                        faction['counterRates'][counter.name] = {
                            'won': 0,
                            'lost': 0,
                            'tie': 0
                        }
                    if game.losFaction[0] == counter:
                        if not game.tie:
                            if counter.name in faction['bestCounter'].keys():
                                faction['bestCounter'][counter.name].append(game)
                            else:
                                faction['bestCounter'][counter.name] = [game]
                            faction['counterRates'][counter.name]['won'] += 1
                        else:
                            if counter.name in faction['tieCounter'].keys():
                                faction['tieCounter'][counter.name].append(game)
                            else:
                                faction['tieCounter'][counter.name] = [game]
                            faction['counterRates'][counter.name]['tie'] += 1
                if not game.tie:
                    if game.mission[0].shortName in faction['bestMission'].keys():
                        faction['bestMission'][game.mission[0].shortName].append(game)
                    else:
                        faction['bestMission'][game.mission[0].shortName] = [game]
                    if game.winSecondaryFirst[0].shortName in faction['bestSecondary'].keys():
                        faction['bestSecondary'][game.winSecondaryFirst[0].shortName].append(game)
                    else:
                        faction['bestSecondary'][game.winSecondaryFirst[0].shortName] = [game]
                    if game.winSecondarySecond[0].shortName in faction['bestSecondary'].keys():
                        faction['bestSecondary'][game.winSecondarySecond[0].shortName].append(game)
                    else:
                        faction['bestSecondary'][game.winSecondarySecond[0].shortName] = [game]
                    if game.winSecondaryThird[0].shortName in faction['bestSecondary'].keys():
                        faction['bestSecondary'][game.winSecondaryThird[0].shortName].append(game)
                    else:
                        faction['bestSecondary'][game.winSecondaryThird[0].shortName] = [game]
                else:
                    if game.mission[0].shortName in faction['bestMission'].keys():
                        faction['tieMission'][game.mission[0].shortName].append(game)
                    else:
                        faction['tieMission'][game.mission[0].shortName] = [game]
                    if game.winSecondaryFirst[0].shortName in faction['bestSecondary'].keys():
                        faction['tieSecondary'][game.winSecondaryFirst[0].shortName].append(game)
                    else:
                        faction['tieSecondary'][game.winSecondaryFirst[0].shortName] = [game]
                    if game.winSecondarySecond[0].shortName in faction['bestSecondary'].keys():
                        faction['tieSecondary'][game.winSecondarySecond[0].shortName].append(game)
                    else:
                        faction['tieSecondary'][game.winSecondarySecond[0].shortName] = [game]
                    if game.winSecondaryThird[0].shortName in faction['bestSecondary'].keys():
                        faction['tieSecondary'][game.winSecondaryThird[0].shortName].append(game)
                    else:
                        faction['tieSecondary'][game.winSecondaryThird[0].shortName] = [game]
        for game in factionGl['sql'].gamesLost:
            if update.date <= game.date <= update.dateEnd if update.dateEnd else datetime(3000, 9, 25, 0, 0):
                faction['totalGames'] += 1
                if not game.tie:
                    faction['gamesLost'] += 1
                else:
                    faction['gamesTie'] += 1
                for counter in Faction.query.all():
                    if counter.name not in faction['counterRates'].keys():
                        faction['counterRates'][counter.name] = {
                            'won': 0,
                            'lost': 0,
                            'tie': 0
                        }
                    if game.winFaction[0] == counter:
                        if not game.tie:
                            if counter.name in faction['worstCounter'].keys():
                                faction['worstCounter'][counter.name].append(game)
                            else:
                                faction['worstCounter'][counter.name] = [game]
                            faction['counterRates'][counter.name]['lost'] += 1
                        else:
                            if counter.name in faction['tieCounter'].keys():
                                faction['tieCounter'][counter.name].append(game)
                            else:
                                faction['tieCounter'][counter.name] = [game]
                            faction['counterRates'][counter.name]['tie'] += 1
                if not game.tie:
                    if game.mission[0].shortName in faction['worstMission'].keys():
                        faction['worstMission'][game.mission[0].shortName].append(game)
                    else:
                        faction['worstMission'][game.mission[0].shortName] = [game]
                    if game.losSecondaryFirst[0].shortName in faction['worstSecondary'].keys():
                        faction['worstSecondary'][game.losSecondaryFirst[0].shortName].append(game)
                    else:
                        faction['worstSecondary'][game.losSecondaryFirst[0].shortName] = [game]
                    if game.losSecondarySecond[0].shortName in faction['worstSecondary'].keys():
                        faction['worstSecondary'][game.losSecondarySecond[0].shortName].append(game)
                    else:
                        faction['worstSecondary'][game.losSecondarySecond[0].shortName] = [game]
                    if game.losSecondaryThird[0].shortName in faction['worstSecondary'].keys():
                        faction['worstSecondary'][game.losSecondaryThird[0].shortName].append(game)
                    else:
                        faction['worstSecondary'][game.losSecondaryThird[0].shortName] = [game]
        if faction['totalGames'] > 0:
            faction['winRate'] = float("{:.2f}".format(faction['gamesWon'] * 100 / faction['totalGames']))
        else:
            faction['winRate'] = 0.0
        for fct in faction['counterRates'].keys():
            faction['counterRates'][fct]["winRate"] = float("{:.2f}".format(faction['counterRates'][fct]['won'] * 100 / (
                    faction['counterRates'][fct]['won'] + faction['counterRates'][fct]['lost'] +
                    faction['counterRates'][fct]['tie']))) if faction['counterRates'][fct]['won'] + \
                                                              faction['counterRates'][fct]['lost'] + \
                                                              faction['counterRates'][fct]['tie'] > 0 else 0
            faction['counterRates'][fct]["loseRate"] = float("{:.2f}".format(faction['counterRates'][fct]['lost'] * 100 / (
                    faction['counterRates'][fct]['won'] + faction['counterRates'][fct]['lost'] +
                    faction['counterRates'][fct]['tie']))) if faction['counterRates'][fct]['won'] + \
                                                              faction['counterRates'][fct]['lost'] + \
                                                              faction['counterRates'][fct]['tie'] > 0 else 0
            faction['counterRates'][fct]["tieRate"] = float("{:.2f}".format(faction['counterRates'][fct]['tie'] * 100 / (
                    faction['counterRates'][fct]['won'] + faction['counterRates'][fct]['lost'] +
                    faction['counterRates'][fct]['tie']))) if faction['counterRates'][fct]['won'] + \
                                                              faction['counterRates'][fct]['lost'] + \
                                                              faction['counterRates'][fct]['tie'] > 0 else 0
            faction['winnerRates'][fct] = faction['counterRates'][fct]["winRate"]
            faction['loserRates'][fct] = faction['counterRates'][fct]["loseRate"]
            faction['tieRates'][fct] = faction['counterRates'][fct]["tieRate"]
        faction['bestFactions'] = [Faction.query.filter_by(name=fct).first() for fct in
                                   sorted(faction['bestCounter'], key=lambda k: len(faction['bestCounter'][k]),
                                          reverse=True)]
        faction['winnerRates'] = [Faction.query.filter_by(name=fct).first() for fct in
                                  sorted(faction['winnerRates'], key=lambda k: faction['winnerRates'][k], reverse=True)]
        faction['loserRates'] = [Faction.query.filter_by(name=fct).first() for fct in
                                 sorted(faction['loserRates'], key=lambda k: faction['loserRates'][k], reverse=True)]
        faction['tieRates'] = [Faction.query.filter_by(name=fct).first() for fct in
                               sorted(faction['tieRates'], key=lambda k: faction['tieRates'][k], reverse=True)]
        faction['worstFactions'] = [Faction.query.filter_by(name=fct).first() for fct in
                                    sorted(faction['worstCounter'], key=lambda k: len(faction['worstCounter'][k]),
                                           reverse=True)]
        faction['tieFactions'] = [Faction.query.filter_by(name=fct).first() for fct in
                                  sorted(faction['tieCounter'], key=lambda k: len(faction['tieCounter'][k]), reverse=True)]
        faction['bestMissions'] = [Mission.query.filter_by(shortName=fct).first() for fct in
                                   sorted(faction['bestMission'], key=lambda k: len(faction['bestMission'][k]),
                                          reverse=True)]
        faction['worstMissions'] = [Mission.query.filter_by(shortName=fct).first() for fct in
                                    sorted(faction['worstMission'], key=lambda k: len(faction['worstMission'][k]),
                                           reverse=True)]
        faction['bestSecondaries'] = [Secondary.query.filter_by(shortName=fct).first() for fct in
                                      sorted(faction['bestSecondary'], key=lambda k: len(faction['bestSecondary'][k]),
                                             reverse=True)]
        faction['worstSecondaries'] = [Secondary.query.filter_by(shortName=fct).first() for fct in
                                       sorted(faction['worstSecondary'], key=lambda k: len(faction['worstSecondary'][k]),
                                              reverse=True)]
        faction['games'] = {}
        faction['popularity'] = faction['totalGames'] * 100 / (len(Game.query.all()) * 2)
        faction['maxGames'] = 0
        for i in range(0, 12):
            if datetime.now().month - i < 1:
                month = datetime.now().month - i + 12
                year = datetime.now().year - 1
            else:
                month = datetime.now().month - i
                year = datetime.now().year
            faction['games'][str(month) + '-' + str(year)] = 0
            for game in Game.query.filter(extract('month', Game.date) == month).filter(
                    extract('year', Game.date) == year).all():
                if game.losFaction[0] == factionGl['sql'] or game.winFaction[0] == factionGl['sql']:
                    faction['games'][str(month) + '-' + str(year)] += 1
            faction['maxGames'] = faction['games'][str(month) + '-' + str(year)] if faction['maxGames'] < faction['games'][
                str(month) + '-' + str(year)] else faction['maxGames']
        faction['games'] = dict(OrderedDict(reversed(list(faction['games'].items()))))

        for counter in faction['winnerRates']:
            if not WinRates.query.filter_by(fromUpdate=update.id).filter_by(faction1=factionGl['sql'].id).filter_by(faction2=counter.id).first():
                db.session.add(WinRates(
                    faction1=factionGl['sql'].id,
                    fromUpdate=update.id,
                    faction2=counter.id,
                    rate1=faction['counterRates'][counter.name]['winRate'] if counter.name in faction[
                        'counterRates'].keys() else 0,
                    rate2=faction['counterRates'][counter.name]['loseRate'] if counter.name in faction[
                        'counterRates'].keys() else 0,
                    rate3=faction['counterRates'][counter.name]['tieRate'] if counter.name in faction[
                        'counterRates'].keys() else 0
                ))
            else:
                rate = WinRates.query.filter_by(fromUpdate=update.id).filter_by(faction1=factionGl['sql'].id).filter_by(faction2=counter.id).first()
                rate.rate1 = faction['counterRates'][counter.name]['winRate'] if counter.name in faction[
                    'counterRates'].keys() else 0
                rate.rate2 = faction['counterRates'][counter.name]['loseRate'] if counter.name in faction[
                    'counterRates'].keys() else 0
                rate.rate3 = faction['counterRates'][counter.name]['tieRate'] if counter.name in faction[
                    'counterRates'].keys() else 0
                db.session.add(rate)
        for mission in faction['bestMissions']:
            if not MissionRates.query.filter_by(fromUpdate=update.id).filter_by(faction=factionGl['sql'].id).filter_by(mission=mission.id).first():
                db.session.add(MissionRates(
                    faction=factionGl['sql'].id,
                    fromUpdate=update.id,
                    mission=mission.id,
                    rate1=float("{:.2f}".format(len(faction['bestMission'][mission.shortName]) * 100 / faction[
                        'totalGames'])) if mission.shortName in faction['bestMission'].keys() else 0,
                    rate2=float("{:.2f}".format(len(faction['worstMission'][mission.shortName]) * 100 / faction[
                        'totalGames'])) if mission.shortName in faction['worstMission'].keys() else 0,
                    rate3=float("{:.2f}".format(len(faction['tieMission'][mission.shortName]) * 100 / faction[
                        'totalGames'])) if mission.shortName in faction['tieMission'].keys() else 0
                ))
            else:
                rate = MissionRates.query.filter_by(fromUpdate=update.id).filter_by(faction=factionGl['sql'].id).filter_by(mission=mission.id).first()
                rate.rate1 = float("{:.2f}".format(
                    len(faction['bestMission'][mission.shortName]) * 100 / faction['totalGames'])) if mission.shortName in \
                                                                                                      faction[
                                                                                                          'bestMission'].keys() else 0
                rate.rate2 = float("{:.2f}".format(
                    len(faction['worstMission'][mission.shortName]) * 100 / faction['totalGames'])) if mission.shortName in \
                                                                                                       faction[
                                                                                                           'worstMission'].keys() else 0
                rate.rate3 = float("{:.2f}".format(
                    len(faction['tieMission'][mission.shortName]) * 100 / faction['totalGames'])) if mission.shortName in \
                                                                                                     faction[
                                                                                                         'tieMission'].keys() else 0
                db.session.add(rate)
        for secondary in faction['bestSecondaries']:
            if not SecondaryRates.query.filter_by(fromUpdate=update.id).filter_by(faction=factionGl['sql'].id).filter_by(secondary=secondary.id).first():
                db.session.add(SecondaryRates(
                    faction=factionGl['sql'].id,
                    fromUpdate=update.id,
                    secondary=secondary.id,
                    rate1=float("{:.2f}".format(len(faction['bestSecondary'][secondary.shortName]) * 100 / faction[
                        'totalGames'])) if secondary.shortName in faction['bestSecondary'].keys() else 0,
                    rate2=float("{:.2f}".format(len(faction['worstSecondary'][secondary.shortName]) * 100 / faction[
                        'totalGames'])) if secondary.shortName in faction['worstSecondary'].keys() else 0,
                    rate3=float("{:.2f}".format(len(faction['tieSecondary'][secondary.shortName]) * 100 / faction[
                        'totalGames'])) if secondary.shortName in faction['tieSecondary'].keys() else 0
                ))
            else:
                rate = SecondaryRates.query.filter_by(fromUpdate=update.id).filter_by(faction=factionGl['sql'].id).filter_by(secondary=secondary.id).first()
                rate.rate1 = float("{:.2f}".format(len(faction['bestSecondary'][secondary.shortName]) * 100 / faction[
                    'totalGames'])) if secondary.shortName in faction['bestSecondary'].keys() else 0
                rate.rate2 = float("{:.2f}".format(len(faction['worstSecondary'][secondary.shortName]) * 100 / faction[
                    'totalGames'])) if secondary.shortName in faction['worstSecondary'].keys() else 0
                rate.rate3 = float("{:.2f}".format(len(faction['tieSecondary'][secondary.shortName]) * 100 / faction[
                    'totalGames'])) if secondary.shortName in faction['tieSecondary'].keys() else 0
                db.session.add(rate)
        factionGl['updates'].append(faction)
    db.session.commit()
    db.session.add(factionGl['sql'])
    db.session.commit()
    return factionGl


def getFactions():
    factions = {}
    for faction in Faction.query.all():
        factionInd = getFaction(faction.id, glo=True)
        factions[factionInd['sql'].shortName] = factionInd
    return [faction for faction in factions.values()]


def getFaction(fact, glo=False):
    factionGl = {
        'sql': Faction.query.filter_by(id=fact).first(),
        'updates': {}
    }
    for update in Update.query.all():
        faction = {
            'winnerRates': [],
            'loserRates': [],
            'bestMissions': [],
            'bestSecondaries': [],
            'factionRates': [],
            'missionRates': [],
            'secondaryRates': [],
            'playerRates': [],
            'gamesWon': 0,
            'gamesLost': 0,
            'gamesTie': 0,
            'totalGames': 0,
        }
        for game in factionGl['sql'].gamesWon:
            if update.date <= game.date <= update.dateEnd if update.dateEnd else datetime(3000, 9, 25, 0, 0):
                faction['gamesWon'] += 1
                faction['totalGames'] += 1
        for game in factionGl['sql'].gamesLost:
            if update.date <= game.date <= update.dateEnd if update.dateEnd else datetime(3000, 9, 25, 0, 0):
                faction['gamesLost'] += 1
                faction['totalGames'] += 1
        for game in factionGl['sql'].gamesTied:
            if update.date <= game.date <= update.dateEnd if update.dateEnd else datetime(3000, 9, 25, 0, 0):
                faction['gamesTie'] += 1
                faction['totalGames'] += 1

        if faction['totalGames'] > 0:
            faction['winRate'] = float("{:.2f}".format(faction['gamesWon'] * 100 / faction['totalGames']))
        else:
            faction['winRate'] = 0.0
        faction['popularity'] = float("{:.2f}".format(faction['totalGames'] * 100 / (len(Game.query.filter(Game.date >= update.date).filter(Game.date <= (update.dateEnd if update.dateEnd else datetime(3000, 9, 25, 0, 0))).all()) * 2)))

        if not glo:
            for rate in WinRates.query.filter_by(fromUpdate=update.id).filter_by(faction1=factionGl['sql'].id).order_by(desc(WinRates.rate1)).all():
                fct = Faction.query.filter_by(id=rate.faction2).first()
                faction['factionRates'].append({
                    'id': fct.id,
                    'name': fct.name,
                    'shortName': fct.shortName,
                    'winRate': rate.rate1 if rate.rate1 else 0,
                    'loseRate': rate.rate2 if rate.rate2 else 0,
                    'tieRate': rate.rate3 if rate.rate3 else 0
                })
            for rate in MissionRates.query.filter_by(fromUpdate=update.id).filter_by(faction=factionGl['sql'].id).order_by(desc(MissionRates.rate1)).all():
                ms = Mission.query.filter_by(id=rate.mission).first()
                faction['missionRates'].append({
                    'id': ms.id,
                    'name': ms.name,
                    'shortName': ms.shortName,
                    'winRate': rate.rate1 if rate.rate1 else 0,
                    'loseRate': rate.rate2 if rate.rate2 else 0,
                    'tieRate': rate.rate3 if rate.rate3 else 0
                })
            for rate in SecondaryRates.query.filter_by(fromUpdate=update.id).filter_by(faction=factionGl['sql'].id).order_by(
                    desc(SecondaryRates.rate1)).all():
                sec = Secondary.query.filter_by(id=rate.secondary).first()
                faction['secondaryRates'].append({
                    'id': sec.id,
                    'name': sec.name,
                    'shortName': sec.shortName,
                    'winRate': rate.rate1 if rate.rate1 else 0,
                    'loseRate': rate.rate2 if rate.rate2 else 0,
                    'tieRate': rate.rate3 if rate.rate3 else 0
                })
            for rate in PlayerWinRates.query.filter_by(fromUpdate=update.id).filter_by(faction=factionGl['sql'].id).order_by(
                    desc(PlayerWinRates.rate1)).all():
                pl = Player.query.filter_by(id=rate.player).first()
                faction['playerRates'].append({
                    'id': pl.id,
                    'name': pl.username,
                    'shortName': pl.shortName,
                    'winRate': rate.rate1 if rate.rate1 else 0,
                    'loseRate': rate.rate2 if rate.rate2 else 0,
                    'tieRate': rate.rate3 if rate.rate3 else 0
                })
            faction['games'] = {}
            faction['maxGames'] = 0
            for i in range(0, 12):
                if datetime.now().month - i < 1:
                    month = datetime.now().month - i + 12
                    year = datetime.now().year - 1
                else:
                    month = datetime.now().month - i
                    year = datetime.now().year
                faction['games'][str(month) + '-' + str(year)] = 0
                for game in Game.query.filter(extract('month', Game.date) == month).filter(
                        extract('year', Game.date) == year).all():
                    if game.losFaction[0] == factionGl['sql'] or game.winFaction[0] == factionGl['sql']:
                        faction['games'][str(month) + '-' + str(year)] += 1
                faction['maxGames'] = faction['games'][str(month) + '-' + str(year)] if faction['maxGames'] < \
                                                                                        faction['games'][
                                                                                            str(month) + '-' + str(
                                                                                                year)] else faction[
                    'maxGames']
            faction['games'] = dict(OrderedDict(reversed(list(faction['games'].items()))))
        else:
            if WinRates.query.filter_by(fromUpdate=update.id).filter_by(faction1=factionGl['sql'].id).order_by(desc(WinRates.rate1)).first():
                faction['winnerRates'].append(Faction.query.filter_by(
                    id=WinRates.query.filter_by(fromUpdate=update.id).filter_by(faction1=factionGl['sql'].id).order_by(
                        desc(WinRates.rate1)).first().faction2).first())
            if WinRates.query.filter_by(fromUpdate=update.id).filter_by(faction1=factionGl['sql'].id).order_by(desc(WinRates.rate2)).first():
                faction['loserRates'].append(Faction.query.filter_by(
                    id=WinRates.query.filter_by(fromUpdate=update.id).filter_by(faction1=factionGl['sql'].id).order_by(
                        desc(WinRates.rate2)).first().faction2).first())
            if MissionRates.query.filter_by(fromUpdate=update.id).filter_by(faction=factionGl['sql'].id).order_by(desc(MissionRates.rate1)).first():
                faction['bestMissions'].append(Mission.query.filter_by(
                    id=MissionRates.query.filter_by(fromUpdate=update.id).filter_by(faction=factionGl['sql'].id).order_by(
                        desc(MissionRates.rate1)).first().mission).first())
            if SecondaryRates.query.filter_by(fromUpdate=update.id).filter_by(faction=factionGl['sql'].id).order_by(desc(SecondaryRates.rate1)).first():
                faction['bestSecondaries'].append(Secondary.query.filter_by(
                    id=SecondaryRates.query.filter_by(fromUpdate=update.id).filter_by(faction=factionGl['sql'].id).order_by(
                        desc(SecondaryRates.rate1)).first().secondary).first())
        faction['updateId'] = update.id
        factionGl['updates'][str(update.id)] = faction
    faction = {
        'winnerRates': [],
        'loserRates': [],
        'bestMissions': [],
        'bestSecondaries': [],
        'factionRates': [],
        'missionRates': [],
        'secondaryRates': [],
        'playerRates': [],
        'gamesWon': 0,
        'gamesLost': 0,
        'gamesTie': 0,
        'totalGames': 0,
    }
    for game in factionGl['sql'].gamesWon:
        faction['gamesWon'] += 1
        faction['totalGames'] += 1
    for game in factionGl['sql'].gamesLost:
        faction['gamesLost'] += 1
        faction['totalGames'] += 1
    for game in factionGl['sql'].gamesTied:
        faction['gamesTie'] += 1
        faction['totalGames'] += 1

    if faction['totalGames'] > 0:
        faction['winRate'] = float("{:.2f}".format(faction['gamesWon'] * 100 / faction['totalGames']))
    else:
        faction['winRate'] = 0.0
    faction['popularity'] = float("{:.2f}".format(faction['totalGames'] * 100 / (len(
        Game.query.all()) * 2)))

    if not glo:
        for rate in WinRates.query.filter_by(faction1=factionGl['sql'].id).order_by(
                desc(WinRates.rate1)).all():
            fct = Faction.query.filter_by(id=rate.faction2).first()
            faction['factionRates'].append({
                'id': fct.id,
                'name': fct.name,
                'shortName': fct.shortName,
                'winRate': rate.rate1 if rate.rate1 else 0,
                'loseRate': rate.rate2 if rate.rate2 else 0,
                'tieRate': rate.rate3 if rate.rate3 else 0
            })
        for rate in MissionRates.query.filter_by(faction=factionGl['sql'].id).order_by(
                desc(MissionRates.rate1)).all():
            ms = Mission.query.filter_by(id=rate.mission).first()
            faction['missionRates'].append({
                'id': ms.id,
                'name': ms.name,
                'shortName': ms.shortName,
                'winRate': rate.rate1 if rate.rate1 else 0,
                'loseRate': rate.rate2 if rate.rate2 else 0,
                'tieRate': rate.rate3 if rate.rate3 else 0
            })
        for rate in SecondaryRates.query.filter_by(
                faction=factionGl['sql'].id).order_by(
                desc(SecondaryRates.rate1)).all():
            sec = Secondary.query.filter_by(id=rate.secondary).first()
            faction['secondaryRates'].append({
                'id': sec.id,
                'name': sec.name,
                'shortName': sec.shortName,
                'winRate': rate.rate1 if rate.rate1 else 0,
                'loseRate': rate.rate2 if rate.rate2 else 0,
                'tieRate': rate.rate3 if rate.rate3 else 0
            })
        for rate in PlayerWinRates.query.filter_by(
                faction=factionGl['sql'].id).order_by(
                desc(PlayerWinRates.rate1)).all():
            pl = Player.query.filter_by(id=rate.player).first()
            faction['playerRates'].append({
                'id': pl.id,
                'name': pl.username,
                'shortName': pl.shortName,
                'winRate': rate.rate1 if rate.rate1 else 0,
                'loseRate': rate.rate2 if rate.rate2 else 0,
                'tieRate': rate.rate3 if rate.rate3 else 0
            })
        faction['games'] = {}
        faction['maxGames'] = 0
        for i in range(0, 12):
            if datetime.now().month - i < 1:
                month = datetime.now().month - i + 12
                year = datetime.now().year - 1
            else:
                month = datetime.now().month - i
                year = datetime.now().year
            faction['games'][str(month) + '-' + str(year)] = 0
            for game in Game.query.filter(extract('month', Game.date) == month).filter(
                    extract('year', Game.date) == year).all():
                if game.losFaction[0] == factionGl['sql'] or game.winFaction[0] == factionGl['sql']:
                    faction['games'][str(month) + '-' + str(year)] += 1
            faction['maxGames'] = faction['games'][str(month) + '-' + str(year)] if faction['maxGames'] < \
                                                                                    faction['games'][
                                                                                        str(month) + '-' + str(
                                                                                            year)] else faction[
                'maxGames']
        faction['games'] = dict(OrderedDict(reversed(list(faction['games'].items()))))
    else:
        if WinRates.query.filter_by(faction1=factionGl['sql'].id).order_by(
                desc(WinRates.rate1)).first():
            faction['winnerRates'].append(Faction.query.filter_by(
                id=WinRates.query.filter_by(faction1=factionGl['sql'].id).order_by(
                    desc(WinRates.rate1)).first().faction2).first())
        if WinRates.query.filter_by(faction1=factionGl['sql'].id).order_by(
                desc(WinRates.rate2)).first():
            faction['loserRates'].append(Faction.query.filter_by(
                id=WinRates.query.filter_by(faction1=factionGl['sql'].id).order_by(
                    desc(WinRates.rate2)).first().faction2).first())
        if MissionRates.query.filter_by(faction=factionGl['sql'].id).order_by(
                desc(MissionRates.rate1)).first():
            faction['bestMissions'].append(Mission.query.filter_by(
                id=MissionRates.query.filter_by(faction=factionGl['sql'].id).order_by(
                    desc(MissionRates.rate1)).first().mission).first())
        if SecondaryRates.query.filter_by(faction=factionGl['sql'].id).order_by(
                desc(SecondaryRates.rate1)).first():
            faction['bestSecondaries'].append(Secondary.query.filter_by(
                id=SecondaryRates.query.filter_by(faction=factionGl['sql'].id).order_by(
                    desc(SecondaryRates.rate1)).first().secondary).first())
    faction['updateId'] = 0
    factionGl['updates'][str(0)] = faction
    return factionGl


############
# Missions #
def updateMissions(db):
    for mission in Mission.query.all():
        updateMission(db, mission.id)


def updateMission(db, fact):
    missionGl = {
        'sql': Mission.query.filter_by(id=fact).first(),
        'updates': []
    }
    for update in Update.query.all():
        mission = {
            'avgScore': 0,
            'avgScoreFirst': 0,
            'avgScoreSecond': 0,
            'avgScoreThird': 0,
            'avgScoreFourth': 0,
            'totalScore': 0,
            'totalScoreFirst': 0,
            'totalScoreSecond': 0,
            'totalScoreThird': 0,
            'totalScoreFourth': 0,
            'totalGames': 0
        }
        for game in Game.query.filter(Game.date >= update.date).filter(Game.date <= (update.dateEnd if update.dateEnd else datetime(3000, 9, 25, 0, 0))).filter(Game.mission.contains(missionGl['sql'])).all():
            mission['totalGames'] += 2
            mission['totalScore'] += game.winPrimary + game.losPrimary
            mission['totalScoreFirst'] += game.winPrimaryFirst + game.losPrimaryFirst
            mission['totalScoreSecond'] += game.winPrimarySecond + game.losPrimarySecond
            mission['totalScoreThird'] += game.winPrimaryThird + game.losPrimaryThird
            mission['totalScoreFourth'] += game.winPrimaryFourth + game.losPrimaryFourth
        missionGl['updates'].append(mission)
    try:
        missionGl['sql'].avgScore = float("{:.2f}".format(sum([mission['totalScore'] / mission['totalGames'] for mission in missionGl['updates']])/len(missionGl['updates'])))
        missionGl['sql'].avgScoreFirst = float("{:.2f}".format(sum([mission['totalScoreFirst'] / mission['totalGames'] for mission in missionGl['updates']])/len(missionGl['updates'])))
        missionGl['sql'].avgScoreSecond = float("{:.2f}".format(sum([mission['totalScoreSecond'] / mission['totalGames'] for mission in missionGl['updates']])/len(missionGl['updates'])))
        missionGl['sql'].avgScoreThird = float("{:.2f}".format(sum([mission['totalScoreThird'] / mission['totalGames'] for mission in missionGl['updates']])/len(missionGl['updates'])))
        missionGl['sql'].avgScoreFourth = float("{:.2f}".format(sum([mission['totalScoreFourth'] / mission['totalGames'] for mission in missionGl['updates']])/len(missionGl['updates'])))
    except ZeroDivisionError:
        missionGl['sql'].avgScore = 0
        missionGl['sql'].avgScoreFirst = 0
        missionGl['sql'].avgScoreSecond = 0
        missionGl['sql'].avgScoreThird = 0
        missionGl['sql'].avgScoreFourth = 0
    db.session.add(missionGl['sql'])
    db.session.commit()
    return missionGl


def getMissions():
    missions = {}
    for mission in Mission.query.all():
        missionInd = getMission(mission.id)
        missions[missionInd['sql'].shortName] = missionInd
    return [mission for mission in missions.values()]


def getMission(ms):
    missionGl = {
        'sql': Mission.query.filter_by(id=ms).first(),
        'updates': {},
    }
    for update in Update.query.all():
        mission = {
            'popularity': 0,
            'bestFactions': {},
            'worstFactions': {},
            'games': {},
            'maxGames': 0
        }
        for rate in MissionRates.query.filter_by(fromUpdate=update.id).filter_by(mission=ms).order_by(desc(MissionRates.rate1)).all():
            mission['bestFactions'][Faction.query.filter_by(id=rate.faction).first().name] = {
                'winRate': rate.rate1,
                'loseRate': rate.rate2,
                'tieRate': rate.rate3,
                'id': rate.faction,
                'shortName': Faction.query.filter_by(id=rate.faction).first().shortName
            }
        for rate in MissionRates.query.filter_by(fromUpdate=update.id).filter_by(mission=ms).order_by(desc(MissionRates.rate2)).all():
            mission['worstFactions'][Faction.query.filter_by(id=rate.faction).first().name] = {
                'winRate': rate.rate1,
                'loseRate': rate.rate2,
                'tieRate': rate.rate3,
                'id': rate.faction,
                'shortName': Faction.query.filter_by(id=rate.faction).first().shortName
            }
        mission['popularity'] = float("{:.2f}".format(
            len(Game.query.filter(Game.date >= update.date).filter(Game.date <= update.dateEnd).filter(Game.mission.contains(missionGl['sql'])).all()) * 100 / len(Game.query.filter(Game.date >= update.date).filter(Game.date <= update.dateEnd).all())))
        mission['topFaction'] = Faction.query.filter_by(name=list(mission['bestFactions'].keys())[0]).first() if mission[
            'bestFactions'] else None
        mission['worstFaction'] = Faction.query.filter_by(name=list(mission['worstFactions'].keys())[0]).first() if mission[
            'worstFactions'] else None
        for i in range(0, 12):
            if datetime.now().month - i < 1:
                month = datetime.now().month - i + 12
                year = datetime.now().year - 1
            else:
                month = datetime.now().month - i
                year = datetime.now().year
            mission['games'][str(month) + '-' + str(year)] = 0
            for j in range(0, len(Game.query.filter(extract('month', Game.date) == month).filter(
                    extract('year', Game.date) == year).filter(Game.mission.contains(missionGl['sql'])).all())):
                mission['games'][str(month) + '-' + str(year)] += 1
            mission['maxGames'] = mission['games'][str(month) + '-' + str(year)] if mission['maxGames'] < mission['games'][
                str(month) + '-' + str(year)] else mission['maxGames']
        mission['games'] = dict(OrderedDict(reversed(list(mission['games'].items()))))
        missionGl['updates'][str(update.id)] = mission
    mission = {
        'popularity': 0,
        'bestFactions': {},
        'worstFactions': {},
        'games': {},
        'maxGames': 0
    }
    for rate in MissionRates.query.filter_by(mission=ms).order_by(
            desc(MissionRates.rate1)).all():
        mission['bestFactions'][Faction.query.filter_by(id=rate.faction).first().name] = {
            'winRate': rate.rate1,
            'loseRate': rate.rate2,
            'tieRate': rate.rate3,
            'id': rate.faction,
            'shortName': Faction.query.filter_by(id=rate.faction).first().shortName
        }
    for rate in MissionRates.query.filter_by(mission=ms).order_by(
            desc(MissionRates.rate2)).all():
        mission['worstFactions'][Faction.query.filter_by(id=rate.faction).first().name] = {
            'winRate': rate.rate1,
            'loseRate': rate.rate2,
            'tieRate': rate.rate3,
            'id': rate.faction,
            'shortName': Faction.query.filter_by(id=rate.faction).first().shortName
        }
    mission['popularity'] = float("{:.2f}".format(
        len(Game.query.filter(Game.mission.contains(missionGl['sql'])).all()) * 100 / len(Game.query.all())))
    mission['topFaction'] = Faction.query.filter_by(name=list(mission['bestFactions'].keys())[0]).first() if mission[
        'bestFactions'] else None
    mission['worstFaction'] = Faction.query.filter_by(name=list(mission['worstFactions'].keys())[0]).first() if mission[
        'worstFactions'] else None
    for i in range(0, 12):
        if datetime.now().month - i < 1:
            month = datetime.now().month - i + 12
            year = datetime.now().year - 1
        else:
            month = datetime.now().month - i
            year = datetime.now().year
        mission['games'][str(month) + '-' + str(year)] = 0
        for j in range(0, len(Game.query.filter(extract('month', Game.date) == month).filter(
                extract('year', Game.date) == year).filter(Game.mission.contains(missionGl['sql'])).all())):
            mission['games'][str(month) + '-' + str(year)] += 1
        mission['maxGames'] = mission['games'][str(month) + '-' + str(year)] if mission['maxGames'] < mission['games'][
            str(month) + '-' + str(year)] else mission['maxGames']
    mission['games'] = dict(OrderedDict(reversed(list(mission['games'].items()))))
    missionGl['updates'][str(0)] = mission
    return missionGl


###############
# Secondaries #
def updateSecondaries(db):
    for secondary in Secondary.query.all():
        updateSecondary(db, secondary.id)


def updateSecondary(db, sc):
    secondaryGl = {
        'sql': Secondary.query.filter_by(id=sc).first(),
        'updates': [],
    }
    for update in Update.query.all():
        secondary = {
            'avgScore': 0,
            'avgScoreFirst': 0,
            'avgScoreSecond': 0,
            'avgScoreThird': 0,
            'avgScoreFourth': 0,
            'totalScore': 0,
            'totalScoreFirst': 0,
            'totalScoreSecond': 0,
            'totalScoreThird': 0,
            'totalScoreFourth': 0,
            'totalGames': 0
        }
        for game in Game.query.filter(
                Game.date >= update.date).filter(
                Game.date <= (update.dateEnd if update.dateEnd else datetime(3000, 9, 25, 0, 0))).filter(
                Game.winSecondaryFirst.contains(secondaryGl['sql'])).all():
            secondary['totalGames'] += 1
            secondary['totalScore'] += game.winSecondaryFirstScore
            secondary['totalScoreFirst'] += game.winSecondaryFirstScoreTurn1 if game.winSecondaryFirstScoreTurn1 else 0
            secondary['totalScoreSecond'] += game.winSecondaryFirstScoreTurn2 if game.winSecondaryFirstScoreTurn2 else 0
            secondary['totalScoreThird'] += game.winSecondaryFirstScoreTurn3 if game.winSecondaryFirstScoreTurn3 else 0
            secondary['totalScoreFourth'] += game.winSecondaryFirstScoreTurn4 if game.winSecondaryFirstScoreTurn4 else 0
        for game in Game.query.filter(
                Game.date >= update.date).filter(
                Game.date <= (update.dateEnd if update.dateEnd else datetime(3000, 9, 25, 0, 0))).filter(
                Game.winSecondarySecond.contains(secondaryGl['sql'])).all():
            secondary['totalGames'] += 1
            secondary['totalScore'] += game.winSecondarySecondScore
            secondary['totalScoreFirst'] += game.winSecondarySecondScoreTurn1 if game.winSecondarySecondScoreTurn1 else 0
            secondary['totalScoreSecond'] += game.winSecondarySecondScoreTurn2 if game.winSecondarySecondScoreTurn2 else 0
            secondary['totalScoreThird'] += game.winSecondarySecondScoreTurn3 if game.winSecondarySecondScoreTurn3 else 0
            secondary['totalScoreFourth'] += game.winSecondarySecondScoreTurn4 if game.winSecondarySecondScoreTurn4 else 0
        for game in Game.query.filter(
                Game.date >= update.date).filter(
                Game.date <= (update.dateEnd if update.dateEnd else datetime(3000, 9, 25, 0, 0))).filter(
                Game.winSecondaryThird.contains(secondaryGl['sql'])).all():
            secondary['totalGames'] += 1
            secondary['totalScore'] += game.winSecondaryThirdScore
            secondary['totalScoreFirst'] += game.winSecondaryThirdScoreTurn1 if game.winSecondaryThirdScoreTurn1 else 0
            secondary['totalScoreSecond'] += game.winSecondaryThirdScoreTurn2 if game.winSecondaryThirdScoreTurn2 else 0
            secondary['totalScoreThird'] += game.winSecondaryThirdScoreTurn3 if game.winSecondaryThirdScoreTurn3 else 0
            secondary['totalScoreFourth'] += game.winSecondaryThirdScoreTurn4 if game.winSecondaryThirdScoreTurn4 else 0
        for game in Game.query.filter(
                Game.date >= update.date).filter(
                Game.date <= (update.dateEnd if update.dateEnd else datetime(3000, 9, 25, 0, 0))).filter(
                Game.losSecondaryFirst.contains(secondaryGl['sql'])).all():
            secondary['totalGames'] += 1
            secondary['totalScore'] += game.losSecondaryFirstScore
            secondary['totalScoreFirst'] += game.losSecondaryFirstScoreTurn1 if game.losSecondaryFirstScoreTurn1 else 0
            secondary['totalScoreSecond'] += game.losSecondaryFirstScoreTurn2 if game.losSecondaryFirstScoreTurn2 else 0
            secondary['totalScoreThird'] += game.losSecondaryFirstScoreTurn3 if game.losSecondaryFirstScoreTurn3 else 0
            secondary['totalScoreFourth'] += game.losSecondaryFirstScoreTurn4 if game.losSecondaryFirstScoreTurn4 else 0
        for game in Game.query.filter(
                Game.date >= update.date).filter(
                Game.date <= (update.dateEnd if update.dateEnd else datetime(3000, 9, 25, 0, 0))).filter(
                Game.losSecondarySecond.contains(secondaryGl['sql'])).all():
            secondary['totalGames'] += 1
            secondary['totalScore'] += game.losSecondarySecondScore
            secondary['totalScoreFirst'] += game.losSecondarySecondScoreTurn1 if game.losSecondarySecondScoreTurn1 else 0
            secondary['totalScoreSecond'] += game.losSecondarySecondScoreTurn2 if game.losSecondarySecondScoreTurn2 else 0
            secondary['totalScoreThird'] += game.losSecondarySecondScoreTurn3 if game.losSecondarySecondScoreTurn3 else 0
            secondary['totalScoreFourth'] += game.losSecondarySecondScoreTurn4 if game.losSecondarySecondScoreTurn4 else 0
        for game in Game.query.filter(
                Game.date >= update.date).filter(
                Game.date <= (update.dateEnd if update.dateEnd else datetime(3000, 9, 25, 0, 0))).filter(
                Game.losSecondaryThird.contains(secondaryGl['sql'])).all():
            secondary['totalGames'] += 1
            secondary['totalScore'] += game.losSecondaryThirdScore
            secondary['totalScoreFirst'] += game.losSecondaryThirdScoreTurn1 if game.losSecondaryThirdScoreTurn1 else 0
            secondary['totalScoreSecond'] += game.losSecondaryThirdScoreTurn2 if game.losSecondaryThirdScoreTurn2 else 0
            secondary['totalScoreThird'] += game.losSecondaryThirdScoreTurn3 if game.losSecondaryThirdScoreTurn3 else 0
            secondary['totalScoreFourth'] += game.losSecondaryThirdScoreTurn4 if game.losSecondaryThirdScoreTurn4 else 0
        secondaryGl['updates'].append(secondary)
    try:
        secondaryGl['sql'].avgScore = float(
            "{:.2f}".format(sum([secondary['totalScore'] / secondary['totalGames'] for secondary in secondaryGl['updates']])/len(secondaryGl['updates'])))
        secondaryGl['sql'].avgScoreFirst = float("{:.2f}".format(sum([secondary['totalScoreFirst'] / secondary['totalGames'] for secondary in secondaryGl['updates']])/len(secondaryGl['updates'])))
        secondaryGl['sql'].avgScoreSecond = float(
            "{:.2f}".format(sum([secondary['totalScoreSecond'] / secondary['totalGames'] for secondary in secondaryGl['updates']])/len(secondaryGl['updates'])))
        secondaryGl['sql'].avgScoreThird = float(
            "{:.2f}".format(sum([secondary['totalScoreThird'] / secondary['totalGames'] for secondary in secondaryGl['updates']])/len(secondaryGl['updates'])))
        secondaryGl['sql'].avgScoreFourth = float(
            "{:.2f}".format(sum([secondary['totalScoreFourth'] / secondary['totalGames'] for secondary in secondaryGl['updates']])/len(secondaryGl['updates'])))
    except ZeroDivisionError:
        secondaryGl['sql'].avgScore = 0
        secondaryGl['sql'].avgScoreFirst = 0
        secondaryGl['sql'].avgScoreSecond = 0
        secondaryGl['sql'].avgScoreThird = 0
        secondaryGl['sql'].avgScoreFourth = 0

    secondaryGl['sql'].totalGames = sum([secondary['totalGames'] for secondary in secondaryGl['updates']])
    db.session.add(secondaryGl['sql'])
    db.session.commit()
    return secondaryGl


def getSecondaries():
    secondaries = {}
    for secondary in Secondary.query.all():
        secondaryInd = getSecondary(secondary.id)
        secondaries[secondaryInd['sql'].shortName] = secondaryInd
    return [secondary for secondary in secondaries.values()]


def getSecondary(sc):
    secondaryGl = {
        'sql': Secondary.query.filter_by(id=sc).first(),
        'updates': {},
    }
    for update in Update.query.all():
        secondary = {
            'popularity': 0,
            'bestFactions': {},
            'games': {},
            'maxGames': 0
        }
        for rate in SecondaryRates.query.filter_by(fromUpdate=update.id).filter_by(secondary=sc).order_by(desc(SecondaryRates.rate1)).all():
            secondary['bestFactions'][Faction.query.filter_by(id=rate.faction).first().name] = {
                'winRate': rate.rate1,
                'loseRate': rate.rate2,
                'tieRate': rate.rate3,
                'id': rate.faction,
                'shortName': Faction.query.filter_by(id=rate.faction).first().shortName
            }
        popularity = len(Game.query.filter(
                Game.date >= update.date).filter(
                Game.date <= (update.dateEnd if update.dateEnd else datetime(3000, 9, 25, 0, 0))).filter(
                Game.winSecondaryFirst.contains(secondaryGl['sql'])).all())
        popularity += len(Game.query.filter(
                Game.date >= update.date).filter(
                Game.date <= (update.dateEnd if update.dateEnd else datetime(3000, 9, 25, 0, 0))).filter(
                Game.winSecondarySecond.contains(secondaryGl['sql'])).all())
        popularity += len(Game.query.filter(
                Game.date >= update.date).filter(
                Game.date <= (update.dateEnd if update.dateEnd else datetime(3000, 9, 25, 0, 0))).filter(
                Game.winSecondaryThird.contains(secondaryGl['sql'])).all())
        popularity += len(Game.query.filter(
                Game.date >= update.date).filter(
                Game.date <= (update.dateEnd if update.dateEnd else datetime(3000, 9, 25, 0, 0))).filter(
                Game.losSecondaryFirst.contains(secondaryGl['sql'])).all())
        popularity += len(Game.query.filter(
                Game.date >= update.date).filter(
                Game.date <= (update.dateEnd if update.dateEnd else datetime(3000, 9, 25, 0, 0))).filter(
                Game.losSecondarySecond.contains(secondaryGl['sql'])).all())
        popularity += len(Game.query.filter(
                Game.date >= update.date).filter(
                Game.date <= (update.dateEnd if update.dateEnd else datetime(3000, 9, 25, 0, 0))).filter(
                Game.losSecondaryThird.contains(secondaryGl['sql'])).all())
        secondary['popularity'] = float("{:.2f}".format(popularity * 100 / len(Game.query.filter(
                Game.date >= update.date).filter(
                Game.date <= (update.dateEnd if update.dateEnd else datetime(3000, 9, 25, 0, 0))).all())))
        secondary['topFaction'] = Faction.query.filter_by(name=list(secondary['bestFactions'].keys())[0]).first() if \
            secondary['bestFactions'] else None
        for i in range(0, 12):
            if datetime.now().month - i < 1:
                month = datetime.now().month - i + 12
                year = datetime.now().year - 1
            else:
                month = datetime.now().month - i
                year = datetime.now().year
            secondary['games'][str(month) + '-' + str(year)] = len(
                Game.query.filter(extract('month', Game.date) == month).filter(extract('year', Game.date) == year).filter(
                    Game.winSecondaryFirst.contains(secondaryGl['sql'])).all())
            secondary['games'][str(month) + '-' + str(year)] += len(
                Game.query.filter(extract('month', Game.date) == month).filter(extract('year', Game.date) == year).filter(
                    Game.winSecondarySecond.contains(secondaryGl['sql'])).all())
            secondary['games'][str(month) + '-' + str(year)] += len(
                Game.query.filter(extract('month', Game.date) == month).filter(extract('year', Game.date) == year).filter(
                    Game.winSecondaryThird.contains(secondaryGl['sql'])).all())
            secondary['games'][str(month) + '-' + str(year)] += len(
                Game.query.filter(extract('month', Game.date) == month).filter(extract('year', Game.date) == year).filter(
                    Game.losSecondaryFirst.contains(secondaryGl['sql'])).all())
            secondary['games'][str(month) + '-' + str(year)] += len(
                Game.query.filter(extract('month', Game.date) == month).filter(extract('year', Game.date) == year).filter(
                    Game.losSecondarySecond.contains(secondaryGl['sql'])).all())
            secondary['games'][str(month) + '-' + str(year)] += len(
                Game.query.filter(extract('month', Game.date) == month).filter(extract('year', Game.date) == year).filter(
                    Game.losSecondaryThird.contains(secondaryGl['sql'])).all())
            secondary['maxGames'] = secondary['games'][str(month) + '-' + str(year)] if secondary['maxGames'] < \
                                                                                        secondary['games'][
                                                                                            str(month) + '-' + str(
                                                                                                year)] else secondary[
                'maxGames']
        secondary['games'] = dict(OrderedDict(reversed(list(secondary['games'].items()))))
        secondary['updateId'] = update.id
        secondaryGl['updates'][str(update.id)] = secondary
    secondary = {
        'popularity': 0,
        'bestFactions': {},
        'games': {},
        'maxGames': 0
    }
    for rate in SecondaryRates.query.filter_by(secondary=sc).order_by(
            desc(SecondaryRates.rate1)).all():
        secondary['bestFactions'][Faction.query.filter_by(id=rate.faction).first().name] = {
            'winRate': rate.rate1,
            'loseRate': rate.rate2,
            'tieRate': rate.rate3,
            'id': rate.faction,
            'shortName': Faction.query.filter_by(id=rate.faction).first().shortName
        }
    popularity = len(Game.query.filter(
        Game.winSecondaryFirst.contains(secondaryGl['sql'])).all())
    popularity += len(Game.query.filter(
        Game.winSecondarySecond.contains(secondaryGl['sql'])).all())
    popularity += len(Game.query.filter(
        Game.winSecondaryThird.contains(secondaryGl['sql'])).all())
    popularity += len(Game.query.filter(
        Game.losSecondaryFirst.contains(secondaryGl['sql'])).all())
    popularity += len(Game.query.filter(
        Game.losSecondarySecond.contains(secondaryGl['sql'])).all())
    popularity += len(Game.query.filter(
        Game.losSecondaryThird.contains(secondaryGl['sql'])).all())
    secondary['popularity'] = float("{:.2f}".format(popularity * 100 / len(Game.query.all())))
    secondary['topFaction'] = Faction.query.filter_by(name=list(secondary['bestFactions'].keys())[0]).first() if \
        secondary['bestFactions'] else None
    for i in range(0, 12):
        if datetime.now().month - i < 1:
            month = datetime.now().month - i + 12
            year = datetime.now().year - 1
        else:
            month = datetime.now().month - i
            year = datetime.now().year
        secondary['games'][str(month) + '-' + str(year)] = len(
            Game.query.filter(extract('month', Game.date) == month).filter(extract('year', Game.date) == year).filter(
                Game.winSecondaryFirst.contains(secondaryGl['sql'])).all())
        secondary['games'][str(month) + '-' + str(year)] += len(
            Game.query.filter(extract('month', Game.date) == month).filter(extract('year', Game.date) == year).filter(
                Game.winSecondarySecond.contains(secondaryGl['sql'])).all())
        secondary['games'][str(month) + '-' + str(year)] += len(
            Game.query.filter(extract('month', Game.date) == month).filter(extract('year', Game.date) == year).filter(
                Game.winSecondaryThird.contains(secondaryGl['sql'])).all())
        secondary['games'][str(month) + '-' + str(year)] += len(
            Game.query.filter(extract('month', Game.date) == month).filter(extract('year', Game.date) == year).filter(
                Game.losSecondaryFirst.contains(secondaryGl['sql'])).all())
        secondary['games'][str(month) + '-' + str(year)] += len(
            Game.query.filter(extract('month', Game.date) == month).filter(extract('year', Game.date) == year).filter(
                Game.losSecondarySecond.contains(secondaryGl['sql'])).all())
        secondary['games'][str(month) + '-' + str(year)] += len(
            Game.query.filter(extract('month', Game.date) == month).filter(extract('year', Game.date) == year).filter(
                Game.losSecondaryThird.contains(secondaryGl['sql'])).all())
        secondary['maxGames'] = secondary['games'][str(month) + '-' + str(year)] if secondary['maxGames'] < \
                                                                                    secondary['games'][
                                                                                        str(month) + '-' + str(
                                                                                            year)] else secondary[
            'maxGames']
    secondary['games'] = dict(OrderedDict(reversed(list(secondary['games'].items()))))
    secondary['updateId'] = 0
    secondaryGl['updates'][str(0)] = secondary
    return secondaryGl


###########
# General #
def getGeneral():
    players = Player.query.order_by(desc(Player.score)).all()
    topPlayers = players[0:3]
    factions = {}
    auxTop = 0
    auxBot = 0
    auxMost = 0
    auxLess = 100000000000
    mostUsedFaction = None
    lessUsedFaction = None
    topFaction = None
    botFaction = None
    for faction in Faction.query.all():
        factions[faction.name] = {
            'loses': 0,
            'wins': 0,
            'ties': 0,
            'uses': 0,
        }
        for game in Game.query.filter(Game.losFaction.contains(faction)).filter_by(tie=False).all():
            factions[faction.name]['loses'] += 1
            factions[faction.name]['uses'] += 1
        for game in Game.query.filter(Game.losFaction.contains(faction)).filter_by(tie=True).all():
            factions[faction.name]['ties'] += 1
            factions[faction.name]['uses'] += 1
        for game in Game.query.filter(Game.winFaction.contains(faction)).filter_by(tie=False).all():
            factions[faction.name]['wins'] += 1
            factions[faction.name]['uses'] += 1
        for game in Game.query.filter(Game.winFaction.contains(faction)).filter_by(tie=True).all():
            factions[faction.name]['wins'] += 1
            factions[faction.name]['uses'] += 1
        if factions[faction.name]['uses'] > auxMost:
            auxMost = factions[faction.name]['uses']
            mostUsedFaction = faction
        if factions[faction.name]['uses'] < auxLess:
            auxLess = factions[faction.name]['uses']
            lessUsedFaction = faction
        if factions[faction.name]['loses'] > auxBot:
            auxBot = factions[faction.name]['loses']
            botFaction = faction
        if factions[faction.name]['wins'] > auxTop:
            auxTop = factions[faction.name]['wins']
            topFaction = faction
    primaries = {}
    secondaries = {}
    for mission in Mission.query.all():
        primaries[mission.name] = len(Game.query.filter(Game.mission.contains(mission)).all())
    for secondary in Secondary.query.all():
        secondaries[secondary.name] = len(Game.query.filter(Game.winSecondaryFirst.contains(secondary)).all()) + \
                                      len(Game.query.filter(Game.winSecondarySecond.contains(secondary)).all()) + \
                                      len(Game.query.filter(Game.winSecondaryThird.contains(secondary)).all()) + \
                                      len(Game.query.filter(Game.losSecondaryFirst.contains(secondary)).all()) + \
                                      len(Game.query.filter(Game.losSecondarySecond.contains(secondary)).all()) + \
                                      len(Game.query.filter(Game.losSecondaryThird.contains(secondary)).all())
    primaries = {k: v for k, v in sorted(primaries.items(), key=operator.itemgetter(1), reverse=True)}
    secondaries = {k: v for k, v in sorted(secondaries.items(), key=operator.itemgetter(1), reverse=True)}
    lenGames = len(Game.query.all())
    games = Game.query.all()
    general = {
        'totalGames': lenGames,
        'avgWinner': float("{:.2f}".format(sum([game.winTotal for game in games]) / lenGames if lenGames > 0 else 0.0)),
        'avgLoser': float("{:.2f}".format(sum([game.losTotal for game in games]) / lenGames if lenGames > 0 else 0.0)),
        'missionMostPlayed': list(primaries)[0] if list(primaries) else None,
        'missionLessPlayed': list(primaries)[-1] if list(primaries) else None,
        'secondaryMostPlayed': list(secondaries)[0] if list(secondaries) else None,
        'secondaryLessPlayed': list(secondaries)[-1] if list(secondaries) else None,
        'factionMostPlayed': mostUsedFaction.name if mostUsedFaction else None,
        'factionLessPlayed': lessUsedFaction.name if lessUsedFaction else None,
        'factionMostWinRate': topFaction.name if topFaction else None,
        'factionLessWinRate': botFaction.name if botFaction else None,
        'totalPlayers': len(players),
        'top1Player': topPlayers[0].username if topPlayers else None,
        'top2Player': topPlayers[1].username if len(topPlayers) > 1 else None,
        'top3Player': topPlayers[2].username if len(topPlayers) > 2 else None,
        'played': {},
        'maxPlayed': 0
    }
    for i in range(0, 12):
        if datetime.now().month - i < 1:
            month = datetime.now().month - i + 12
            year = datetime.now().year - 1
        else:
            month = datetime.now().month - i
            year = datetime.now().year
        general['played'][str(month) + '-' + str(year)] = len(
            Game.query.filter(extract('month', Game.date) == month).filter(extract('year', Game.date) == year).all())
        general['maxPlayed'] = general['played'][str(month) + '-' + str(year)] if general['maxPlayed'] < \
                                                                                  general['played'][
                                                                                      str(month) + '-' + str(year)] else \
            general['maxPlayed']
    general['played'] = dict(OrderedDict(reversed(list(general['played'].items()))))
    return general


###################
# Admin functions #
def randomize_data(db):
    createDatabase(db)
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
        "Ork Kommandos",
        "Tomb Worlds",
        "Hunter Cadre",
        "Cadre Mercenary",
        "Hive Fleets",
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
        'Open game',
        'Matched game'
    ]
    players = [names.get_full_name() for i in range(0, 3)]
    players.append('mariofelectronica')
    for i in range(0, 1):
        d = random.randint(int(time.time()) - 31556926, int(time.time()))
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


def addNewUpdate(db, form):
    if not Update.query.filter_by(name=form['name']).first():
        lastUpd = Update.query.order_by(desc(Update.date)).first()
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
