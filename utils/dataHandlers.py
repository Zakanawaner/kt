import time

from datetime import datetime
from database import (
    Game, Player, Mission, Rank, Secondary,
    Faction, Tournament, Operative, Update,
    GameType
)


#####################
# Raw data Handlers #
def handlePlayers(db, response, opt):
    if not Player.query.filter_by(username=response[opt]).first():
        player = Player(
            username=response[opt],
            steamId=response[response[opt]]['steamId'],
            shortName=response[opt].lower().replace(' ', ''),
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
                              shortName=response['mission']['name'].lower().replace(' ', ''),
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
                    name=response[response[opt]]['secondaries'][sec]['name'],
                    shortName=response[response[opt]]['secondaries'][sec]['name'].lower().replace(' ',
                                                                                                  ''), ) if not Secondary.query.filter_by(
                    name=response[response[opt]]['secondaries'][sec]['name']).first() else Secondary.query.filter_by(
                    name=response[response[opt]]['secondaries'][sec]['name']).first()
                db.session.add(response[response[opt]]['secondaries'][sec]['name'])
    db.session.commit()
    return response


def handleTournament(db, response):
    if 'tournament' in response.keys():
        if not Tournament.query.filter_by(name=response['tournament']).first():
            response['tournament'] = Tournament(name=response['tournament'],
                                                shortName=response['tournament'].lower().replace(' ', ''), )
            db.session.add(response['tournament'])
        else:
            response['tournament'] = Tournament.query.filter_by(name=response['tournament']).first()
    else:
        response['tournament'] = None
    db.session.commit()
    return response


def handleGameType(db, response):
    if 'gameType' in response.keys():
        if not GameType.query.filter_by(name=response['gameType']).first():
            response['gameType'] = GameType(name=response['gameType'],
                                            shortName=response['gameType'].lower().replace(' ', ''), )
            db.session.add(response['gameType'])
        else:
            response['gameType'] = GameType.query.filter_by(name=response['gameType']).first()
    else:
        response['gameType'] = None
    db.session.commit()
    return response


def handleOperatives(db, response, pls):
    for pl in pls:
        if 'operatives' in response[response[pl]].keys():
            for op in response[response[pl]]['operatives'].keys():
                weapons = response[response[pl]]['operatives'][op]['desc'].split('Weapons')[1].split('---')[0].split(
                    '\n')
                melee = []
                ranged = []
                for i, weapon in enumerate(weapons):
                    if weapon == '':
                        if i < len(weapons) - 1:
                            if '[' not in weapons[i + 1]:
                                ranged.append(weapons[i + 1])
                    else:
                        if ']M[' in weapon:
                            melee.append(weapon[weapon.find(' ') + 1:])
                        if ']R[' in weapon:
                            ranged.append(weapon[weapon.find(' ') + 1:])
                name = response[response[pl]]['operatives'][op]['desc'].split('\n')[0]
                response[response[pl]]['operatives'][op]['sql'] = Operative.query.filter_by(name=name).filter_by(
                    melee=','.join(melee)).filter_by(ranged=','.join(ranged)).first()
                if not response[response[pl]]['operatives'][op]['sql']:
                    response[response[pl]]['operatives'][op]['sql'] = Operative(
                        name=name,
                        faction=response[response[pl]]['faction'].id,
                        melee=','.join(melee),
                        ranged=','.join(ranged),
                        desc=response[response[pl]]['operatives'][op]['desc'].split("Owned")[0]
                    )
                    db.session.add(response[response[pl]]['operatives'][op]['sql'])
                    db.session.commit()
        else:
            response[response[pl]]['operatives'] = {}
    return response


def handleGameData(response, db):
    if checkData(response):
        if not Game.query.filter_by(timestamp=response['timestamp']).first():
            response = handleFactions(db, response, 'winner')
            response = handleFactions(db, response, 'loser')
            response = handleSecondaries(db, response, 'winner')
            response = handleSecondaries(db, response, 'loser')
            response = handleMission(db, response)
            response = handleTournament(db, response)
            response = handleGameType(db, response)
            response = handleOperatives(db, response, ['winner', 'loser'])

            game = Game(
                date=datetime.now(),
                timestamp=response['timestamp'],
                tournament=response['tournament'].id,
                gameType=response['gameType'].id,
                mission=[response['mission']] if response['mission'] else [],
                initFirst=[response[response['winner']]['faction']] if response[response['winner']]['initiative'][
                    0] else [response[response['loser']]['faction']],
                initSecond=[response[response['winner']]['faction']] if response[response['winner']]['initiative'][
                    1] else [response[response['loser']]['faction']],
                initThird=[response[response['winner']]['faction']] if response[response['winner']]['initiative'][
                    2] else [response[response['loser']]['faction']],
                initFourth=[response[response['winner']]['faction']] if response[response['winner']]['initiative'][
                    3] else [response[response['loser']]['faction']],
                winner=response['winner'],
                winnerId=response[response['winner']]['steamId'],
                winFaction=[response[response['winner']]['faction']] if response[response['winner']]['faction'] else [],
                winOperatives=','.join([str(op['sql'].id) for op in response[response['winner']]['operatives'].values()]),
                winOpKilled=','.join([str(op['roundKilled']) if op['killed'] else '0' for op in response[response['winner']]['operatives'].values()]),
                winScouting=response[response['winner']]['scouting'],
                winTotal=response[response['winner']]['total'],
                winPrimary=response[response['winner']]['primaries']['total'],
                winPrimaryFirst=response[response['winner']]['primaries']['first'],
                winPrimarySecond=response[response['winner']]['primaries']['second'],
                winPrimaryThird=response[response['winner']]['primaries']['third'],
                winPrimaryFourth=response[response['winner']]['primaries']['fourth'],
                winSecondary=response[response['winner']]['secondaries']['total'],
                winSecondaryFirst=[response[response['winner']]['secondaries']['first']['name']],
                winSecondaryFirstScoreTurn1=response[response['winner']]['secondaries']['first']['first'],
                winSecondaryFirstScoreTurn2=response[response['winner']]['secondaries']['first']['second'],
                winSecondaryFirstScoreTurn3=response[response['winner']]['secondaries']['first']['third'],
                winSecondaryFirstScoreTurn4=response[response['winner']]['secondaries']['first']['fourth'],
                winSecondaryFirstScore=response[response['winner']]['secondaries']['first']['score'],
                winSecondarySecond=[response[response['winner']]['secondaries']['second']['name']],
                winSecondarySecondScoreTurn1=response[response['winner']]['secondaries']['second']['first'],
                winSecondarySecondScoreTurn2=response[response['winner']]['secondaries']['second']['second'],
                winSecondarySecondScoreTurn3=response[response['winner']]['secondaries']['second']['third'],
                winSecondarySecondScoreTurn4=response[response['winner']]['secondaries']['second']['fourth'],
                winSecondarySecondScore=response[response['winner']]['secondaries']['second']['score'],
                winSecondaryThird=[response[response['winner']]['secondaries']['third']['name']],
                winSecondaryThirdScoreTurn1=response[response['winner']]['secondaries']['third']['first'],
                winSecondaryThirdScoreTurn2=response[response['winner']]['secondaries']['third']['second'],
                winSecondaryThirdScoreTurn3=response[response['winner']]['secondaries']['third']['third'],
                winSecondaryThirdScoreTurn4=response[response['winner']]['secondaries']['third']['fourth'],
                winSecondaryThirdScore=response[response['winner']]['secondaries']['third']['score'],
                loser=response['loser'],
                loserId=response[response['loser']]['steamId'],
                losFaction=[response[response['loser']]['faction']] if response[response['loser']]['faction'] else [],
                losOperatives=','.join([str(op['sql'].id) for op in response[response['loser']]['operatives'].values()]),
                losOpKilled=','.join([str(op['roundKilled']) if op['killed'] else '0' for op in response[response['loser']]['operatives'].values()]),
                losScouting=response[response['loser']]['scouting'],
                losTotal=response[response['loser']]['total'],
                losPrimary=response[response['loser']]['primaries']['total'],
                losPrimaryFirst=response[response['loser']]['primaries']['first'],
                losPrimarySecond=response[response['loser']]['primaries']['second'],
                losPrimaryThird=response[response['loser']]['primaries']['third'],
                losPrimaryFourth=response[response['loser']]['primaries']['fourth'],
                losSecondary=response[response['loser']]['secondaries']['total'],
                losSecondaryFirst=[response[response['loser']]['secondaries']['first']['name']],
                losSecondaryFirstScoreTurn1=response[response['loser']]['secondaries']['first']['first'],
                losSecondaryFirstScoreTurn2=response[response['loser']]['secondaries']['first']['second'],
                losSecondaryFirstScoreTurn3=response[response['loser']]['secondaries']['first']['third'],
                losSecondaryFirstScoreTurn4=response[response['loser']]['secondaries']['first']['fourth'],
                losSecondaryFirstScore=response[response['loser']]['secondaries']['first']['score'],
                losSecondarySecond=[response[response['loser']]['secondaries']['second']['name']],
                losSecondarySecondScoreTurn1=response[response['loser']]['secondaries']['second']['first'],
                losSecondarySecondScoreTurn2=response[response['loser']]['secondaries']['second']['second'],
                losSecondarySecondScoreTurn3=response[response['loser']]['secondaries']['second']['third'],
                losSecondarySecondScoreTurn4=response[response['loser']]['secondaries']['second']['fourth'],
                losSecondarySecondScore=response[response['loser']]['secondaries']['second']['score'],
                losSecondaryThird=[response[response['loser']]['secondaries']['third']['name']],
                losSecondaryThirdScoreTurn1=response[response['loser']]['secondaries']['third']['first'],
                losSecondaryThirdScoreTurn2=response[response['loser']]['secondaries']['third']['second'],
                losSecondaryThirdScoreTurn3=response[response['loser']]['secondaries']['third']['third'],
                losSecondaryThirdScoreTurn4=response[response['loser']]['secondaries']['third']['fourth'],
                losSecondaryThirdScore=response[response['loser']]['secondaries']['third']['score'],
                rollOffWinner=[
                    response[response['rollOffWinner']]['faction']] if 'rollOffWinner' in response.keys() else [],
                rollOffSelection=response[
                    'rollOffWinnerSelection'] if 'rollOffWinnerSelection' in response.keys() else '',
                tie=response['tie']
            )

            if response['tie']:
                response[response['winner']]['faction'].gamesTied.append(game)
                if response[response['winner']]['faction'] != response[response['loser']]['faction']:
                    response[response['loser']]['faction'].gamesTied.append(game)
            else:
                response[response['winner']]['faction'].gamesWon.append(game)
                response[response['loser']]['faction'].gamesLost.append(game)

            db.session.add(response[response['winner']]['faction'])
            db.session.add(response[response['loser']]['faction'])
            response['tournament'].games.append(game)
            response['gameType'].games.append(game)
            db.session.add(response['tournament'])
            db.session.add(response['gameType'])
            db.session.add(game)
            db.session.commit()
            return game
        return "Already saved"
    return "Bad game data"


def checkData(response):
    template = {
        'mission': {
            "code": 0,
            "name": ""
        },
        'timestamp': "",
        'tournament': "",
        'gameType': "",
        'rollOffWinner': "",
        'rollOffWinnerSelection': "",
        response['winner']: {
            'steamId': 0,
            'initiative': [],
            'scouting': "",
            'faction': "",
            'primaries': {
                'first': 0,
                'second': 0,
                'third': 0,
                'fourth': 0,
                'total': 0,
            },
            'secondaries': {
                'first': {
                    'name': "",
                    'score': 0,
                    'first': 0,
                    'second': 0,
                    'third': 0,
                    'fourth': 0,
                },
                'second': {
                    'name': "",
                    'score': 0,
                    'first': 0,
                    'second': 0,
                    'third': 0,
                    'fourth': 0,
                },
                'third': {
                    'name': "",
                    'score': 0,
                    'first': 0,
                    'second': 0,
                    'third': 0,
                    'fourth': 0,
                },
                'total': 0,
            }
        },
        response['loser']: {
            'steamId': 0,
            'initiative': [],
            'scouting': "",
            'faction': "",
            'primaries': {
                'first': 0,
                'second': 0,
                'third': 0,
                'fourth': 0,
                'total': 0,
            },
            'secondaries': {
                'first': {
                    'name': "",
                    'score': 0,
                    'first': 0,
                    'second': 0,
                    'third': 0,
                    'fourth': 0,
                },
                'second': {
                    'name': "",
                    'score': 0,
                    'first': 0,
                    'second': 0,
                    'third': 0,
                    'fourth': 0,
                },
                'third': {
                    'name': "",
                    'score': 0,
                    'first': 0,
                    'second': 0,
                    'third': 0,
                    'fourth': 0,
                },
                'total': 0,
            }
        }
    }
    if set(template.keys()) <= set(response.keys()):
        if set(template['mission'].keys()) <= set(response['mission'].keys()) and set(
                template[response['winner']].keys()) <= set(response[response['winner']].keys()) and set(
            template[response['loser']].keys()) <= set(response[response['loser']].keys()):
            if set(template[response['winner']]['primaries'].keys()) <= set(
                    response[response['winner']]['primaries'].keys()) and set(
                template[response['loser']]['primaries'].keys()) <= set(
                response[response['loser']]['primaries'].keys()) and set(
                template[response['winner']]['secondaries'].keys()) <= set(
                response[response['winner']]['secondaries'].keys()) and set(
                template[response['loser']]['secondaries'].keys()) <= set(
                response[response['loser']]['secondaries'].keys()):
                if set(template[response['winner']]['secondaries']['first'].keys()) <= set(
                        response[response['winner']]['secondaries']['first'].keys()) and set(
                    template[response['loser']]['secondaries']['first'].keys()) <= set(
                    response[response['loser']]['secondaries']['first'].keys()) and set(
                    template[response['winner']]['secondaries']['second'].keys()) <= set(
                    response[response['winner']]['secondaries']['second'].keys()) and set(
                    template[response['loser']]['secondaries']['second'].keys()) <= set(
                    response[response['loser']]['secondaries']['second'].keys()) and set(
                    template[response['winner']]['secondaries']['third'].keys()) <= set(
                    response[response['winner']]['secondaries']['third'].keys()) and set(
                    template[response['loser']]['secondaries']['third'].keys()) <= set(
                    response[response['loser']]['secondaries']['third'].keys()):
                    if (response[response['winner']]['secondaries']['first']['name'] != response[response['winner']]['secondaries']['second']['name']) \
                            and (response[response['winner']]['secondaries']['first']['name'] != response[response['winner']]['secondaries']['third']['name'])\
                                and (response[response['winner']]['secondaries']['second']['name'] != response[response['winner']]['secondaries']['third']['name']):
                        if (response[response['loser']]['secondaries']['first']['name'] !=
                            response[response['loser']]['secondaries']['second']['name']) \
                                and (response[response['loser']]['secondaries']['first']['name'] !=
                                     response[response['loser']]['secondaries']['third']['name']) \
                                and (response[response['loser']]['secondaries']['second']['name'] !=
                                     response[response['loser']]['secondaries']['third']['name']):
                            return True
    return False


############
# Database #
def createTables(db):
    db.create_all()

    db.session.add(Rank(name="Guardsman", shortName="guardsman", score=0))
    db.session.add(Rank(name="Sergeant", shortName="sergeant", score=50))
    db.session.add(Rank(name="Lieutenant", shortName="lieutenant", score=100))
    db.session.add(Rank(name="Captain", shortName="captain", score=200))
    db.session.add(Rank(name="Major", shortName="major", score=400))
    db.session.add(Rank(name="Colonel", shortName="colonel", score=800))
    db.session.add(Rank(name="Major General", shortName="majorgeneral", score=1600))
    db.session.add(Rank(name="Lieutenant General", shortName="lieutenantgeneral", score=3200))
    db.session.add(Rank(name="Marshall", shortName="marshall", score=6400))
    db.session.add(Rank(name="General", shortName="general", score=12800))
    db.session.add(Rank(name="Lord General", shortName="lordgeneral", score=25600))
    db.session.add(Rank(name="Lord General Militant", shortName="lordgeneralmilitant", score=51200))
    db.session.add(Rank(name="Warmaster", shortName="warmaster", score=102400))
    db.session.add(Rank(name="Lord Commander", shortName="lordcommander", score=204800))

    db.session.add(Update(name="All Time",
                          date=datetime.fromtimestamp(0),
                          dateEnd=datetime.fromtimestamp(9999999999),
                          description="All time data",
                          id=1))
    db.session.add(GameType(name="All plays",
                            shortName="allplays",
                            id=1))
    db.session.commit()
    db.session.add(Update(name="First APP launch",
                          date=datetime.fromtimestamp(int(time.time())),
                          dateEnd=datetime.fromtimestamp(int(time.time()) + 31556926),
                          description="First update dated on the web launch day"))
    db.session.commit()
