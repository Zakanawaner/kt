from sqlalchemy import extract, desc
from datetime import datetime
from collections import OrderedDict
from database import (
    Game, Player, Mission, Secondary, Faction,
    WinRates, MissionRates, SecondaryRates,
    PlayerWinRates, Update
)


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
            if update.date <= game.date <= update.dateEnd:
                faction['totalGames'] += 1
                faction['gamesWon'] += 1
                for counter in Faction.query.all():
                    if counter.name not in faction['counterRates'].keys():
                        faction['counterRates'][counter.name] = {
                            'won': 0,
                            'lost': 0,
                            'tie': 0
                        }
                    if game.losFaction[0] == counter:
                        if counter.name in faction['bestCounter'].keys():
                            faction['bestCounter'][counter.name].append(game)
                        else:
                            faction['bestCounter'][counter.name] = [game]
                        faction['counterRates'][counter.name]['won'] += 1
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
        for game in factionGl['sql'].gamesLost:
            if update.date <= game.date <= update.dateEnd:
                faction['totalGames'] += 1
                faction['gamesLost'] += 1
                for counter in Faction.query.all():
                    if counter.name not in faction['counterRates'].keys():
                        faction['counterRates'][counter.name] = {
                            'won': 0,
                            'lost': 0,
                            'tie': 0
                        }
                    if game.winFaction[0] == counter:
                        if counter.name in faction['worstCounter'].keys():
                            faction['worstCounter'][counter.name].append(game)
                        else:
                            faction['worstCounter'][counter.name] = [game]
                        faction['counterRates'][counter.name]['lost'] += 1
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
        for game in factionGl['sql'].gamesTied:
            if update.date <= game.date <= update.dateEnd:
                faction['totalGames'] += 1
                faction['gamesTie'] += 1
                for counter in Faction.query.all():
                    if counter.name not in faction['counterRates'].keys():
                        faction['counterRates'][counter.name] = {
                            'won': 0,
                            'lost': 0,
                            'tie': 0
                        }
                    if game.winFaction[0] == counter or game.losFaction[0] == counter:
                        if counter.name in faction['tieCounter'].keys():
                            faction['tieCounter'][counter.name].append(game)
                        else:
                            faction['tieCounter'][counter.name] = [game]
                        faction['counterRates'][counter.name]['tie'] += 1
                if game.mission[0].shortName in faction['tieMission'].keys():
                    faction['tieMission'][game.mission[0].shortName].append(game)
                else:
                    faction['tieMission'][game.mission[0].shortName] = [game]
                if game.winSecondaryFirst[0].shortName in faction['tieSecondary'].keys():
                    faction['tieSecondary'][game.winSecondaryFirst[0].shortName].append(game)
                else:
                    faction['tieSecondary'][game.winSecondaryFirst[0].shortName] = [game]
                if game.winSecondarySecond[0].shortName in faction['tieSecondary'].keys():
                    faction['tieSecondary'][game.winSecondarySecond[0].shortName].append(game)
                else:
                    faction['tieSecondary'][game.winSecondarySecond[0].shortName] = [game]
                if game.winSecondaryThird[0].shortName in faction['tieSecondary'].keys():
                    faction['tieSecondary'][game.winSecondaryThird[0].shortName].append(game)
                else:
                    faction['tieSecondary'][game.winSecondaryThird[0].shortName] = [game]
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

        for counter in Faction.query.all():
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
                        'counterRates'].keys() else 0,
                    games=(faction['counterRates'][counter.name]['won'] + faction['counterRates'][counter.name]['lost'] + faction['counterRates'][counter.name]['tie']) if counter.name in faction[
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
                rate.games = (faction['counterRates'][counter.name]['won'] + faction['counterRates'][counter.name]['lost'] + faction['counterRates'][counter.name]['tie']) if counter.name in faction[
                        'counterRates'].keys() else 0
                db.session.add(rate)
        for mission in Mission.query.all():
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
                        'totalGames'])) if mission.shortName in faction['tieMission'].keys() else 0,
                    games=len(faction['bestMission'][mission.shortName]) if mission.shortName in faction['bestMission'].keys() else 0 + len(faction['worstMission'][mission.shortName]) if mission.shortName in faction['worstMission'].keys() else 0 + len(faction['tieMission'][mission.shortName]) if mission.shortName in faction['tieMission'].keys() else 0
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
                rate.games = len(faction['bestMission'][mission.shortName]) if mission.shortName in faction['bestMission'].keys() else 0 + len(faction['worstMission'][mission.shortName]) if mission.shortName in faction['worstMission'].keys() else 0 + len(faction['tieMission'][mission.shortName]) if mission.shortName in faction['tieMission'].keys() else 0
                db.session.add(rate)
        for secondary in Secondary.query.all():
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
                        'totalGames'])) if secondary.shortName in faction['tieSecondary'].keys() else 0,
                    games=len(faction['bestSecondary'][secondary.shortName]) if secondary.shortName in faction['bestSecondary'].keys() else 0
                + len(faction['worstSecondary'][secondary.shortName]) if secondary.shortName in faction['worstSecondary'].keys() else 0
                + len(faction['tieSecondary'][secondary.shortName]) if secondary.shortName in faction['tieSecondary'].keys() else 0
                ))
            else:
                rate = SecondaryRates.query.filter_by(fromUpdate=update.id).filter_by(faction=factionGl['sql'].id).filter_by(secondary=secondary.id).first()
                rate.rate1 = float("{:.2f}".format(len(faction['bestSecondary'][secondary.shortName]) * 100 / faction[
                    'totalGames'])) if secondary.shortName in faction['bestSecondary'].keys() else 0
                rate.rate2 = float("{:.2f}".format(len(faction['worstSecondary'][secondary.shortName]) * 100 / faction[
                    'totalGames'])) if secondary.shortName in faction['worstSecondary'].keys() else 0
                rate.rate3 = float("{:.2f}".format(len(faction['tieSecondary'][secondary.shortName]) * 100 / faction[
                    'totalGames'])) if secondary.shortName in faction['tieSecondary'].keys() else 0
                rate.games = len(faction['bestSecondary'][secondary.shortName]) if secondary.shortName in faction['bestSecondary'].keys() else 0
                + len(faction['worstSecondary'][secondary.shortName]) if secondary.shortName in faction['worstSecondary'].keys() else 0
                + len(faction['tieSecondary'][secondary.shortName]) if secondary.shortName in faction['tieSecondary'].keys() else 0
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
            if update.date <= game.date <=  update.dateEnd:
                faction['gamesWon'] += 1
                faction['totalGames'] += 1
        for game in factionGl['sql'].gamesLost:
            if update.date <= game.date <=  update.dateEnd:
                faction['gamesLost'] += 1
                faction['totalGames'] += 1
        for game in factionGl['sql'].gamesTied:
            if update.date <= game.date <=  update.dateEnd:
                faction['gamesTie'] += 1
                faction['totalGames'] += 1

        if faction['totalGames'] > 0:
            faction['winRate'] = float("{:.2f}".format(faction['gamesWon'] * 100 / faction['totalGames']))
        else:
            faction['winRate'] = 0.0
        try:
            faction['popularity'] = float("{:.2f}".format(faction['totalGames'] * 100 / (len(Game.query.filter(Game.date >= update.date).filter(Game.date <= update.dateEnd).all()) * 2)))
        except ZeroDivisionError:
            faction['popularity'] = 0

        if not glo:
            for rate in WinRates.query.filter_by(fromUpdate=update.id).filter_by(faction1=factionGl['sql'].id).order_by(desc(WinRates.rate1)).all():
                fct = Faction.query.filter_by(id=rate.faction2).first()
                faction['factionRates'].append({
                    'id': fct.id,
                    'name': fct.name,
                    'shortName': fct.shortName,
                    'winRate': rate.rate1 if rate.rate1 else 0,
                    'loseRate': rate.rate2 if rate.rate2 else 0,
                    'tieRate': rate.rate3 if rate.rate3 else 0,
                    'games': rate.games if rate.games else 0
                })
            for rate in MissionRates.query.filter_by(fromUpdate=update.id).filter_by(faction=factionGl['sql'].id).order_by(desc(MissionRates.rate1)).all():
                ms = Mission.query.filter_by(id=rate.mission).first()
                faction['missionRates'].append({
                    'id': ms.id,
                    'name': ms.name,
                    'shortName': ms.shortName,
                    'winRate': rate.rate1 if rate.rate1 else 0,
                    'loseRate': rate.rate2 if rate.rate2 else 0,
                    'tieRate': rate.rate3 if rate.rate3 else 0,
                    'games': rate.games if rate.games else 0
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
                    'tieRate': rate.rate3 if rate.rate3 else 0,
                    'games': rate.games if rate.games else 0
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
                    'tieRate': rate.rate3 if rate.rate3 else 0,
                    'games': rate.games if rate.games else 0
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
                'tieRate': rate.rate3 if rate.rate3 else 0,
                'games': rate.games if rate.games else 0
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
                'tieRate': rate.rate3 if rate.rate3 else 0,
                'games': rate.games if rate.games else 0
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
                'tieRate': rate.rate3 if rate.rate3 else 0,
                'games': rate.games if rate.games else 0
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
                'tieRate': rate.rate3 if rate.rate3 else 0,
                'games': rate.games if rate.games else 0
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