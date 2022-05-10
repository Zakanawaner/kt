from database import Secondary, Update, Game, Faction, SecondaryRates
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
                Game.date <=  update.dateEnd).filter(
                Game.winSecondaryFirst.contains(secondaryGl['sql'])).all():
            secondary['totalGames'] += 1
            secondary['totalScore'] += game.winSecondaryFirstScore
            secondary['totalScoreFirst'] += game.winSecondaryFirstScoreTurn1 if game.winSecondaryFirstScoreTurn1 else 0
            secondary['totalScoreSecond'] += game.winSecondaryFirstScoreTurn2 if game.winSecondaryFirstScoreTurn2 else 0
            secondary['totalScoreThird'] += game.winSecondaryFirstScoreTurn3 if game.winSecondaryFirstScoreTurn3 else 0
            secondary['totalScoreFourth'] += game.winSecondaryFirstScoreTurn4 if game.winSecondaryFirstScoreTurn4 else 0
        for game in Game.query.filter(
                Game.date >= update.date).filter(
                Game.date <=  update.dateEnd).filter(
                Game.winSecondarySecond.contains(secondaryGl['sql'])).all():
            secondary['totalGames'] += 1
            secondary['totalScore'] += game.winSecondarySecondScore
            secondary['totalScoreFirst'] += game.winSecondarySecondScoreTurn1 if game.winSecondarySecondScoreTurn1 else 0
            secondary['totalScoreSecond'] += game.winSecondarySecondScoreTurn2 if game.winSecondarySecondScoreTurn2 else 0
            secondary['totalScoreThird'] += game.winSecondarySecondScoreTurn3 if game.winSecondarySecondScoreTurn3 else 0
            secondary['totalScoreFourth'] += game.winSecondarySecondScoreTurn4 if game.winSecondarySecondScoreTurn4 else 0
        for game in Game.query.filter(
                Game.date >= update.date).filter(
                Game.date <=  update.dateEnd).filter(
                Game.winSecondaryThird.contains(secondaryGl['sql'])).all():
            secondary['totalGames'] += 1
            secondary['totalScore'] += game.winSecondaryThirdScore
            secondary['totalScoreFirst'] += game.winSecondaryThirdScoreTurn1 if game.winSecondaryThirdScoreTurn1 else 0
            secondary['totalScoreSecond'] += game.winSecondaryThirdScoreTurn2 if game.winSecondaryThirdScoreTurn2 else 0
            secondary['totalScoreThird'] += game.winSecondaryThirdScoreTurn3 if game.winSecondaryThirdScoreTurn3 else 0
            secondary['totalScoreFourth'] += game.winSecondaryThirdScoreTurn4 if game.winSecondaryThirdScoreTurn4 else 0
        for game in Game.query.filter(
                Game.date >= update.date).filter(
                Game.date <=  update.dateEnd).filter(
                Game.losSecondaryFirst.contains(secondaryGl['sql'])).all():
            secondary['totalGames'] += 1
            secondary['totalScore'] += game.losSecondaryFirstScore
            secondary['totalScoreFirst'] += game.losSecondaryFirstScoreTurn1 if game.losSecondaryFirstScoreTurn1 else 0
            secondary['totalScoreSecond'] += game.losSecondaryFirstScoreTurn2 if game.losSecondaryFirstScoreTurn2 else 0
            secondary['totalScoreThird'] += game.losSecondaryFirstScoreTurn3 if game.losSecondaryFirstScoreTurn3 else 0
            secondary['totalScoreFourth'] += game.losSecondaryFirstScoreTurn4 if game.losSecondaryFirstScoreTurn4 else 0
        for game in Game.query.filter(
                Game.date >= update.date).filter(
                Game.date <=  update.dateEnd).filter(
                Game.losSecondarySecond.contains(secondaryGl['sql'])).all():
            secondary['totalGames'] += 1
            secondary['totalScore'] += game.losSecondarySecondScore
            secondary['totalScoreFirst'] += game.losSecondarySecondScoreTurn1 if game.losSecondarySecondScoreTurn1 else 0
            secondary['totalScoreSecond'] += game.losSecondarySecondScoreTurn2 if game.losSecondarySecondScoreTurn2 else 0
            secondary['totalScoreThird'] += game.losSecondarySecondScoreTurn3 if game.losSecondarySecondScoreTurn3 else 0
            secondary['totalScoreFourth'] += game.losSecondarySecondScoreTurn4 if game.losSecondarySecondScoreTurn4 else 0
        for game in Game.query.filter(
                Game.date >= update.date).filter(
                Game.date <= update.dateEnd).filter(
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
                'games': rate.games,
                'id': rate.faction,
                'shortName': Faction.query.filter_by(id=rate.faction).first().shortName
            }
        popularity = len(Game.query.filter(
                Game.date >= update.date).filter(
                Game.date <= update.dateEnd).filter(
                Game.winSecondaryFirst.contains(secondaryGl['sql'])).all())
        popularity += len(Game.query.filter(
                Game.date >= update.date).filter(
                Game.date <= update.dateEnd).filter(
                Game.winSecondarySecond.contains(secondaryGl['sql'])).all())
        popularity += len(Game.query.filter(
                Game.date >= update.date).filter(
                Game.date <= update.dateEnd).filter(
                Game.winSecondaryThird.contains(secondaryGl['sql'])).all())
        popularity += len(Game.query.filter(
                Game.date >= update.date).filter(
                Game.date <= update.dateEnd).filter(
                Game.losSecondaryFirst.contains(secondaryGl['sql'])).all())
        popularity += len(Game.query.filter(
                Game.date >= update.date).filter(
                Game.date <= update.dateEnd).filter(
                Game.losSecondarySecond.contains(secondaryGl['sql'])).all())
        popularity += len(Game.query.filter(
                Game.date >= update.date).filter(
                Game.date <= update.dateEnd).filter(
                Game.losSecondaryThird.contains(secondaryGl['sql'])).all())
        secondary['popularity'] = float("{:.2f}".format(popularity * 100 / len(Game.query.filter(
                Game.date >= update.date).filter(
                Game.date <= update.dateEnd).all())))
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
            'games': rate.games,
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
    secondary['popularity'] = float("{:.2f}".format(popularity * 100 / (2 * len(Game.query.all()))))
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