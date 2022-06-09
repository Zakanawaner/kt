from database import Secondary, Update, Game, Faction, SecondaryRates, GameType
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
        for gameType in GameType.query.all():
            gameTypeId = str(gameType.id)
            secondary[gameTypeId] = {
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
                    Game.date <= update.dateEnd).filter(
                    Game.winSecondaryFirst.contains(secondaryGl['sql'])).all():
                if game.gameType == gameType.id or gameType.id == 1:
                    secondary[gameTypeId]['totalGames'] += 1
                    secondary[gameTypeId]['totalScore'] += game.winSecondaryFirstScore
                    secondary[gameTypeId]['totalScoreFirst'] += game.winSecondaryFirstScoreTurn1 if game.winSecondaryFirstScoreTurn1 else 0
                    secondary[gameTypeId]['totalScoreSecond'] += game.winSecondaryFirstScoreTurn2 if game.winSecondaryFirstScoreTurn2 else 0
                    secondary[gameTypeId]['totalScoreThird'] += game.winSecondaryFirstScoreTurn3 if game.winSecondaryFirstScoreTurn3 else 0
                    secondary[gameTypeId]['totalScoreFourth'] += game.winSecondaryFirstScoreTurn4 if game.winSecondaryFirstScoreTurn4 else 0
            for game in Game.query.filter(
                    Game.date >= update.date).filter(
                    Game.date <= update.dateEnd).filter(
                    Game.winSecondarySecond.contains(secondaryGl['sql'])).all():
                if game.gameType == gameType.id or gameType.id == 1:
                    secondary[gameTypeId]['totalGames'] += 1
                    secondary[gameTypeId]['totalScore'] += game.winSecondarySecondScore
                    secondary[gameTypeId]['totalScoreFirst'] += game.winSecondarySecondScoreTurn1 if game.winSecondarySecondScoreTurn1 else 0
                    secondary[gameTypeId]['totalScoreSecond'] += game.winSecondarySecondScoreTurn2 if game.winSecondarySecondScoreTurn2 else 0
                    secondary[gameTypeId]['totalScoreThird'] += game.winSecondarySecondScoreTurn3 if game.winSecondarySecondScoreTurn3 else 0
                    secondary[gameTypeId]['totalScoreFourth'] += game.winSecondarySecondScoreTurn4 if game.winSecondarySecondScoreTurn4 else 0
            for game in Game.query.filter(
                    Game.date >= update.date).filter(
                    Game.date <= update.dateEnd).filter(
                    Game.winSecondaryThird.contains(secondaryGl['sql'])).all():
                if game.gameType == gameType.id or gameType.id == 1:
                    secondary[gameTypeId]['totalGames'] += 1
                    secondary[gameTypeId]['totalScore'] += game.winSecondaryThirdScore
                    secondary[gameTypeId]['totalScoreFirst'] += game.winSecondaryThirdScoreTurn1 if game.winSecondaryThirdScoreTurn1 else 0
                    secondary[gameTypeId]['totalScoreSecond'] += game.winSecondaryThirdScoreTurn2 if game.winSecondaryThirdScoreTurn2 else 0
                    secondary[gameTypeId]['totalScoreThird'] += game.winSecondaryThirdScoreTurn3 if game.winSecondaryThirdScoreTurn3 else 0
                    secondary[gameTypeId]['totalScoreFourth'] += game.winSecondaryThirdScoreTurn4 if game.winSecondaryThirdScoreTurn4 else 0
            for game in Game.query.filter(
                    Game.date >= update.date).filter(
                    Game.date <= update.dateEnd).filter(
                    Game.losSecondaryFirst.contains(secondaryGl['sql'])).all():
                if game.gameType == gameType.id or gameType.id == 1:
                    secondary[gameTypeId]['totalGames'] += 1
                    secondary[gameTypeId]['totalScore'] += game.losSecondaryFirstScore
                    secondary[gameTypeId]['totalScoreFirst'] += game.losSecondaryFirstScoreTurn1 if game.losSecondaryFirstScoreTurn1 else 0
                    secondary[gameTypeId]['totalScoreSecond'] += game.losSecondaryFirstScoreTurn2 if game.losSecondaryFirstScoreTurn2 else 0
                    secondary[gameTypeId]['totalScoreThird'] += game.losSecondaryFirstScoreTurn3 if game.losSecondaryFirstScoreTurn3 else 0
                    secondary[gameTypeId]['totalScoreFourth'] += game.losSecondaryFirstScoreTurn4 if game.losSecondaryFirstScoreTurn4 else 0
            for game in Game.query.filter(
                    Game.date >= update.date).filter(
                    Game.date <= update.dateEnd).filter(
                    Game.losSecondarySecond.contains(secondaryGl['sql'])).all():
                if game.gameType == gameType.id or gameType.id == 1:
                    secondary[gameTypeId]['totalGames'] += 1
                    secondary[gameTypeId]['totalScore'] += game.losSecondarySecondScore
                    secondary[gameTypeId]['totalScoreFirst'] += game.losSecondarySecondScoreTurn1 if game.losSecondarySecondScoreTurn1 else 0
                    secondary[gameTypeId]['totalScoreSecond'] += game.losSecondarySecondScoreTurn2 if game.losSecondarySecondScoreTurn2 else 0
                    secondary[gameTypeId]['totalScoreThird'] += game.losSecondarySecondScoreTurn3 if game.losSecondarySecondScoreTurn3 else 0
                    secondary[gameTypeId]['totalScoreFourth'] += game.losSecondarySecondScoreTurn4 if game.losSecondarySecondScoreTurn4 else 0
            for game in Game.query.filter(
                    Game.date >= update.date).filter(
                    Game.date <= update.dateEnd).filter(
                    Game.losSecondaryThird.contains(secondaryGl['sql'])).all():
                if game.gameType == gameType.id or gameType.id == 1:
                    secondary[gameTypeId]['totalGames'] += 1
                    secondary[gameTypeId]['totalScore'] += game.losSecondaryThirdScore
                    secondary[gameTypeId]['totalScoreFirst'] += game.losSecondaryThirdScoreTurn1 if game.losSecondaryThirdScoreTurn1 else 0
                    secondary[gameTypeId]['totalScoreSecond'] += game.losSecondaryThirdScoreTurn2 if game.losSecondaryThirdScoreTurn2 else 0
                    secondary[gameTypeId]['totalScoreThird'] += game.losSecondaryThirdScoreTurn3 if game.losSecondaryThirdScoreTurn3 else 0
                    secondary[gameTypeId]['totalScoreFourth'] += game.losSecondaryThirdScoreTurn4 if game.losSecondaryThirdScoreTurn4 else 0
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

    secondaryGl['sql'].totalGames = secondaryGl['updates']['1']['1']['totalGames']
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
    rates = SecondaryRates.query.filter_by(secondary=sc).order_by(desc(SecondaryRates.rate1)).all()
    gameWinSec1 = Game.query.filter(Game.winSecondaryFirst.contains(secondaryGl['sql'])).all()
    gameWinSec2 = Game.query.filter(Game.winSecondarySecond.contains(secondaryGl['sql'])).all()
    gameWinSec3 = Game.query.filter(Game.winSecondaryThird.contains(secondaryGl['sql'])).all()
    gameLosSec1 = Game.query.filter(Game.winSecondaryFirst.contains(secondaryGl['sql'])).all()
    gameLosSec2 = Game.query.filter(Game.winSecondarySecond.contains(secondaryGl['sql'])).all()
    gameLosSec3 = Game.query.filter(Game.winSecondaryThird.contains(secondaryGl['sql'])).all()
    for update in Update.query.all():
        secondary = {}
        for gameType in GameType.query.all():
            gameTypeId = str(gameType.id)
            secondary[gameTypeId] = {
                'popularity': 0,
                'bestFactions': {},
                'games': {},
                'maxGames': 0
            }
            for rate in rates:
                if rate.fromUpdate == update.id and rate.fromGameType == gameType.id:
                    faction = Faction.query.filter_by(id=rate.faction).first()
                    secondary[gameTypeId]['bestFactions'][faction.name] = {
                        'winRate': rate.rate1,
                        'loseRate': rate.rate2,
                        'tieRate': rate.rate3,
                        'games': rate.games,
                        'id': rate.faction,
                        'shortName': faction.shortName
                    }
            if gameType.id == 1:
                popularity = len([i for i in gameWinSec1 if update.date < i.date <= update.dateEnd])
                popularity += len([i for i in gameWinSec2 if update.date < i.date <= update.dateEnd])
                popularity += len([i for i in gameWinSec3 if update.date < i.date <= update.dateEnd])
                popularity += len([i for i in gameLosSec1 if update.date < i.date <= update.dateEnd])
                popularity += len([i for i in gameLosSec2 if update.date < i.date <= update.dateEnd])
                popularity += len([i for i in gameLosSec3 if update.date < i.date <= update.dateEnd])
                try:
                    secondary[gameTypeId]['popularity'] = float("{:.2f}".format(popularity * 50 / len(Game.query.filter(Game.date >= update.date).filter(Game.date <= update.dateEnd).all())))
                except ZeroDivisionError:
                    secondary[gameTypeId]['popularity'] = 0
            else:
                popularity = len([i for i in gameWinSec1 if update.date < i.date <= update.dateEnd and i.gameType == gameType.id])
                popularity += len([i for i in gameWinSec2 if update.date < i.date <= update.dateEnd and i.gameType == gameType.id])
                popularity += len([i for i in gameWinSec3 if update.date < i.date <= update.dateEnd and i.gameType == gameType.id])
                popularity += len([i for i in gameLosSec1 if update.date < i.date <= update.dateEnd and i.gameType == gameType.id])
                popularity += len([i for i in gameLosSec2 if update.date < i.date <= update.dateEnd and i.gameType == gameType.id])
                popularity += len([i for i in gameLosSec3 if update.date < i.date <= update.dateEnd and i.gameType == gameType.id])
                try:
                    secondary[gameTypeId]['popularity'] = float("{:.2f}".format(popularity * 50 / len(Game.query.filter_by(gameType=gameType.id).filter(Game.date >= update.date).filter(Game.date <= update.dateEnd).all())))
                except ZeroDivisionError:
                    secondary[gameTypeId]['popularity'] = 0
            secondary[gameTypeId]['topFaction'] = Faction.query.filter_by(name=list(secondary[gameTypeId]['bestFactions'].keys())[0]).first() if secondary[gameTypeId]['bestFactions'] else None
            secondaryGl['updates'][str(update.id)] = secondary
    return secondaryGl
