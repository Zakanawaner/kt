from sqlalchemy import extract, desc
from datetime import datetime
from collections import OrderedDict
from database import (
    Game, Player, Mission, Secondary, Faction,
    WinRates, MissionRates, SecondaryRates,
    PlayerWinRates, Update, GameType, Edition
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
        for edition in Edition.query.all():
            editionId = str(edition.id)
            faction[editionId] = {}
            for gameType in GameType.query.all():
                gameTypeId = str(gameType.id)
                faction[editionId][gameTypeId] = {
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
                    if game.update == update.id or update.id == 1:
                        if game.edition == edition.id or edition.id == 1:
                            if game.gameType == gameType.id or gameType.id == 1:
                                faction[editionId][gameTypeId]['totalGames'] += 1
                                faction[editionId][gameTypeId]['gamesWon'] += 1
                                for counter in Faction.query.all():
                                    if game.losFaction[0] == counter:
                                        if counter.name in faction[editionId][gameTypeId]['bestCounter'].keys():
                                            faction[editionId][gameTypeId]['bestCounter'][counter.name].append(game)
                                        else:
                                            faction[editionId][gameTypeId]['bestCounter'][counter.name] = [game]
                                        if counter.name not in faction[editionId][gameTypeId]['counterRates'].keys():
                                            faction[editionId][gameTypeId]['counterRates'][counter.name] = {
                                                'won': 0,
                                                'lost': 0,
                                                'tie': 0
                                            }
                                        faction[editionId][gameTypeId]['counterRates'][counter.name]['won'] += 1
                                if game.mission[0].shortName in faction[editionId][gameTypeId]['bestMission'].keys():
                                    faction[editionId][gameTypeId]['bestMission'][game.mission[0].shortName].append(game)
                                else:
                                    faction[editionId][gameTypeId]['bestMission'][game.mission[0].shortName] = [game]
                                if game.winSecondaryFirst[0].shortName in faction[editionId][gameTypeId]['bestSecondary'].keys():
                                    faction[editionId][gameTypeId]['bestSecondary'][game.winSecondaryFirst[0].shortName].append(game)
                                else:
                                    faction[editionId][gameTypeId]['bestSecondary'][game.winSecondaryFirst[0].shortName] = [game]
                                if game.winSecondarySecond[0].shortName in faction[editionId][gameTypeId]['bestSecondary'].keys():
                                    faction[editionId][gameTypeId]['bestSecondary'][game.winSecondarySecond[0].shortName].append(game)
                                else:
                                    faction[editionId][gameTypeId]['bestSecondary'][game.winSecondarySecond[0].shortName] = [game]
                                if game.winSecondaryThird[0].shortName in faction[editionId][gameTypeId]['bestSecondary'].keys():
                                    faction[editionId][gameTypeId]['bestSecondary'][game.winSecondaryThird[0].shortName].append(game)
                                else:
                                    faction[editionId][gameTypeId]['bestSecondary'][game.winSecondaryThird[0].shortName] = [game]
                for game in factionGl['sql'].gamesLost:
                    if game.update == update.id or update.id == 1:
                        if game.edition == edition.id or edition.id == 1:
                            if game.gameType == gameType.id or gameType.id == 1:
                                faction[editionId][gameTypeId]['totalGames'] += 1
                                faction[editionId][gameTypeId]['gamesLost'] += 1
                                for counter in Faction.query.all():
                                    if game.winFaction[0] == counter:
                                        if counter.name not in faction[editionId][gameTypeId]['counterRates'].keys():
                                            if counter.name in faction[editionId][gameTypeId]['worstCounter'].keys():
                                                faction[editionId][gameTypeId]['worstCounter'][counter.name].append(game)
                                            else:
                                                faction[editionId][gameTypeId]['worstCounter'][counter.name] = [game]
                                            faction[editionId][gameTypeId]['counterRates'][counter.name] = {
                                                'won': 0,
                                                'lost': 0,
                                                'tie': 0
                                            }
                                            faction[editionId][gameTypeId]['counterRates'][counter.name]['lost'] += 1
                                if game.mission[0].shortName in faction[editionId][gameTypeId]['worstMission'].keys():
                                    faction[editionId][gameTypeId]['worstMission'][game.mission[0].shortName].append(game)
                                else:
                                    faction[editionId][gameTypeId]['worstMission'][game.mission[0].shortName] = [game]
                                if game.losSecondaryFirst[0].shortName in faction[editionId][gameTypeId]['worstSecondary'].keys():
                                    faction[editionId][gameTypeId]['worstSecondary'][game.losSecondaryFirst[0].shortName].append(game)
                                else:
                                    faction[editionId][gameTypeId]['worstSecondary'][game.losSecondaryFirst[0].shortName] = [game]
                                if game.losSecondarySecond[0].shortName in faction[editionId][gameTypeId]['worstSecondary'].keys():
                                    faction[editionId][gameTypeId]['worstSecondary'][game.losSecondarySecond[0].shortName].append(game)
                                else:
                                    faction[editionId][gameTypeId]['worstSecondary'][game.losSecondarySecond[0].shortName] = [game]
                                if game.losSecondaryThird[0].shortName in faction[editionId][gameTypeId]['worstSecondary'].keys():
                                    faction[editionId][gameTypeId]['worstSecondary'][game.losSecondaryThird[0].shortName].append(game)
                                else:
                                    faction[editionId][gameTypeId]['worstSecondary'][game.losSecondaryThird[0].shortName] = [game]
                for game in factionGl['sql'].gamesTied:
                    if game.update == update.id or update.id == 1:
                        if game.edition == edition.id or edition.id == 1:
                            if game.gameType == gameType.id or gameType.id == 1:
                                faction[editionId][gameTypeId]['totalGames'] += 1
                                faction[editionId][gameTypeId]['gamesTie'] += 1
                                for counter in Faction.query.all():
                                    if (game.winFaction[0] == counter and counter != factionGl['sql']) or (game.losFaction[0] == counter and counter != factionGl['sql']):
                                        if counter.name not in faction[editionId][gameTypeId]['counterRates'].keys():
                                            if counter.name in faction[editionId][gameTypeId]['tieCounter'].keys():
                                                faction[editionId][gameTypeId]['tieCounter'][counter.name].append(game)
                                            else:
                                                faction[editionId][gameTypeId]['tieCounter'][counter.name] = [game]
                                            faction[editionId][gameTypeId]['counterRates'][counter.name] = {
                                                'won': 0,
                                                'lost': 0,
                                                'tie': 0
                                            }
                                            faction[editionId][gameTypeId]['counterRates'][counter.name]['tie'] += 1
                                    elif game.winFaction == game.losFaction:
                                        if counter.name not in faction[editionId][gameTypeId]['counterRates'].keys():
                                            if counter.name in faction[editionId][gameTypeId]['tieCounter'].keys():
                                                faction[editionId][gameTypeId]['tieCounter'][counter.name].append(game)
                                            else:
                                                faction[editionId][gameTypeId]['tieCounter'][counter.name] = [game]
                                            faction[editionId][gameTypeId]['counterRates'][counter.name] = {
                                                'won': 0,
                                                'lost': 0,
                                                'tie': 0
                                            }
                                            faction[editionId][gameTypeId]['counterRates'][counter.name]['tie'] += 2
                                if game.mission[0].shortName in faction[editionId][gameTypeId]['tieMission'].keys():
                                    faction[editionId][gameTypeId]['tieMission'][game.mission[0].shortName].append(game)
                                else:
                                    faction[editionId][gameTypeId]['tieMission'][game.mission[0].shortName] = [game]
                                if game.winSecondaryFirst[0].shortName in faction[editionId][gameTypeId]['tieSecondary'].keys():
                                    faction[editionId][gameTypeId]['tieSecondary'][game.winSecondaryFirst[0].shortName].append(game)
                                else:
                                    faction[editionId][gameTypeId]['tieSecondary'][game.winSecondaryFirst[0].shortName] = [game]
                                if game.winSecondarySecond[0].shortName in faction[editionId][gameTypeId]['tieSecondary'].keys():
                                    faction[editionId][gameTypeId]['tieSecondary'][game.winSecondarySecond[0].shortName].append(game)
                                else:
                                    faction[editionId][gameTypeId]['tieSecondary'][game.winSecondarySecond[0].shortName] = [game]
                                if game.winSecondaryThird[0].shortName in faction[editionId][gameTypeId]['tieSecondary'].keys():
                                    faction[editionId][gameTypeId]['tieSecondary'][game.winSecondaryThird[0].shortName].append(game)
                                else:
                                    faction[editionId][gameTypeId]['tieSecondary'][game.winSecondaryThird[0].shortName] = [game]
                if faction[editionId][gameTypeId]['totalGames'] > 0:
                    faction[editionId][gameTypeId]['winRate'] = float("{:.2f}".format(faction[editionId][gameTypeId]['gamesWon'] * 100 / faction[editionId][gameTypeId]['totalGames']))
                else:
                    faction[editionId][gameTypeId]['winRate'] = 0.0
                for counter in Faction.query.all():
                    if counter.name in faction[editionId][gameTypeId]['counterRates'].keys():
                        totalFct = faction[editionId][gameTypeId]['counterRates'][counter.name]['won'] + faction[editionId][gameTypeId]['counterRates'][counter.name]['lost'] + faction[editionId][gameTypeId]['counterRates'][counter.name]['tie']
                        try:
                            faction[editionId][gameTypeId]['counterRates'][counter.name]["winRate"] = float("{:.2f}".format(faction[editionId][gameTypeId]['counterRates'][counter.name]['won'] * 100 / totalFct))
                            faction[editionId][gameTypeId]['counterRates'][counter.name]["loseRate"] = float("{:.2f}".format(faction[editionId][gameTypeId]['counterRates'][counter.name]['lost'] * 100 / totalFct))
                            faction[editionId][gameTypeId]['counterRates'][counter.name]["tieRate"] = float("{:.2f}".format(faction[editionId][gameTypeId]['counterRates'][counter.name]['tie'] * 100 / totalFct))
                        except ZeroDivisionError:
                            faction[editionId][gameTypeId]['counterRates'][counter.name]["winRate"] = 0
                            faction[editionId][gameTypeId]['counterRates'][counter.name]["loseRate"] = 0
                            faction[editionId][gameTypeId]['counterRates'][counter.name]["tieRate"] = 0
                        rate = WinRates.query.filter_by(fromUpdate=update.id).filter_by(fromEdition=edition.id).filter_by(fromGameType=gameType.id).filter_by(faction1=factionGl['sql'].id).filter_by(faction2=counter.id).first()
                        if not rate:
                            rate = WinRates(
                                faction1=factionGl['sql'].id,
                                fromUpdate=update.id,
                                fromEdition=edition.id,
                                fromGameType=gameType.id,
                                faction2=counter.id
                            )
                        rate.rate1 = faction[editionId][gameTypeId]['counterRates'][counter.name]['winRate']
                        rate.rate2 = faction[editionId][gameTypeId]['counterRates'][counter.name]['loseRate']
                        rate.rate3 = faction[editionId][gameTypeId]['counterRates'][counter.name]['tieRate']
                        rate.games = faction[editionId][gameTypeId]['counterRates'][counter.name]['won'] + faction[editionId][gameTypeId]['counterRates'][counter.name]['lost'] + faction[editionId][gameTypeId]['counterRates'][counter.name]['tie']
                        db.session.add(rate)
                for mission in Mission.query.all():
                    if mission.shortName in faction[editionId][gameTypeId]['bestMission'].keys():
                        bg = len(faction[editionId][gameTypeId]['bestMission'][mission.shortName])
                    else:
                        bg = 0
                    if mission.shortName in faction[editionId][gameTypeId]['worstMission'].keys():
                        wg = len(faction[editionId][gameTypeId]['worstMission'][mission.shortName])
                    else:
                        wg = 0
                    if mission.shortName in faction[editionId][gameTypeId]['tieMission'].keys():
                        tg = len(faction[editionId][gameTypeId]['tieMission'][mission.shortName])
                    else:
                        tg = 0
                    if (bg + wg + tg) > 0:
                        rate = MissionRates.query.filter_by(fromUpdate=update.id).filter_by(fromEdition=edition.id).filter_by(fromGameType=gameType.id).filter_by(faction=factionGl['sql'].id).filter_by(mission=mission.id).first()
                        if not rate:
                            rate = MissionRates(
                                faction=factionGl['sql'].id,
                                fromUpdate=update.id,
                                fromEdition=edition.id,
                                fromGameType=gameType.id,
                                mission=mission.id
                            )
                        try:
                            if mission.shortName in faction[editionId][gameTypeId]['bestMission'].keys():
                                rate.rate1 = float("{:.2f}".format(len(faction[editionId][gameTypeId]['bestMission'][mission.shortName]) * 100 / (bg + wg + tg)))
                            else:
                                rate.rate1 = 0
                            if mission.shortName in faction[editionId][gameTypeId]['worstMission'].keys():
                                rate.rate2 = float("{:.2f}".format(len(faction[editionId][gameTypeId]['worstMission'][mission.shortName]) * 100 / (bg + wg + tg)))
                            else:
                                rate.rate2 = 0
                            if mission.shortName in faction[editionId][gameTypeId]['tieMission'].keys():
                                rate.rate3 = float("{:.2f}".format(len(faction[editionId][gameTypeId]['tieMission'][mission.shortName]) * 100 / (bg + wg + tg)))
                            else:
                                rate.rate3 = 0
                        except ZeroDivisionError:
                            rate.rate1 = 0
                            rate.rate2 = 0
                            rate.rate3 = 0
                        rate.games = bg + wg + tg
                        db.session.add(rate)
                for secondary in Secondary.query.all():
                    if secondary.shortName in faction[editionId][gameTypeId]['bestSecondary'].keys():
                        bg = len(faction[editionId][gameTypeId]['bestSecondary'][secondary.shortName])
                    else:
                        bg = 0
                    if secondary.shortName in faction[editionId][gameTypeId]['worstSecondary'].keys():
                        wg = len(faction[editionId][gameTypeId]['worstSecondary'][secondary.shortName])
                    else:
                        wg = 0
                    if secondary.shortName in faction[editionId][gameTypeId]['tieSecondary'].keys():
                        tg = len(faction[editionId][gameTypeId]['tieSecondary'][secondary.shortName])
                    else:
                        tg = 0
                    if (bg + wg + tg) > 0:
                        rate = SecondaryRates.query.filter_by(fromUpdate=update.id).filter_by(fromEdition=edition.id).filter_by(fromGameType=gameType.id).filter_by(faction=factionGl['sql'].id).filter_by(secondary=secondary.id).first()
                        if not rate:
                            rate = SecondaryRates(
                                faction=factionGl['sql'].id,
                                fromUpdate=update.id,
                                fromEdition=edition.id,
                                fromGameType=gameType.id,
                                secondary=secondary.id
                            )
                        try:
                            if secondary.shortName in faction[editionId][gameTypeId]['bestSecondary'].keys():
                                rate.rate1 = float("{:.2f}".format(len(faction[editionId][gameTypeId]['bestSecondary'][secondary.shortName]) * 100 / (bg + wg + tg)))
                            else:
                                rate.rate1 = 0
                            if secondary.shortName in faction[editionId][gameTypeId]['worstSecondary'].keys():
                                rate.rate2 = float("{:.2f}".format(len(faction[editionId][gameTypeId]['worstSecondary'][secondary.shortName]) * 100 / (bg + wg + tg)))
                            else:
                                rate.rate2 = 0
                            if secondary.shortName in faction[editionId][gameTypeId]['tieSecondary'].keys():
                                rate.rate3 = float("{:.2f}".format(len(faction[editionId][gameTypeId]['tieSecondary'][secondary.shortName]) * 100 / (bg + wg + tg)))
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


def getFactions(up, tp, ed):
    factions = {}
    for faction in Faction.query.all():
        factionInd = getFaction(faction.id, up, tp, ed, glo=True)
        factions[factionInd['sql'].shortName] = factionInd
    return [faction for faction in factions.values()]


def getFaction(fact, up, tp, ed, glo=False):
    factionGl = {
        'sql': Faction.query.filter_by(id=fact).first(),
        'rates': {}
    }
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
        if (up == game.update or up == 1) and (ed == game.edition or ed == 1) and (tp == game.gameType or tp == 1):
            faction['gamesWon'] += 1
            faction['totalGames'] += 1
    for game in factionGl['sql'].gamesLost:
        if (up == game.update or up == 1) and (ed == game.edition or ed == 1) and (tp == game.gameType or tp == 1):
            faction['gamesLost'] += 1
            faction['totalGames'] += 1
    for game in factionGl['sql'].gamesTied:
        if (up == game.update or up == 1) and (ed == game.edition or ed == 1) and (tp == game.gameType or tp == 1):
            faction['gamesTie'] += 1
            faction['totalGames'] += 1
    if faction['totalGames'] > 0:
        faction['winRate'] = float("{:.2f}".format(faction['gamesWon'] * 100 / faction['totalGames']))
    else:
        faction['winRate'] = 0.0
    try:
        faction['popularity'] = float("{:.2f}".format(faction['totalGames'] * 50 / len(Game.query.filter(Game.update == up if up > 1 else Game.update).filter(Game.edition == ed if ed > 1 else Game.edition).filter(Game.gameType == tp if tp > 1 else Game.gameType).all())))
    except ZeroDivisionError:
        faction['popularity'] = 0

    if not glo:
        for rate in WinRates.query.filter_by(fromUpdate=up).filter_by(fromEdition=ed).filter_by(fromGameType=tp).filter_by(faction1=factionGl['sql'].id).order_by(desc(WinRates.rate1)).all():
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
        for rate in MissionRates.query.filter_by(fromUpdate=up).filter_by(fromEdition=ed).filter_by(fromGameType=tp).filter_by(faction=factionGl['sql'].id).order_by(desc(MissionRates.rate1)).all():
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
        for rate in SecondaryRates.query.filter_by(fromUpdate=up).filter_by(fromEdition=ed).filter_by(fromGameType=tp).filter_by(faction=factionGl['sql'].id).order_by(desc(SecondaryRates.rate1)).all():
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
        for rate in PlayerWinRates.query.filter_by(fromUpdate=up).filter_by(fromEdition=ed).filter_by(fromGameType=tp).filter_by(faction=factionGl['sql'].id).order_by(
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
        winRate = WinRates.query.filter_by(fromUpdate=up).filter_by(fromEdition=ed).filter_by(fromGameType=tp).filter_by(faction1=factionGl['sql'].id).order_by(desc(WinRates.rate1)).first()
        loseRate = WinRates.query.filter_by(fromUpdate=up).filter_by(fromEdition=ed).filter_by(fromGameType=tp).filter_by(faction1=factionGl['sql'].id).order_by(desc(WinRates.rate2)).first()
        missionRate = MissionRates.query.filter_by(fromUpdate=up).filter_by(fromEdition=ed).filter_by(fromGameType=tp).filter_by(faction=factionGl['sql'].id).order_by(desc(MissionRates.rate1)).first()
        secondaryRate = SecondaryRates.query.filter_by(fromUpdate=up).filter_by(fromEdition=ed).filter_by(fromGameType=tp).filter_by(faction=factionGl['sql'].id).order_by(desc(SecondaryRates.rate1)).first()
        if winRate:
            faction['winnerRates'].append(Faction.query.filter_by(id=winRate.faction2).first())
        if loseRate:
            faction['loserRates'].append(Faction.query.filter_by(id=loseRate.faction2).first())
        if missionRate:
            faction['bestMissions'].append(Mission.query.filter_by(id=missionRate.mission).first())
        if secondaryRate:
            faction['bestSecondaries'].append(Secondary.query.filter_by(id=secondaryRate.secondary).first())
    factionGl['rates'] = faction
    return factionGl
