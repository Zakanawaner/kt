from database import Game, Mission, Faction, MissionRates, Update, GameType
from sqlalchemy import extract, desc
from datetime import datetime
from collections import OrderedDict


############
# Missions #
def updateMissions(db):
    for mission in Mission.query.all():
        updateMission(db, mission.id)


def updateMission(db, fact):
    missionGl = {
        'sql': Mission.query.filter_by(id=fact).first(),
        'updates': {}
    }
    for update in Update.query.all():
        mission = {}
        for gameType in GameType.query.all():
            gameTypeId = str(gameType.id)
            mission[gameTypeId] = {
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
            for game in Game.query.filter(Game.date >= update.date).filter(Game.date <= update.dateEnd).filter(Game.mission.contains(missionGl['sql'])).all():
                if gameType.id == 1 or game.gameType == gameType.id:
                    mission[gameTypeId]['totalGames'] += 2
                    mission[gameTypeId]['totalScore'] += game.winPrimary + game.losPrimary
                    mission[gameTypeId]['totalScoreFirst'] += game.winPrimaryFirst + game.losPrimaryFirst
                    mission[gameTypeId]['totalScoreSecond'] += game.winPrimarySecond + game.losPrimarySecond
                    mission[gameTypeId]['totalScoreThird'] += game.winPrimaryThird + game.losPrimaryThird
                    mission[gameTypeId]['totalScoreFourth'] += game.winPrimaryFourth + game.losPrimaryFourth
        missionGl['updates'][str(update.id)] = mission
    try:
        missionGl['sql'].avgScore = float("{:.2f}".format(missionGl['updates']['1']['1']['totalScore'] / missionGl['updates']['1']['1']['totalGames']))
        missionGl['sql'].avgScoreFirst = float("{:.2f}".format(missionGl['updates']['1']['1']['totalScoreFirst'] / missionGl['updates']['1']['1']['totalGames']))
        missionGl['sql'].avgScoreSecond = float("{:.2f}".format(missionGl['updates']['1']['1']['totalScoreSecond'] / missionGl['updates']['1']['1']['totalGames']))
        missionGl['sql'].avgScoreThird = float("{:.2f}".format(missionGl['updates']['1']['1']['totalScoreThird'] / missionGl['updates']['1']['1']['totalGames']))
        missionGl['sql'].avgScoreFourth = float("{:.2f}".format(missionGl['updates']['1']['1']['totalScoreFourth'] / missionGl['updates']['1']['1']['totalGames']))
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
    rates1 = MissionRates.query.filter_by(mission=ms).order_by(desc(MissionRates.rate1)).all()
    rates2 = MissionRates.query.filter_by(mission=ms).order_by(desc(MissionRates.rate1)).all()
    for update in Update.query.all():
        mission = {}
        for gameType in GameType.query.all():
            gameTypeId = str(gameType.id)
            mission[gameTypeId] = {
                'popularity': 0,
                'bestFactions': {},
                'worstFactions': {},
                'games': {},
                'maxGames': 0
            }
            for rate in rates1:
                if rate.fromUpdate == update.id and rate.fromGameType == gameType.id:
                    faction = Faction.query.filter_by(id=rate.faction).first()
                    mission[gameTypeId]['bestFactions'][faction.name] = {
                        'winRate': rate.rate1,
                        'loseRate': rate.rate2,
                        'tieRate': rate.rate3,
                        'games': rate.games,
                        'id': rate.faction,
                        'shortName': faction.shortName
                    }
            for rate in rates2:
                if rate.fromUpdate == update.id and rate.fromGameType == gameType.id:
                    faction = Faction.query.filter_by(id=rate.faction).first()
                    mission[gameTypeId]['worstFactions'][faction.name] = {
                        'winRate': rate.rate1,
                        'loseRate': rate.rate2,
                        'tieRate': rate.rate3,
                        'games': rate.games,
                        'id': rate.faction,
                        'shortName': faction.shortName
                    }
            try:
                if gameType.id == 1:
                    mission[gameTypeId]['popularity'] = float("{:.2f}".format(len(Game.query.filter(Game.date >= update.date).filter(Game.date <= update.dateEnd).filter(Game.mission.contains(missionGl['sql'])).all()) * 100 / len(Game.query.filter(Game.date >= update.date).filter(Game.date <= update.dateEnd).all())))
                else:
                    mission[gameTypeId]['popularity'] = float("{:.2f}".format(len(Game.query.filter_by(gameType=gameType.id).filter(Game.date >= update.date).filter(Game.date <= update.dateEnd).filter(Game.mission.contains(missionGl['sql'])).all()) * 100 / len(Game.query.filter_by(gameType=gameType.id).filter(Game.date >= update.date).filter(Game.date <= update.dateEnd).all())))
            except ZeroDivisionError:
                mission[gameTypeId]['popularity'] = 0
            mission[gameTypeId]['topFaction'] = Faction.query.filter_by(name=list(mission[gameTypeId]['bestFactions'].keys())[0]).first() if mission[gameTypeId]['bestFactions'] else None
            mission[gameTypeId]['worstFaction'] = Faction.query.filter_by(name=list(mission[gameTypeId]['worstFactions'].keys())[0]).first() if mission[gameTypeId]['worstFactions'] else None
        missionGl['updates'][str(update.id)] = mission
    return missionGl
