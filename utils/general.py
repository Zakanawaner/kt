import operator

from database import Game, Player, Faction, Mission, Secondary
from sqlalchemy import extract, desc
from datetime import datetime
from collections import OrderedDict


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