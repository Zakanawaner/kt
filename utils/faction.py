from sqlalchemy import extract, desc
from datetime import datetime
from collections import OrderedDict
from database import (
    Game, Player, Mission, Secondary, Faction,
    WinRates, MissionRates, SecondaryRates,
    PlayerWinRates, Update, GameType
)


############
# Factions #
def updateFactions(db):
    for faction in Faction.query.all():
        updateFaction(db, faction.id)


def updateFaction(db, fact):
    factionGl = {'sql': Faction.query.filter_by(id=fact).first(), 'updates': {}}
    for update in Update.query.all():
        faction = {}
        for gameType in GameType.query.all():
            gameTypeId = str(gameType.id)
            faction[gameTypeId] = {
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
                    if game.gameType == gameType.id or gameType.id == 0:
                        faction[gameTypeId]['totalGames'] += 1
                        faction[gameTypeId]['gamesWon'] += 1
                        for counter in Faction.query.all():
                            if game.losFaction[0] == counter:
                                if counter.name in faction[gameTypeId]['bestCounter'].keys():
                                    faction[gameTypeId]['bestCounter'][counter.name].append(game)
                                else:
                                    faction[gameTypeId]['bestCounter'][counter.name] = [game]
                                if counter.name not in faction[gameTypeId]['counterRates'].keys():
                                    faction[gameTypeId]['counterRates'][counter.name] = {
                                        'won': 0,
                                        'lost': 0,
                                        'tie': 0
                                    }
                                faction[gameTypeId]['counterRates'][counter.name]['won'] += 1
                        if game.mission[0].shortName in faction[gameTypeId]['bestMission'].keys():
                            faction[gameTypeId]['bestMission'][game.mission[0].shortName].append(game)
                        else:
                            faction[gameTypeId]['bestMission'][game.mission[0].shortName] = [game]
                        if game.winSecondaryFirst[0].shortName in faction[gameTypeId]['bestSecondary'].keys():
                            faction[gameTypeId]['bestSecondary'][game.winSecondaryFirst[0].shortName].append(game)
                        else:
                            faction[gameTypeId]['bestSecondary'][game.winSecondaryFirst[0].shortName] = [game]
                        if game.winSecondarySecond[0].shortName in faction[gameTypeId]['bestSecondary'].keys():
                            faction[gameTypeId]['bestSecondary'][game.winSecondarySecond[0].shortName].append(game)
                        else:
                            faction[gameTypeId]['bestSecondary'][game.winSecondarySecond[0].shortName] = [game]
                        if game.winSecondaryThird[0].shortName in faction[gameTypeId]['bestSecondary'].keys():
                            faction[gameTypeId]['bestSecondary'][game.winSecondaryThird[0].shortName].append(game)
                        else:
                            faction[gameTypeId]['bestSecondary'][game.winSecondaryThird[0].shortName] = [game]
            for game in factionGl['sql'].gamesLost:
                if update.date <= game.date <= update.dateEnd:
                    if game.gameType == gameType.id or gameType.id == 0:
                        faction[gameTypeId]['totalGames'] += 1
                        faction[gameTypeId]['gamesLost'] += 1
                        for counter in Faction.query.all():
                            if game.winFaction[0] == counter:
                                if counter.name not in faction[gameTypeId]['counterRates'].keys():
                                    if counter.name in faction[gameTypeId]['worstCounter'].keys():
                                        faction[gameTypeId]['worstCounter'][counter.name].append(game)
                                    else:
                                        faction[gameTypeId]['worstCounter'][counter.name] = [game]
                                    faction[gameTypeId]['counterRates'][counter.name] = {
                                        'won': 0,
                                        'lost': 0,
                                        'tie': 0
                                    }
                                    faction[gameTypeId]['counterRates'][counter.name]['lost'] += 1
                        if game.mission[0].shortName in faction[gameTypeId]['worstMission'].keys():
                            faction[gameTypeId]['worstMission'][game.mission[0].shortName].append(game)
                        else:
                            faction[gameTypeId]['worstMission'][game.mission[0].shortName] = [game]
                        if game.losSecondaryFirst[0].shortName in faction[gameTypeId]['worstSecondary'].keys():
                            faction[gameTypeId]['worstSecondary'][game.losSecondaryFirst[0].shortName].append(game)
                        else:
                            faction[gameTypeId]['worstSecondary'][game.losSecondaryFirst[0].shortName] = [game]
                        if game.losSecondarySecond[0].shortName in faction[gameTypeId]['worstSecondary'].keys():
                            faction[gameTypeId]['worstSecondary'][game.losSecondarySecond[0].shortName].append(game)
                        else:
                            faction[gameTypeId]['worstSecondary'][game.losSecondarySecond[0].shortName] = [game]
                        if game.losSecondaryThird[0].shortName in faction[gameTypeId]['worstSecondary'].keys():
                            faction[gameTypeId]['worstSecondary'][game.losSecondaryThird[0].shortName].append(game)
                        else:
                            faction[gameTypeId]['worstSecondary'][game.losSecondaryThird[0].shortName] = [game]
            for game in factionGl['sql'].gamesTied:
                if update.date <= game.date <= update.dateEnd:
                    if game.gameType == gameType.id or gameType.id == 0:
                        faction[gameTypeId]['totalGames'] += 1
                        faction[gameTypeId]['gamesTie'] += 1
                        for counter in Faction.query.all():
                            if game.winFaction[0] == counter or game.losFaction[0] == counter:
                                if counter.name not in faction[gameTypeId]['counterRates'].keys():
                                    if counter.name in faction[gameTypeId]['tieCounter'].keys():
                                        faction[gameTypeId]['tieCounter'][counter.name].append(game)
                                    else:
                                        faction[gameTypeId]['tieCounter'][counter.name] = [game]
                                    faction[gameTypeId]['counterRates'][counter.name] = {
                                        'won': 0,
                                        'lost': 0,
                                        'tie': 0
                                    }
                                    faction[gameTypeId]['counterRates'][counter.name]['tie'] += 1
                        if game.mission[0].shortName in faction[gameTypeId]['tieMission'].keys():
                            faction[gameTypeId]['tieMission'][game.mission[0].shortName].append(game)
                        else:
                            faction[gameTypeId]['tieMission'][game.mission[0].shortName] = [game]
                        if game.winSecondaryFirst[0].shortName in faction[gameTypeId]['tieSecondary'].keys():
                            faction[gameTypeId]['tieSecondary'][game.winSecondaryFirst[0].shortName].append(game)
                        else:
                            faction[gameTypeId]['tieSecondary'][game.winSecondaryFirst[0].shortName] = [game]
                        if game.winSecondarySecond[0].shortName in faction[gameTypeId]['tieSecondary'].keys():
                            faction[gameTypeId]['tieSecondary'][game.winSecondarySecond[0].shortName].append(game)
                        else:
                            faction[gameTypeId]['tieSecondary'][game.winSecondarySecond[0].shortName] = [game]
                        if game.winSecondaryThird[0].shortName in faction[gameTypeId]['tieSecondary'].keys():
                            faction[gameTypeId]['tieSecondary'][game.winSecondaryThird[0].shortName].append(game)
                        else:
                            faction[gameTypeId]['tieSecondary'][game.winSecondaryThird[0].shortName] = [game]
            if faction[gameTypeId]['totalGames'] > 0:
                faction[gameTypeId]['winRate'] = float("{:.2f}".format(faction[gameTypeId]['gamesWon'] * 100 / faction[gameTypeId]['totalGames']))
            else:
                faction[gameTypeId]['winRate'] = 0.0
            for counter in Faction.query.all():
                if counter.name in faction[gameTypeId]['counterRates'].keys():
                    totalFct = faction[gameTypeId]['counterRates'][counter.name]['won'] + faction[gameTypeId]['counterRates'][counter.name]['lost'] + faction[gameTypeId]['counterRates'][counter.name]['tie']
                    try:
                        faction[gameTypeId]['counterRates'][counter.name]["winRate"] = float("{:.2f}".format(faction[gameTypeId]['counterRates'][counter.name]['won'] * 100 / totalFct))
                        faction[gameTypeId]['counterRates'][counter.name]["loseRate"] = float("{:.2f}".format(faction[gameTypeId]['counterRates'][counter.name]['lost'] * 100 / totalFct))
                        faction[gameTypeId]['counterRates'][counter.name]["tieRate"] = float("{:.2f}".format(faction[gameTypeId]['counterRates'][counter.name]['tie'] * 100 / totalFct))
                    except ZeroDivisionError:
                        faction[gameTypeId]['counterRates'][counter.name]["winRate"] = 0
                        faction[gameTypeId]['counterRates'][counter.name]["loseRate"] = 0
                        faction[gameTypeId]['counterRates'][counter.name]["tieRate"] = 0
                    rate = WinRates.query.filter_by(fromUpdate=update.id).filter_by(fromGameType=gameType.id).filter_by(faction1=factionGl['sql'].id).filter_by(faction2=counter.id).first()
                    if not rate:
                        rate = WinRates(
                            faction1=factionGl['sql'].id,
                            fromUpdate=update.id,
                            fromGameType=gameType.id,
                            faction2=counter.id
                        )
                    rate.rate1 = faction[gameTypeId]['counterRates'][counter.name]['winRate']
                    rate.rate2 = faction[gameTypeId]['counterRates'][counter.name]['loseRate']
                    rate.rate3 = faction[gameTypeId]['counterRates'][counter.name]['tieRate']
                    rate.games = faction[gameTypeId]['counterRates'][counter.name]['won'] + faction[gameTypeId]['counterRates'][counter.name]['lost'] + faction[gameTypeId]['counterRates'][counter.name]['tie']
                    db.session.add(rate)
            for mission in Mission.query.all():
                if mission.shortName in faction[gameTypeId]['bestMission'].keys():
                    bg = len(faction[gameTypeId]['bestMission'][mission.shortName])
                else:
                    bg = 0
                if mission.shortName in faction[gameTypeId]['worstMission'].keys():
                    wg = len(faction[gameTypeId]['worstMission'][mission.shortName])
                else:
                    wg = 0
                if mission.shortName in faction[gameTypeId]['tieMission'].keys():
                    tg = len(faction[gameTypeId]['tieMission'][mission.shortName])
                else:
                    tg = 0
                if (bg + wg + tg) > 0:
                    rate = MissionRates.query.filter_by(fromUpdate=update.id).filter_by(fromGameType=gameType.id).filter_by(faction=factionGl['sql'].id).filter_by(mission=mission.id).first()
                    if not rate:
                        rate = MissionRates(
                            faction=factionGl['sql'].id,
                            fromUpdate=update.id,
                            fromGameType=gameType.id,
                            mission=mission.id
                        )
                    try:
                        if mission.shortName in faction[gameTypeId]['bestMission'].keys():
                            rate.rate1 = float("{:.2f}".format(len(faction[gameTypeId]['bestMission'][mission.shortName]) * 100 / (bg + wg + tg)))
                        else:
                            rate.rate1 = 0
                        if mission.shortName in faction[gameTypeId]['worstMission'].keys():
                            rate.rate2 = float("{:.2f}".format(len(faction[gameTypeId]['worstMission'][mission.shortName]) * 100 / (bg + wg + tg)))
                        else:
                            rate.rate2 = 0
                        if mission.shortName in faction[gameTypeId]['tieMission'].keys():
                            rate.rate3 = float("{:.2f}".format(len(faction[gameTypeId]['tieMission'][mission.shortName]) * 100 / (bg + wg + tg)))
                        else:
                            rate.rate3 = 0
                    except ZeroDivisionError:
                        rate.rate1 = 0
                        rate.rate2 = 0
                        rate.rate3 = 0
                    rate.games = bg + wg + tg
                    db.session.add(rate)
            for secondary in Secondary.query.all():
                if secondary.shortName in faction[gameTypeId]['bestSecondary'].keys():
                    bg = len(faction[gameTypeId]['bestSecondary'][secondary.shortName])
                else:
                    bg = 0
                if secondary.shortName in faction[gameTypeId]['worstSecondary'].keys():
                    wg = len(faction[gameTypeId]['worstSecondary'][secondary.shortName])
                else:
                    wg = 0
                if secondary.shortName in faction[gameTypeId]['tieSecondary'].keys():
                    tg = len(faction[gameTypeId]['tieSecondary'][secondary.shortName])
                else:
                    tg = 0
                if (bg + wg + tg) > 0:
                    rate = SecondaryRates.query.filter_by(fromUpdate=update.id).filter_by(fromGameType=gameType.id).filter_by(faction=factionGl['sql'].id).filter_by(secondary=secondary.id).first()
                    if not rate:
                        rate = SecondaryRates(
                            faction=factionGl['sql'].id,
                            fromUpdate=update.id,
                            fromGameType=gameType.id,
                            secondary=secondary.id
                        )
                    try:
                        if secondary.shortName in faction[gameTypeId]['bestSecondary'].keys():
                            rate.rate1 = float("{:.2f}".format(len(faction[gameTypeId]['bestSecondary'][secondary.shortName]) * 100 / (bg + wg + tg)))
                        else:
                            rate.rate1 = 0
                        if secondary.shortName in faction[gameTypeId]['worstSecondary'].keys():
                            rate.rate2 = float("{:.2f}".format(len(faction[gameTypeId]['worstSecondary'][secondary.shortName]) * 100 / (bg + wg + tg)))
                        else:
                            rate.rate2 = 0
                        if secondary.shortName in faction[gameTypeId]['tieSecondary'].keys():
                            rate.rate3 = float("{:.2f}".format(len(faction[gameTypeId]['tieSecondary'][secondary.shortName]) * 100 / (bg + wg + tg)))
                        else:
                            rate.rate3 = 0
                    except ZeroDivisionError:
                        rate.rate1 = 0
                        rate.rate2 = 0
                        rate.rate3 = 0
                    rate.games = bg + wg + tg
                    db.session.add(rate)
        factionGl['updates'][str(update.id)] = faction
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
        faction = {}
        for gameType in GameType.query.all():
            gameTypeId = str(gameType.id)
            faction[gameTypeId] = {
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
                if update.date <= game.date <= update.dateEnd:
                    faction[gameTypeId]['gamesWon'] += 1
                    faction[gameTypeId]['totalGames'] += 1
            for game in factionGl['sql'].gamesLost:
                if update.date <= game.date <= update.dateEnd:
                    faction[gameTypeId]['gamesLost'] += 1
                    faction[gameTypeId]['totalGames'] += 1
            for game in factionGl['sql'].gamesTied:
                if update.date <= game.date <= update.dateEnd:
                    faction[gameTypeId]['gamesTie'] += 1
                    faction[gameTypeId]['totalGames'] += 1

            if faction[gameTypeId]['totalGames'] > 0:
                faction[gameTypeId]['winRate'] = float("{:.2f}".format(faction[gameTypeId]['gamesWon'] * 100 / faction[gameTypeId]['totalGames']))
            else:
                faction[gameTypeId]['winRate'] = 0.0
            try:
                faction[gameTypeId]['popularity'] = float("{:.2f}".format(faction[gameTypeId]['totalGames'] * 50 / len(Game.query.filter(Game.date >= update.date).filter(Game.date <= update.dateEnd).all())))
            except ZeroDivisionError:
                faction[gameTypeId]['popularity'] = 0

            if not glo:
                for rate in WinRates.query.filter_by(fromUpdate=update.id).filter_by(fromGameType=gameType.id).filter_by(faction1=factionGl['sql'].id).order_by(desc(WinRates.rate1)).all():
                    fct = Faction.query.filter_by(id=rate.faction2).first()
                    faction[gameTypeId]['factionRates'].append({
                        'id': fct.id,
                        'name': fct.name,
                        'shortName': fct.shortName,
                        'winRate': rate.rate1 if rate.rate1 else 0,
                        'loseRate': rate.rate2 if rate.rate2 else 0,
                        'tieRate': rate.rate3 if rate.rate3 else 0,
                        'games': rate.games if rate.games else 0
                    })
                for rate in MissionRates.query.filter_by(fromUpdate=update.id).filter_by(fromGameType=gameType.id).filter_by(faction=factionGl['sql'].id).order_by(desc(MissionRates.rate1)).all():
                    ms = Mission.query.filter_by(id=rate.mission).first()
                    faction[gameTypeId]['missionRates'].append({
                        'id': ms.id,
                        'name': ms.name,
                        'shortName': ms.shortName,
                        'winRate': rate.rate1 if rate.rate1 else 0,
                        'loseRate': rate.rate2 if rate.rate2 else 0,
                        'tieRate': rate.rate3 if rate.rate3 else 0,
                        'games': rate.games if rate.games else 0
                    })
                for rate in SecondaryRates.query.filter_by(fromUpdate=update.id).filter_by(fromGameType=gameType.id).filter_by(faction=factionGl['sql'].id).order_by(
                        desc(SecondaryRates.rate1)).all():
                    sec = Secondary.query.filter_by(id=rate.secondary).first()
                    faction[gameTypeId]['secondaryRates'].append({
                        'id': sec.id,
                        'name': sec.name,
                        'shortName': sec.shortName,
                        'winRate': rate.rate1 if rate.rate1 else 0,
                        'loseRate': rate.rate2 if rate.rate2 else 0,
                        'tieRate': rate.rate3 if rate.rate3 else 0,
                        'games': rate.games if rate.games else 0
                    })
                for rate in PlayerWinRates.query.filter_by(fromUpdate=update.id).filter_by(fromGameType=gameType.id).filter_by(faction=factionGl['sql'].id).order_by(
                        desc(PlayerWinRates.rate1)).all():
                    pl = Player.query.filter_by(id=rate.player).first()
                    faction[gameTypeId]['playerRates'].append({
                        'id': pl.id,
                        'name': pl.username,
                        'shortName': pl.shortName,
                        'winRate': rate.rate1 if rate.rate1 else 0,
                        'loseRate': rate.rate2 if rate.rate2 else 0,
                        'tieRate': rate.rate3 if rate.rate3 else 0,
                        'games': rate.games if rate.games else 0
                    })
                faction[gameTypeId]['games'] = {}
                faction[gameTypeId]['maxGames'] = 0
                for i in range(0, 12):
                    if datetime.now().month - i < 1:
                        month = datetime.now().month - i + 12
                        year = datetime.now().year - 1
                    else:
                        month = datetime.now().month - i
                        year = datetime.now().year
                    faction[gameTypeId]['games'][str(month) + '-' + str(year)] = 0
                    for game in Game.query.filter(extract('month', Game.date) == month).filter(
                            extract('year', Game.date) == year).all():
                        if game.losFaction[0] == factionGl['sql'] or game.winFaction[0] == factionGl['sql']:
                            faction[gameTypeId]['games'][str(month) + '-' + str(year)] += 1
                    faction[gameTypeId]['maxGames'] = faction[gameTypeId]['games'][str(month) + '-' + str(year)] if faction[gameTypeId]['maxGames'] < \
                                                                                            faction[gameTypeId]['games'][
                                                                                                str(month) + '-' + str(
                                                                                                    year)] else faction[gameTypeId][
                        'maxGames']
                faction[gameTypeId]['games'] = dict(OrderedDict(reversed(list(faction[gameTypeId]['games'].items()))))
            else:
                if WinRates.query.filter_by(fromUpdate=update.id).filter_by(fromGameType=gameType.id).filter_by(faction1=factionGl['sql'].id).order_by(desc(WinRates.rate1)).first():
                    faction[gameTypeId]['winnerRates'].append(Faction.query.filter_by(
                        id=WinRates.query.filter_by(fromUpdate=update.id).filter_by(fromGameType=gameType.id).filter_by(faction1=factionGl['sql'].id).order_by(
                            desc(WinRates.rate1)).first().faction2).first())
                if WinRates.query.filter_by(fromUpdate=update.id).filter_by(fromGameType=gameType.id).filter_by(faction1=factionGl['sql'].id).order_by(desc(WinRates.rate2)).first():
                    faction[gameTypeId]['loserRates'].append(Faction.query.filter_by(
                        id=WinRates.query.filter_by(fromUpdate=update.id).filter_by(fromGameType=gameType.id).filter_by(faction1=factionGl['sql'].id).order_by(
                            desc(WinRates.rate2)).first().faction2).first())
                if MissionRates.query.filter_by(fromUpdate=update.id).filter_by(fromGameType=gameType.id).filter_by(faction=factionGl['sql'].id).order_by(desc(MissionRates.rate1)).first():
                    faction[gameTypeId]['bestMissions'].append(Mission.query.filter_by(
                        id=MissionRates.query.filter_by(fromUpdate=update.id).filter_by(fromGameType=gameType.id).filter_by(faction=factionGl['sql'].id).order_by(
                            desc(MissionRates.rate1)).first().mission).first())
                if SecondaryRates.query.filter_by(fromUpdate=update.id).filter_by(fromGameType=gameType.id).filter_by(faction=factionGl['sql'].id).order_by(desc(SecondaryRates.rate1)).first():
                    faction[gameTypeId]['bestSecondaries'].append(Secondary.query.filter_by(
                        id=SecondaryRates.query.filter_by(fromUpdate=update.id).filter_by(fromGameType=gameType.id).filter_by(faction=factionGl['sql'].id).order_by(
                            desc(SecondaryRates.rate1)).first().secondary).first())
        factionGl['updates'][str(update.id)] = faction
    return factionGl
