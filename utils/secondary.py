from database import Secondary, Update, Game, Faction, SecondaryRates, GameType, Edition
from sqlalchemy import extract, desc
from datetime import datetime
from collections import OrderedDict


###############
# Secondaries #
def updateSecondaries(db):
    for secondary in Secondary.query.all():
        updateSecondary(db, secondary.id)


def updateSecondary(db, sc):
    secondaryGl = {
        'sql': Secondary.query.filter_by(id=sc).first(),
        'updates': {},
    }
    for update in Update.query.all():
        secondary = {}
        for edition in Edition.query.all():
            editionId = str(edition.id)
            secondary[editionId] = {}
            for gameType in GameType.query.all():
                gameTypeId = str(gameType.id)
                secondary[editionId][gameTypeId] = {
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
                        Game.update == update.id if update.id > 1 else Game.update).filter(
                        Game.gameType == gameType.id if gameType.id > 1 else Game.gameType).filter(
                        Game.edition == edition.id if edition.id > 1 else Game.edition).all():
                    if secondaryGl['sql'] in game.winSecondaryFirst:
                        secondary[editionId][gameTypeId]['totalGames'] += 1
                        secondary[editionId][gameTypeId]['totalScore'] += game.winSecondaryFirstScore
                        secondary[editionId][gameTypeId]['totalScoreFirst'] += game.winSecondaryFirstScoreTurn1 if game.winSecondaryFirstScoreTurn1 else 0
                        secondary[editionId][gameTypeId]['totalScoreSecond'] += game.winSecondaryFirstScoreTurn2 if game.winSecondaryFirstScoreTurn2 else 0
                        secondary[editionId][gameTypeId]['totalScoreThird'] += game.winSecondaryFirstScoreTurn3 if game.winSecondaryFirstScoreTurn3 else 0
                        secondary[editionId][gameTypeId]['totalScoreFourth'] += game.winSecondaryFirstScoreTurn4 if game.winSecondaryFirstScoreTurn4 else 0
                    if secondaryGl['sql'] in game.winSecondarySecond:
                        secondary[editionId][gameTypeId]['totalGames'] += 1
                        secondary[editionId][gameTypeId]['totalScore'] += game.winSecondarySecondScore
                        secondary[editionId][gameTypeId]['totalScoreFirst'] += game.winSecondarySecondScoreTurn1 if game.winSecondarySecondScoreTurn1 else 0
                        secondary[editionId][gameTypeId]['totalScoreSecond'] += game.winSecondarySecondScoreTurn2 if game.winSecondarySecondScoreTurn2 else 0
                        secondary[editionId][gameTypeId]['totalScoreThird'] += game.winSecondarySecondScoreTurn3 if game.winSecondarySecondScoreTurn3 else 0
                        secondary[editionId][gameTypeId]['totalScoreFourth'] += game.winSecondarySecondScoreTurn4 if game.winSecondarySecondScoreTurn4 else 0
                    if secondaryGl['sql'] in game.winSecondaryThird:
                        secondary[editionId][gameTypeId]['totalGames'] += 1
                        secondary[editionId][gameTypeId]['totalScore'] += game.winSecondaryThirdScore
                        secondary[editionId][gameTypeId]['totalScoreFirst'] += game.winSecondaryThirdScoreTurn1 if game.winSecondaryThirdScoreTurn1 else 0
                        secondary[editionId][gameTypeId]['totalScoreSecond'] += game.winSecondaryThirdScoreTurn2 if game.winSecondaryThirdScoreTurn2 else 0
                        secondary[editionId][gameTypeId]['totalScoreThird'] += game.winSecondaryThirdScoreTurn3 if game.winSecondaryThirdScoreTurn3 else 0
                        secondary[editionId][gameTypeId]['totalScoreFourth'] += game.winSecondaryThirdScoreTurn4 if game.winSecondaryThirdScoreTurn4 else 0
                    if secondaryGl['sql'] in game.losSecondaryFirst:
                        secondary[editionId][gameTypeId]['totalGames'] += 1
                        secondary[editionId][gameTypeId]['totalScore'] += game.losSecondaryFirstScore
                        secondary[editionId][gameTypeId]['totalScoreFirst'] += game.losSecondaryFirstScoreTurn1 if game.losSecondaryFirstScoreTurn1 else 0
                        secondary[editionId][gameTypeId]['totalScoreSecond'] += game.losSecondaryFirstScoreTurn2 if game.losSecondaryFirstScoreTurn2 else 0
                        secondary[editionId][gameTypeId]['totalScoreThird'] += game.losSecondaryFirstScoreTurn3 if game.losSecondaryFirstScoreTurn3 else 0
                        secondary[editionId][gameTypeId]['totalScoreFourth'] += game.losSecondaryFirstScoreTurn4 if game.losSecondaryFirstScoreTurn4 else 0
                    if secondaryGl['sql'] in game.losSecondarySecond:
                        secondary[editionId][gameTypeId]['totalGames'] += 1
                        secondary[editionId][gameTypeId]['totalScore'] += game.losSecondarySecondScore
                        secondary[editionId][gameTypeId]['totalScoreFirst'] += game.losSecondarySecondScoreTurn1 if game.losSecondarySecondScoreTurn1 else 0
                        secondary[editionId][gameTypeId]['totalScoreSecond'] += game.losSecondarySecondScoreTurn2 if game.losSecondarySecondScoreTurn2 else 0
                        secondary[editionId][gameTypeId]['totalScoreThird'] += game.losSecondarySecondScoreTurn3 if game.losSecondarySecondScoreTurn3 else 0
                        secondary[editionId][gameTypeId]['totalScoreFourth'] += game.losSecondarySecondScoreTurn4 if game.losSecondarySecondScoreTurn4 else 0
                    if secondaryGl['sql'] in game.losSecondaryThird:
                        secondary[editionId][gameTypeId]['totalGames'] += 1
                        secondary[editionId][gameTypeId]['totalScore'] += game.losSecondaryThirdScore
                        secondary[editionId][gameTypeId]['totalScoreFirst'] += game.losSecondaryThirdScoreTurn1 if game.losSecondaryThirdScoreTurn1 else 0
                        secondary[editionId][gameTypeId]['totalScoreSecond'] += game.losSecondaryThirdScoreTurn2 if game.losSecondaryThirdScoreTurn2 else 0
                        secondary[editionId][gameTypeId]['totalScoreThird'] += game.losSecondaryThirdScoreTurn3 if game.losSecondaryThirdScoreTurn3 else 0
                        secondary[editionId][gameTypeId]['totalScoreFourth'] += game.losSecondaryThirdScoreTurn4 if game.losSecondaryThirdScoreTurn4 else 0
        secondaryGl['updates'][str(update.id)] = secondary
    try:
        secondaryGl['sql'].avgScore = float("{:.2f}".format(secondaryGl['updates']['1']['1']['totalScore'] / secondaryGl['updates']['1']['1']['totalGames']))
        secondaryGl['sql'].avgScoreFirst = float("{:.2f}".format(secondaryGl['updates']['1']['1']['totalScoreFirst'] / secondaryGl['updates']['1']['1']['totalGames']))
        secondaryGl['sql'].avgScoreSecond = float("{:.2f}".format(secondaryGl['updates']['1']['1']['totalScoreSecond'] / secondaryGl['updates']['1']['1']['totalGames']))
        secondaryGl['sql'].avgScoreThird = float("{:.2f}".format(secondaryGl['updates']['1']['1']['totalScoreThird'] / secondaryGl['updates']['1']['1']['totalGames']))
        secondaryGl['sql'].avgScoreFourth = float("{:.2f}".format(secondaryGl['updates']['1']['1']['totalScoreFourth'] / secondaryGl['updates']['1']['1']['totalGames']))
    except ZeroDivisionError:
        secondaryGl['sql'].avgScore = 0
        secondaryGl['sql'].avgScoreFirst = 0
        secondaryGl['sql'].avgScoreSecond = 0
        secondaryGl['sql'].avgScoreThird = 0
        secondaryGl['sql'].avgScoreFourth = 0
    secondaryGl['sql'].totalGames = secondaryGl['updates']['1']['1']['1']['totalGames']
    db.session.add(secondaryGl['sql'])
    db.session.commit()
    return secondaryGl


def getSecondaries(up, tp, ed):
    secondaries = {}
    for secondary in Secondary.query.all():
        secondaryInd = getSecondary(secondary.id, up, tp, ed)
        secondaries[secondaryInd['sql'].shortName] = secondaryInd
    return [secondary for secondary in secondaries.values()]


def getSecondary(sc, up, tp, ed):
    secondaryGl = {
        'sql': Secondary.query.filter_by(id=sc).first(),
        'rates': {},
    }
    rates = SecondaryRates.query.filter_by(secondary=sc).filter_by(fromUpdate=up).filter_by(fromGameType=tp).filter_by(fromEdition=ed).order_by(desc(SecondaryRates.rate1)).all()
    gameWinSec1 = Game.query.filter(Game.update == up if up > 1 else Game.update).filter(Game.gameType == tp if tp > 1 else Game.gameType).filter(Game.edition == ed if ed > 1 else Game.edition).filter(Game.winSecondaryFirst.contains(secondaryGl['sql'])).all()
    gameWinSec2 = Game.query.filter(Game.update == up if up > 1 else Game.update).filter(Game.gameType == tp if tp > 1 else Game.gameType).filter(Game.edition == ed if ed > 1 else Game.edition).filter(Game.winSecondarySecond.contains(secondaryGl['sql'])).all()
    gameWinSec3 = Game.query.filter(Game.update == up if up > 1 else Game.update).filter(Game.gameType == tp if tp > 1 else Game.gameType).filter(Game.edition == ed if ed > 1 else Game.edition).filter(Game.winSecondaryThird.contains(secondaryGl['sql'])).all()
    gameLosSec1 = Game.query.filter(Game.update == up if up > 1 else Game.update).filter(Game.gameType == tp if tp > 1 else Game.gameType).filter(Game.edition == ed if ed > 1 else Game.edition).filter(Game.winSecondaryFirst.contains(secondaryGl['sql'])).all()
    gameLosSec2 = Game.query.filter(Game.update == up if up > 1 else Game.update).filter(Game.gameType == tp if tp > 1 else Game.gameType).filter(Game.edition == ed if ed > 1 else Game.edition).filter(Game.winSecondarySecond.contains(secondaryGl['sql'])).all()
    gameLosSec3 = Game.query.filter(Game.update == up if up > 1 else Game.update).filter(Game.gameType == tp if tp > 1 else Game.gameType).filter(Game.edition == ed if ed > 1 else Game.edition).filter(Game.winSecondaryThird.contains(secondaryGl['sql'])).all()
    secondary = {
        'popularity': 0,
        'bestFactions': {},
        'games': {},
        'maxGames': 0
    }
    for rate in rates:
        faction = Faction.query.filter_by(id=rate.faction).first()
        secondary['bestFactions'][faction.name] = {
            'winRate': rate.rate1,
            'loseRate': rate.rate2,
            'tieRate': rate.rate3,
            'games': rate.games,
            'id': rate.faction,
            'shortName': faction.shortName
        }
    popularity = len(gameWinSec1)
    popularity += len(gameWinSec2)
    popularity += len(gameWinSec3)
    popularity += len(gameLosSec1)
    popularity += len(gameLosSec2)
    popularity += len(gameLosSec3)
    try:
        secondary['popularity'] = float("{:.2f}".format(popularity * 50 / len(Game.query.filter(Game.update == up if up > 1 else Game.update).filter(Game.gameType == tp if tp > 1 else Game.gameType).filter(Game.edition == ed if ed > 1 else Game.edition).all())))
    except ZeroDivisionError:
        secondary['popularity'] = 0
    secondary['topFaction'] = Faction.query.filter_by(name=list(secondary['bestFactions'].keys())[0]).first() if secondary['bestFactions'] else None
    secondaryGl['rates'] = secondary
    return secondaryGl
