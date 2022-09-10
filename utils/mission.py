from database import Game, Mission, Faction, MissionRates, Update, GameType, Edition
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
        for edition in Edition.query.all():
            editionId = str(edition.id)
            mission[editionId] = {}
            for gameType in GameType.query.all():
                gameTypeId = str(gameType.id)
                mission[editionId][gameTypeId] = {
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
                for game in Game.query.filter(Game.mission.contains(missionGl['sql'])).filter(Game.update == update.id if update.id > 1 else Game.update).filter(Game.gameType == gameType.id if gameType.id > 1 else Game.gameType).filter(Game.edition == edition.id if edition.id > 1 else Game.edition).all():
                    mission[editionId][gameTypeId]['totalGames'] += 2
                    mission[editionId][gameTypeId]['totalScore'] += game.winPrimary + game.losPrimary
                    mission[editionId][gameTypeId]['totalScoreFirst'] += game.winPrimaryFirst + game.losPrimaryFirst
                    mission[editionId][gameTypeId]['totalScoreSecond'] += game.winPrimarySecond + game.losPrimarySecond
                    mission[editionId][gameTypeId]['totalScoreThird'] += game.winPrimaryThird + game.losPrimaryThird
                    mission[editionId][gameTypeId]['totalScoreFourth'] += game.winPrimaryFourth + game.losPrimaryFourth
            missionGl['updates'][str(update.id)] = mission
    try:
        missionGl['sql'].avgScore = float("{:.2f}".format(missionGl['updates']['1']['1']['1']['totalScore'] / missionGl['updates']['1']['1']['1']['totalGames']))
        missionGl['sql'].avgScoreFirst = float("{:.2f}".format(missionGl['updates']['1']['1']['1']['totalScoreFirst'] / missionGl['updates']['1']['1']['1']['totalGames']))
        missionGl['sql'].avgScoreSecond = float("{:.2f}".format(missionGl['updates']['1']['1']['1']['totalScoreSecond'] / missionGl['updates']['1']['1']['1']['totalGames']))
        missionGl['sql'].avgScoreThird = float("{:.2f}".format(missionGl['updates']['1']['1']['1']['totalScoreThird'] / missionGl['updates']['1']['1']['1']['totalGames']))
        missionGl['sql'].avgScoreFourth = float("{:.2f}".format(missionGl['updates']['1']['1']['1']['totalScoreFourth'] / missionGl['updates']['1']['1']['1']['totalGames']))
    except ZeroDivisionError:
        missionGl['sql'].avgScore = 0
        missionGl['sql'].avgScoreFirst = 0
        missionGl['sql'].avgScoreSecond = 0
        missionGl['sql'].avgScoreThird = 0
        missionGl['sql'].avgScoreFourth = 0
    db.session.add(missionGl['sql'])
    db.session.commit()
    return missionGl


def getMissions(up, tp, ed):
    missions = {}
    for mission in Mission.query.all():
        missionInd = getMission(mission.id, up, tp, ed)
        missions[missionInd['sql'].shortName] = missionInd
    return [mission for mission in missions.values()]


def getMission(ms, up, tp, ed):
    missionGl = {
        'sql': Mission.query.filter_by(id=ms).first(),
        'rates': {},
    }
    rates1 = MissionRates.query.filter_by(mission=ms).filter_by(fromUpdate=up).filter_by(fromEdition=ed).filter_by(fromGameType=tp).order_by(desc(MissionRates.rate1)).all()
    rates2 = MissionRates.query.filter_by(mission=ms).filter_by(fromUpdate=up).filter_by(fromEdition=ed).filter_by(fromGameType=tp).order_by(desc(MissionRates.rate2)).all()
    mission = {
        'popularity': 0,
        'bestFactions': {},
        'worstFactions': {},
        'games': {},
        'maxGames': 0
    }
    for rate in rates1:
        faction = Faction.query.filter_by(id=rate.faction).first()
        mission['bestFactions'][faction.name] = {
            'winRate': rate.rate1,
            'loseRate': rate.rate2,
            'tieRate': rate.rate3,
            'games': rate.games,
            'id': rate.faction,
            'shortName': faction.shortName
        }
    for rate in rates2:
        faction = Faction.query.filter_by(id=rate.faction).first()
        mission['worstFactions'][faction.name] = {
            'winRate': rate.rate1,
            'loseRate': rate.rate2,
            'tieRate': rate.rate3,
            'games': rate.games,
            'id': rate.faction,
            'shortName': faction.shortName
        }
    try:
        gamesPlayed = Game.query.filter(Game.mission.contains(missionGl['sql'])).filter(Game.update == up if up > 1 else Game.update).filter(Game.gameType == tp if tp > 1 else Game.gameType).filter(Game.edition == ed if ed > 1 else Game.edition).all()
        gamesTotal = Game.query.filter(Game.update == up if up > 1 else Game.update).filter(Game.gameType == tp if tp > 1 else Game.gameType).filter(Game.edition == ed if ed > 1 else Game.edition).all()
        mission['popularity'] = float("{:.2f}".format(len(gamesPlayed) * 100 / len(gamesTotal)))
    except ZeroDivisionError:
        mission['popularity'] = 0
    mission['topFaction'] = Faction.query.filter_by(name=list(mission['bestFactions'].keys())[0]).first() if mission['bestFactions'] else None
    mission['worstFaction'] = Faction.query.filter_by(name=list(mission['worstFactions'].keys())[0]).first() if mission['worstFactions'] else None
    missionGl['rates'] = mission
    return missionGl
