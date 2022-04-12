from source.db.db import Game, Player, Mission, Rank, Secondary, Faction, Tournament
from sqlalchemy import extract
from datetime import datetime, timedelta
from collections import OrderedDict
import random
import time
import names
import operator

# TODO tts
#  gestionar el tipo de torneo
#  añadir instrucciones en el tablero
#  mirar si podemos sacar el nombre de la mision

# TODO py
#  descartar lo que venga y no esté bien
#  securizar el envio intempestivo de botonazos


def handlePlayers(db, response, opt):
    if not Player.query.filter_by(username=response[opt]).first():
        player = Player(
            username=response[opt],
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
                    name=response[response[opt]]['secondaries'][sec]['name']) if not Secondary.query.filter_by(
                    name=response[response[opt]]['secondaries'][sec]['name']).first() else Secondary.query.filter_by(
                    name=response[response[opt]]['secondaries'][sec]['name']).first()
                db.session.add(response[response[opt]]['secondaries'][sec]['name'])
    db.session.commit()
    return response


def handleTournament(db, response):
    if 'tournament' in response.keys():
        if not Tournament.query.filter_by(name=response['tournament']).first():
            response['tournament'] = Tournament(name=response['tournament'])
            db.session.add(response['tournament'])
        else:
            response['tournament'] = Tournament.query.filter_by(name=response['tournament']).first()
    db.session.commit()
    return response


def handleGameData(response, db):
    winnerSql = handlePlayers(db, response, 'winner')
    loserSql = handlePlayers(db, response, 'loser')
    response = handleFactions(db, response, 'winner')
    response = handleFactions(db, response, 'loser')
    response = handleSecondaries(db, response, 'winner')
    response = handleSecondaries(db, response, 'loser')
    response = handleMission(db, response)
    response = handleTournament(db, response)

    game = Game(
        date=datetime.now(),
        mission=[response['mission']] if response['mission'] else [],
        initFirst=[winnerSql] if response[response['winner']]['initiative'][0] else [loserSql],
        initSecond=[winnerSql] if response[response['winner']]['initiative'][1] else [loserSql],
        initThird=[winnerSql] if response[response['winner']]['initiative'][2] else [loserSql],
        initFourth=[winnerSql] if response[response['winner']]['initiative'][3] else [loserSql],
        winFaction=[response[response['winner']]['faction']] if response[response['winner']]['faction'] else [],
        winTotal=response[response['winner']]['total'],
        winPrimary=response[response['winner']]['primaries']['total'],
        winPrimaryFirst=response[response['winner']]['primaries']['first'],
        winPrimarySecond=response[response['winner']]['primaries']['second'],
        winPrimaryThird=response[response['winner']]['primaries']['third'],
        winPrimaryFourth=response[response['winner']]['primaries']['fourth'],
        winSecondary=response[response['winner']]['secondaries']['total'],
        winSecondaryFirst=[response[response['winner']]['secondaries']['first']['name']],
        winSecondaryFirstScore=response[response['winner']]['secondaries']['first']['score'],
        winSecondarySecond=[response[response['winner']]['secondaries']['second']['name']],
        winSecondarySecondScore=response[response['winner']]['secondaries']['second']['score'],
        winSecondaryThird=[response[response['winner']]['secondaries']['third']['name']],
        winSecondaryThirdScore=response[response['winner']]['secondaries']['third']['score'],
        losFaction=[response[response['loser']]['faction']]if response[response['loser']]['faction'] else [],
        losTotal=response[response['loser']]['total'],
        losPrimary=response[response['loser']]['primaries']['total'],
        losPrimaryFirst=response[response['loser']]['primaries']['first'],
        losPrimarySecond=response[response['loser']]['primaries']['second'],
        losPrimaryThird=response[response['loser']]['primaries']['third'],
        losPrimaryFourth=response[response['loser']]['primaries']['fourth'],
        losSecondary=response[response['loser']]['secondaries']['total'],
        losSecondaryFirst=[response[response['loser']]['secondaries']['first']['name']],
        losSecondaryFirstScore=response[response['loser']]['secondaries']['first']['score'],
        losSecondarySecond=[response[response['loser']]['secondaries']['second']['name']],
        losSecondarySecondScore=response[response['loser']]['secondaries']['second']['score'],
        losSecondaryThird=[response[response['loser']]['secondaries']['third']['name']],
        losSecondaryThirdScore=response[response['loser']]['secondaries']['third']['score'],
        rollOffWinner=[Player.query.filter_by(username=response['rollOffWinner']).first()] if 'rollOffWinner' in response.keys() else [],
        rollOffSelection=response['rollOffWinnerSelection'] if 'rollOffWinnerSelection' in response.keys() else '',
        tie=response['tie']
    )
    game.winner.append(winnerSql)
    game.loser.append(loserSql)

    if 'tournament' in response.keys():
        response['tournament'].games.append(game)
        db.session.add(response['tournament'])
    db.session.add(game)
    db.session.commit()


def createDatabase(db):
    db.create_all()

    db.session.add(Rank(name="a", score=0))
    db.session.add(Rank(name="b", score=50))
    db.session.add(Rank(name="c", score=100))
    db.session.add(Rank(name="d", score=200))
    db.session.add(Rank(name="e", score=400))
    db.session.add(Rank(name="f", score=800))
    db.session.add(Rank(name="g", score=1600))

    db.session.add(Tournament(name="III Liga Mercenaria"))

    db.session.commit()


def getGames():
    games = Game.query.all()
    return games


def getPlayers():
    players = {}
    for player in Player.query.all():
        players[player.username] = {
            'sql': player,
            'wins': [],
            'loses': [],
            'ties': [],
            'factions': {},
            'missions': {},
            'secondaries': {}
        }
        for game in Game.query.filter(Game.winner.contains(player)).all():
            players[player.username]['wins'].append(game) if not game.tie else players[player.username]['ties'].append(game)
        for game in Game.query.filter(Game.loser.contains(player)).all():
            players[player.username]['loses'].append(game) if not game.tie else players[player.username]['ties'].append(game)

        for faction in Faction.query.all():
            players[player.username]['factions'][faction.name] = 0
            for game in players[player.username]['wins']:
                if game.winFaction[0] == faction:
                    players[player.username]['factions'][faction.name] += 1
            for game in players[player.username]['loses']:
                if game.losFaction[0] == faction:
                    players[player.username]['factions'][faction.name] -= 1
        for mission in Mission.query.all():
            players[player.username]['missions'][mission.name] = 0
            for game in players[player.username]['wins']:
                if game.mission[0] == mission:
                    players[player.username]['missions'][mission.name] += 1
            for game in players[player.username]['loses']:
                if game.mission[0] == mission:
                    players[player.username]['missions'][mission.name] -= 1
        for secondary in Secondary.query.all():
            players[player.username]['secondaries'][secondary.name] = 0
            for game in players[player.username]['wins']:
                if game.winSecondaryFirst[0] == secondary:
                    players[player.username]['secondaries'][secondary.name] += 1
                if game.winSecondarySecond[0] == secondary:
                    players[player.username]['secondaries'][secondary.name] += 1
                if game.winSecondaryThird[0] == secondary:
                    players[player.username]['secondaries'][secondary.name] += 1
            for game in players[player.username]['loses']:
                if game.losSecondaryFirst[0] == secondary:
                    players[player.username]['secondaries'][secondary.name] -= 1
                if game.losSecondarySecond[0] == secondary:
                    players[player.username]['secondaries'][secondary.name] -= 1
                if game.losSecondaryThird[0] == secondary:
                    players[player.username]['secondaries'][secondary.name] -= 1
        if player.wins + player.loses + player.ties > 0:
            players[player.username]['winRate'] = float("{:.2f}".format(player.wins * 100 / (player.wins + player.loses + player.ties)))
        else:
            players[player.username]['winRate'] = 0.0
        players[player.username]['factions'] = {k: v for k, v in sorted(players[player.username]['factions'].items(), key=operator.itemgetter(1), reverse=True)}
        players[player.username]['missions'] = {k: v for k, v in sorted(players[player.username]['missions'].items(), key=operator.itemgetter(1), reverse=True)}
        players[player.username]['secondaries'] = {k: v for k, v in sorted(players[player.username]['secondaries'].items(), key=operator.itemgetter(1), reverse=True)}
        players[player.username]['topFaction'] = Faction.query.filter_by(name=next(iter(players[player.username]['factions'].keys()))).first()
        players[player.username]['topMission'] = Mission.query.filter_by(name=next(iter(players[player.username]['missions'].keys()))).first()
        players[player.username]['topSecondary'] = Secondary.query.filter_by(name=next(iter(players[player.username]['secondaries'].keys()))).first()
        if len(players[player.username]['wins']) + len(players[player.username]['loses']) + len(players[player.username]['ties']):
            players[player.username]['avgScore'] = round(player.score / (len(players[player.username]['wins']) + len(players[player.username]['loses']) + len(players[player.username]['ties'])))
        else:
            players[player.username]['avgScore'] = 0.0
    return [player for player in players.values()]


def getFactions():
    factions = {}
    for faction in Faction.query.all():
        factions[faction.name] = {
            'name': faction.name,
            'shortName': faction.shortName,
            'sql': faction,
            'wins': [],
            'loses': [],
            'ties': [],
            'counter': {},
            'missions': {},
            'secondaries': {}
        }
        for game in Game.query.filter(Game.winFaction.contains(faction)).all():
            factions[faction.name]['wins'].append(game) if not game.tie else factions[faction.name]['ties'].append(game)
        for game in Game.query.filter(Game.loser.contains(faction)).all():
            factions[faction.name]['loses'].append(game) if not game.tie else factions[faction.name]['ties'].append(game)
        if len(factions[faction.name]['wins']) + len(factions[faction.name]['loses']) + len(factions[faction.name]['ties']) > 0:
            if len(factions[faction.name]['wins']) + len(factions[faction.name]['loses']) + len(factions[faction.name]['ties']) > 0:
                factions[faction.name]['winRate'] = float("{:.2f}".format(len(factions[faction.name]['wins']) * 100 / (len(factions[faction.name]['wins']) + len(factions[faction.name]['loses']) + len(factions[faction.name]['ties']))))
            else:
                factions[faction.name]['winRate'] = 0.0
        else:
            factions[faction.name]['winRate'] = 0.0

        for counter in Faction.query.all():
            factions[faction.name]['counter'][counter.name] = 0
            for game in factions[faction.name]['wins']:
                if game.losFaction[0] == counter:
                    factions[faction.name]['counter'][counter.name] += 1
            for game in factions[faction.name]['loses']:
                if game.winFaction[0] == counter:
                    factions[faction.name]['counter'][counter.name] -= 1

        for mission in Mission.query.all():
            factions[faction.name]['missions'][mission.name] = 0
            for game in factions[faction.name]['wins']:
                if game.mission[0] == mission:
                    factions[faction.name]['missions'][mission.name] += 1
            for game in factions[faction.name]['loses']:
                if game.mission[0] == mission:
                    factions[faction.name]['missions'][mission.name] -= 1

        for secondary in Secondary.query.all():
            factions[faction.name]['secondaries'][secondary.name] = 0
            for game in factions[faction.name]['wins']:
                if game.winSecondaryFirst[0] == secondary:
                    factions[faction.name]['secondaries'][secondary.name] += 1
                if game.winSecondarySecond[0] == secondary:
                    factions[faction.name]['secondaries'][secondary.name] += 1
                if game.winSecondaryThird[0] == secondary:
                    factions[faction.name]['secondaries'][secondary.name] += 1
            for game in factions[faction.name]['loses']:
                if game.losSecondaryFirst[0] == secondary:
                    factions[faction.name]['secondaries'][secondary.name] -= 1
                if game.losSecondarySecond[0] == secondary:
                    factions[faction.name]['secondaries'][secondary.name] -= 1
                if game.losSecondaryThird[0] == secondary:
                    factions[faction.name]['secondaries'][secondary.name] -= 1

        factions[faction.name]['counter'] = {k: v for k, v in sorted(factions[faction.name]['counter'].items(), key=operator.itemgetter(1), reverse=True)}
        factions[faction.name]['bestCounter'] = Faction.query.filter_by(name=next(iter(factions[faction.name]['counter'].keys()))).first()
        factions[faction.name]['counter'] = {k: v for k, v in sorted(factions[faction.name]['counter'].items(), key=operator.itemgetter(1))}
        factions[faction.name]['worstCounter'] = Faction.query.filter_by(name=next(iter(factions[faction.name]['counter'].keys()))).first()
        if len(Game.query.all()) > 0:
            factions[faction.name]['popularity'] = len(factions[faction.name]['wins'] + factions[faction.name]['loses'] + factions[faction.name]['ties']) * 100 / len(Game.query.all())
        else:
            factions[faction.name]['popularity'] = 0.0
        factions[faction.name]['missions'] = {k: v for k, v in sorted(factions[faction.name]['missions'].items(), key=operator.itemgetter(1), reverse=True)}
        factions[faction.name]['secondaries'] = {k: v for k, v in sorted(factions[faction.name]['secondaries'].items(), key=operator.itemgetter(1), reverse=True)}
        factions[faction.name]['topMission'] = Mission.query.filter_by(name=next(iter(factions[faction.name]['missions'].keys()))).first()
        factions[faction.name]['topSecondary'] = Secondary.query.filter_by(name=next(iter(factions[faction.name]['secondaries'].keys()))).first()
    return [faction for faction in factions.values()]


def getFaction(fact):
    faction = {
        'sql': Faction.query.filter_by(id=fact).first(),
        'bestCounter': {},
        'worstCounter': {},
        'tieCounter': {}
    }
    for counter in Faction.query.all():
        if Game.query.filter(Game.winFaction.contains(faction['sql'])).filter(Game.losFaction.contains(counter)).all():
            faction['bestCounter'][counter.name] = Game.query.filter(Game.winFaction.contains(faction['sql'])).filter(Game.losFaction.contains(counter)).all()
    for counter in Faction.query.all():
        if Game.query.filter(Game.losFaction.contains(faction['sql'])).filter(Game.winFaction.contains(counter)).all():
            faction['worstCounter'][counter.name] = Game.query.filter(Game.losFaction.contains(faction['sql'])).filter(Game.winFaction.contains(counter)).all()
    for counter in faction['bestCounter'].keys():
        for i, game in enumerate(faction['bestCounter'][counter]):
            if game.tie:
                faction['bestCounter'][counter].pop(i)
                if counter in faction['tieCounter'].keys():
                    faction['tieCounter'][counter].append(game)
                else:
                    faction['tieCounter'][counter] = [game]
        if not faction['bestCounter'][counter]:
            faction['bestCounter'].pop(counter, None)
    for counter in faction['worstCounter'].keys():
        for i, game in enumerate(faction['worstCounter'][counter]):
            if game.tie:
                faction['worstCounter'][counter].pop(i)
                if counter in faction['tieCounter'].keys():
                    faction['tieCounter'][counter].append(game)
                else:
                    faction['tieCounter'][counter] = [game]
        if not faction['worstCounter'][counter]:
            faction['worstCounter'].pop(counter, None)

    if len(faction['bestCounter']) + len(faction['worstCounter']) + len(faction['tieCounter']) > 0:
        faction['winRate'] = float("{:.2f}".format(len(faction['bestCounter']) * 100 / (len(faction['bestCounter']) + len(faction['worstCounter']) + len(faction['tieCounter']))))
    else:
        faction['winRate'] = 0.0
    faction['bestFactions'] = [Faction.query.filter_by(name=fct).first() for fct in sorted(faction['bestCounter'], key=lambda k: len(faction['bestCounter'][k]), reverse=True)]
    faction['worstFactions'] = [Faction.query.filter_by(name=fct).first() for fct in sorted(faction['worstCounter'], key=lambda k: len(faction['worstCounter'][k]), reverse=True)]
    faction['tieFactions'] = [Faction.query.filter_by(name=fct).first() for fct in sorted(faction['tieCounter'], key=lambda k: len(faction['tieCounter'][k]), reverse=True)]
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
        for game in Game.query.filter(extract('month', Game.date) == month).filter(extract('year', Game.date) == year).all():
            if game.losFaction[0] == faction['sql'] or game.winFaction[0] == faction['sql']:
                faction['games'][str(month) + '-' + str(year)] += 1
        faction['maxGames'] = faction['games'][str(month) + '-' + str(year)] if faction['maxGames'] < faction['games'][str(month) + '-' + str(year)] else faction['maxGames']
    faction['games'] = dict(OrderedDict(reversed(list(faction['games'].items()))))
    return faction


def getMissions():
    missions = {}
    for mission in Mission.query.all():
        missions[mission.name] = {
            'name': mission.name,
            'games': [],
            'factions': {},
            'secondaries': {}
        }
        score = 0
        for game in Game.query.filter(Game.mission.contains(mission)).all():
            missions[mission.name]['games'].append(game)
            score += game.winPrimary + game.losPrimary
        if len(missions[mission.name]['games']) > 0:
            missions[mission.name]['avgScore'] = float("{:.2f}".format(score / (2*len(missions[mission.name]['games']))))
        else:
            missions[mission.name]['avgScore'] = 0.0
        for faction in Faction.query.all():
            missions[mission.name]['factions'][faction.name] = 0
            for game in missions[mission.name]['games']:
                if game.winFaction[0] == faction:
                    missions[mission.name]['factions'][faction.name] += game.winTotal
                if game.losFaction[0] == faction:
                    missions[mission.name]['factions'][faction.name] += game.losTotal
        missions[mission.name]['factions'] = {k: v for k, v in sorted(missions[mission.name]['factions'].items(), key=operator.itemgetter(1), reverse=True)}
        missions[mission.name]['topFaction'] = Faction.query.filter_by(name=next(iter(missions[mission.name]['factions'].keys()))).first()

        for secondary in Secondary.query.all():
            missions[mission.name]['secondaries'][secondary.name] = 0
            for game in missions[mission.name]['games']:
                if game.winSecondaryFirst[0] == secondary:
                    missions[mission.name]['secondaries'][secondary.name] += game.winSecondaryFirstScore
                if game.winSecondarySecond[0] == secondary:
                    missions[mission.name]['secondaries'][secondary.name] += game.winSecondarySecondScore
                if game.winSecondaryThird[0] == secondary:
                    missions[mission.name]['secondaries'][secondary.name] += game.winSecondaryThirdScore
                if game.losSecondaryFirst[0] == secondary:
                    missions[mission.name]['secondaries'][secondary.name] = game.losSecondaryFirstScore
                if game.losSecondarySecond[0] == secondary:
                    missions[mission.name]['secondaries'][secondary.name] = game.losSecondarySecondScore
                if game.losSecondaryThird[0] == secondary:
                    missions[mission.name]['secondaries'][secondary.name] = game.losSecondaryThirdScore
        missions[mission.name]['secondaries'] = {k: v for k, v in sorted(missions[mission.name]['secondaries'].items(), key=operator.itemgetter(1), reverse=True)}
        missions[mission.name]['topSecondary'] = Secondary.query.filter_by(name=next(iter(missions[mission.name]['secondaries'].keys()))).first()
        missions[mission.name]['games'] = len(missions[mission.name]['games'])
    return [mission for mission in missions.values()]


def getGeneral():
    games = Game.query.all()
    players = Player.query.order_by(Player.score.desc()).all()
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
        for game in games:
            if game.losFaction[0] == faction and not game.tie:
                factions[faction.name]['loses'] += 1
                factions[faction.name]['uses'] += 1
            if game.winFaction[0] == faction and not game.tie:
                factions[faction.name]['wins'] += 1
                factions[faction.name]['uses'] += 1
            if game.winFaction[0] == faction and game.tie:
                factions[faction.name]['ties'] += 1
                factions[faction.name]['uses'] += 1
            if game.losFaction[0] == faction and game.tie:
                factions[faction.name]['ties'] += 1
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
    for game in games:
        if game.mission[0].name in primaries.keys():
            primaries[game.mission[0].name] += 1
        else:
            primaries[game.mission[0].name] = 1
        if game.winSecondaryFirst[0].name in secondaries.keys():
            secondaries[game.winSecondaryFirst[0].name] += 1
        else:
            secondaries[game.winSecondaryFirst[0].name] = 1
        if game.winSecondarySecond[0].name in secondaries.keys():
            secondaries[game.winSecondarySecond[0].name] += 1
        else:
            secondaries[game.winSecondarySecond[0].name] = 1
        if game.winSecondaryThird[0].name in secondaries.keys():
            secondaries[game.winSecondaryThird[0].name] += 1
        else:
            secondaries[game.winSecondaryThird[0].name] = 1
    primaries = {k: v for k, v in sorted(primaries.items(), key=operator.itemgetter(1), reverse=True)}
    secondaries = {k: v for k, v in sorted(secondaries.items(), key=operator.itemgetter(1), reverse=True)}
    general = {
        'totalGames': len(games),
        'avgWinner': sum([game.winTotal for game in games]) / len(games) if len(games) > 0 else 0.0,
        'avgLoser': sum([game.losTotal for game in games]) / len(games) if len(games) > 0 else 0.0,
        'missionMostPlayed': list(primaries)[0],
        'missionLessPlayed': list(primaries)[-1],
        'secondaryMostPlayed': list(secondaries)[0],
        'secondaryLessPlayed': list(secondaries)[-1],
        'factionMostPlayed': mostUsedFaction.name,
        'factionLessPlayed': lessUsedFaction.name,
        'factionMostWinRate': topFaction.name,
        'factionLessWinRate': botFaction.name,
        'totalPlayers': len(players),
        'top1Player': topPlayers[0].username,
        'top2Player': topPlayers[1].username,
        'top3Player': topPlayers[2].username,
    }
    return general


def randomize_data(db):
    createDatabase(db)
    factions = [
        "Space Marines",
        "Grey Knights",
        "Imperial Guard",
        "Veteran Guardsmen",
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
    factions = [
        "Space Marines",
        "Grey Knights",
        "Imperial Guard",
        "Veteran Guardsmen",
    ]
    secondaries = [
        "headhunter",
        "challenge",
        "rout",
        "execution",
        "deadly marksman",
        "rob and ransack",
        "seize ground",
        "hold the line",
        "protect assets",
        "damage limitation",
        "plant banner",
        "central control",
        "capture hostage and infiltrate",
        "behind enemy lines",
        "upload viral code",
        "implant",
        "sabotage",
        "interloper",
        "mark target",
        "triangulate",
        "vantage",
        "retrieval",
        "overrun"
    ]
    tournaments = [
        'Open Game',
        'I Liga Meercenaria',
        'II Liga Meercenaria',
        'III Liga Meercenaria'
    ]
    players = [names.get_full_name() for i in range(0, 10)]
    for i in range(0, 10):
        random.seed(i)
        d = random.randint(1, int(time.time()))
        datetime.fromtimestamp(d)
        ok = False
        while not ok:
            playersName = [random.choice(players), random.choice(players)]
            if playersName[0] != playersName[1]:
                ok = True
        response = {
            'tournament': random.choice(tournaments),
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
                'initiative': [random.choice([True, False]),
                               random.choice([True, False]),
                               random.choice([True, False]),
                               random.choice([True, False])],
                'faction': random.choice(factions),
                'primaries': {
                    'first': random.randint(0, 4),
                    'second': random.randint(0, 4),
                    'third': random.randint(0, 4),
                    'fourth': random.randint(0, 4),
                },
                'secondaries': {
                    'first': {
                        'name': random.choice(secondaries),
                        'score': random.randint(0, 3)
                    },
                    'second': {
                        'name': random.choice(secondaries),
                        'score': random.randint(0, 3)
                    },
                    'third': {
                        'name': random.choice(secondaries),
                        'score': random.randint(0, 3)
                    },
                }
            },
            playersName[1]: {
                'initiative': [random.choice([True, False]),
                               random.choice([True, False]),
                               random.choice([True, False]),
                               random.choice([True, False])],
                'faction': random.choice(factions),
                'primaries': {
                    'first': random.randint(0, 4),
                    'second': random.randint(0, 4),
                    'third': random.randint(0, 4),
                    'fourth': random.randint(0, 4),
                },
                'secondaries': {
                    'first': {
                        'name': random.choice(secondaries),
                        'score': random.randint(0, 3)
                    },
                    'second': {
                        'name': random.choice(secondaries),
                        'score': random.randint(0, 3)
                    },
                    'third': {
                        'name': random.choice(secondaries),
                        'score': random.randint(0, 3)
                    },
                }
            }
        }
        response[playersName[0]]['primaries']['total'] = response[playersName[0]]['primaries']['first'] + response[playersName[0]]['primaries']['second'] + response[playersName[0]]['primaries']['third'] + response[playersName[0]]['primaries']['fourth']
        response[playersName[1]]['primaries']['total'] = response[playersName[0]]['primaries']['first'] + response[playersName[1]]['primaries']['second'] + response[playersName[1]]['primaries']['third'] + response[playersName[1]]['primaries']['fourth']
        response[playersName[0]]['secondaries']['total'] = response[playersName[0]]['secondaries']['first']['score'] + response[playersName[0]]['secondaries']['second']['score'] + response[playersName[0]]['secondaries']['third']['score']
        response[playersName[1]]['secondaries']['total'] = response[playersName[1]]['secondaries']['first']['score'] + response[playersName[1]]['secondaries']['second']['score'] + response[playersName[1]]['secondaries']['third']['score']
        response[playersName[0]]['total'] = response[playersName[0]]['primaries']['total'] + response[playersName[0]]['secondaries']['total']
        response[playersName[1]]['total'] = response[playersName[1]]['primaries']['total'] + response[playersName[1]]['secondaries']['total']
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

        winnerSql = handlePlayers(db, response, 'winner')
        loserSql = handlePlayers(db, response, 'loser')
        response = handleFactions(db, response, 'winner')
        response = handleFactions(db, response, 'loser')
        response = handleSecondaries(db, response, 'winner')
        response = handleSecondaries(db, response, 'loser')
        response = handleMission(db, response)
        response = handleTournament(db, response)

        game = Game(
            date=datetime.fromtimestamp(d),
            mission=[response['mission']] if response['mission'] else [],
            initFirst=[winnerSql] if response[response['winner']]['initiative'][0] else [loserSql],
            initSecond=[winnerSql] if response[response['winner']]['initiative'][1] else [loserSql],
            initThird=[winnerSql] if response[response['winner']]['initiative'][2] else [loserSql],
            initFourth=[winnerSql] if response[response['winner']]['initiative'][3] else [loserSql],
            winFaction=[response[response['winner']]['faction']] if response[response['winner']]['faction'] else [],
            winTotal=response[response['winner']]['total'],
            winPrimary=response[response['winner']]['primaries']['total'],
            winPrimaryFirst=response[response['winner']]['primaries']['first'],
            winPrimarySecond=response[response['winner']]['primaries']['second'],
            winPrimaryThird=response[response['winner']]['primaries']['third'],
            winPrimaryFourth=response[response['winner']]['primaries']['fourth'],
            winSecondary=response[response['winner']]['secondaries']['total'],
            winSecondaryFirst=[response[response['winner']]['secondaries']['first']['name']],
            winSecondaryFirstScore=response[response['winner']]['secondaries']['first']['score'],
            winSecondarySecond=[response[response['winner']]['secondaries']['second']['name']],
            winSecondarySecondScore=response[response['winner']]['secondaries']['second']['score'],
            winSecondaryThird=[response[response['winner']]['secondaries']['third']['name']],
            winSecondaryThirdScore=response[response['winner']]['secondaries']['third']['score'],
            losFaction=[response[response['loser']]['faction']] if response[response['loser']]['faction'] else [],
            losTotal=response[response['loser']]['total'],
            losPrimary=response[response['loser']]['primaries']['total'],
            losPrimaryFirst=response[response['loser']]['primaries']['first'],
            losPrimarySecond=response[response['loser']]['primaries']['second'],
            losPrimaryThird=response[response['loser']]['primaries']['third'],
            losPrimaryFourth=response[response['loser']]['primaries']['fourth'],
            losSecondary=response[response['loser']]['secondaries']['total'],
            losSecondaryFirst=[response[response['loser']]['secondaries']['first']['name']],
            losSecondaryFirstScore=response[response['loser']]['secondaries']['first']['score'],
            losSecondarySecond=[response[response['loser']]['secondaries']['second']['name']],
            losSecondarySecondScore=response[response['loser']]['secondaries']['second']['score'],
            losSecondaryThird=[response[response['loser']]['secondaries']['third']['name']],
            losSecondaryThirdScore=response[response['loser']]['secondaries']['third']['score'],
            rollOffWinner=[Player.query.filter_by(
                username=response['rollOffWinner']).first()] if 'rollOffWinner' in response.keys() else [],
            rollOffSelection=response['rollOffWinnerSelection'] if 'rollOffWinnerSelection' in response.keys() else '',
            tie=response['tie']
        )
        game.winner.append(winnerSql)
        game.loser.append(loserSql)

        response['tournament'].games.append(game)
        db.session.add(response['tournament'])
        db.session.add(game)
        db.session.commit()
