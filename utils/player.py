from sqlalchemy import desc
from database import (
    Game, Player, Mission, Rank, Secondary, Faction,
    PlayerMissionRates,
    PlayerWinRates, PlayerWinRatesPlayer, PlayerSecondaryRates,
    PlayerWinRatesAgainst, Update, GameType
)


###########
# Players #
def updatePlayers(db):
    for player in Player.query.all():
        updatePlayer(db, player.id)


def updatePlayer(db, pl):
    playerGl = {
        'sql': Player.query.filter_by(id=pl).first(),
        'updates': {},
    }
    playerGl['sql'].gamesWon = []
    playerGl['sql'].gamesLost = []
    playerGl['sql'].gamesTied = []
    playerGl['sql'].wins = 0
    playerGl['sql'].loses = 0
    playerGl['sql'].ties = 0
    if playerGl['sql'].steamLink:
        for update in Update.query.all():
            player = {}
            for gameType in GameType.query.all():
                gameTypeId = str(gameType.id)
                player[gameTypeId] = {
                    'wins': 0,
                    'loses': 0,
                    'ties': 0,
                    'winnerFactions': {},
                    'loserFactions': {},
                    'tieFactions': {},
                    'winnerFactionsAgainst': {},
                    'loserFactionsAgainst': {},
                    'tieFactionsAgainst': {},
                    'winnerMissions': {},
                    'loserMissions': {},
                    'tieMissions': {},
                    'winnerSecondaries': {},
                    'loserSecondaries': {},
                    'tieSecondaries': {},
                    'winnerPlayers': {},
                    'loserPlayers': {},
                    'tiePlayers': {}
                }
                for game in Game.query.filter(Game.date >= update.date).filter(Game.date <= update.dateEnd).filter_by(winnerId=playerGl['sql'].steamId).all():
                    if game.gameType == gameType.id or gameType.id == 0:
                        otherPl = Player.query.filter_by(steamId=game.loserId).first()
                        if game.tie:
                            playerGl['sql'].gamesTied.append(game)
                            playerGl['sql'].ties += 1
                            player[gameTypeId]['ties'] += 1
                            if otherPl:
                                if otherPl.username not in player[gameTypeId]['tiePlayers'].keys():
                                    player[gameTypeId]['tiePlayers'][otherPl.username] = 1
                                else:
                                    player[gameTypeId]['tiePlayers'][otherPl.username] += 1
                            if game.winFaction[0].name not in player[gameTypeId]['tieFactions'].keys():
                                player[gameTypeId]['tieFactions'][game.winFaction[0].name] = 1
                            else:
                                player[gameTypeId]['tieFactions'][game.winFaction[0].name] += 1
                            if game.losFaction[0].name not in player[gameTypeId]['tieFactionsAgainst'].keys():
                                player[gameTypeId]['tieFactionsAgainst'][game.losFaction[0].name] = 1
                            else:
                                player[gameTypeId]['tieFactionsAgainst'][game.losFaction[0].name] += 1
                            if game.mission[0].name not in player[gameTypeId]['tieMissions'].keys():
                                player[gameTypeId]['tieMissions'][game.mission[0].name] = 1
                            else:
                                player[gameTypeId]['tieMissions'][game.mission[0].name] += 1
                            if game.winSecondaryFirst[0].name not in player[gameTypeId]['tieSecondaries'].keys():
                                player[gameTypeId]['tieSecondaries'][game.winSecondaryFirst[0].name] = 1
                            else:
                                player[gameTypeId]['tieSecondaries'][game.winSecondaryFirst[0].name] += 1
                            if game.winSecondarySecond[0].name not in player[gameTypeId]['tieSecondaries'].keys():
                                player[gameTypeId]['tieSecondaries'][game.winSecondarySecond[0].name] = 1
                            else:
                                player[gameTypeId]['tieSecondaries'][game.winSecondarySecond[0].name] += 1
                            if game.winSecondaryThird[0].name not in player[gameTypeId]['tieSecondaries'].keys():
                                player[gameTypeId]['tieSecondaries'][game.winSecondaryThird[0].name] = 1
                            else:
                                player[gameTypeId]['tieSecondaries'][game.winSecondaryThird[0].name] += 1
                        else:
                            playerGl['sql'].gamesWon.append(game)
                            playerGl['sql'].wins += 1
                            player[gameTypeId]['wins'] += 1
                            if otherPl:
                                if otherPl.username not in player[gameTypeId]['winnerPlayers'].keys():
                                    player[gameTypeId]['winnerPlayers'][otherPl.username] = 1
                                else:
                                    player[gameTypeId]['winnerPlayers'][otherPl.username] += 1
                            if game.winFaction[0].name not in player[gameTypeId]['winnerFactions'].keys():
                                player[gameTypeId]['winnerFactions'][game.winFaction[0].name] = 1
                            else:
                                player[gameTypeId]['winnerFactions'][game.winFaction[0].name] += 1
                            if game.losFaction[0].name not in player[gameTypeId]['winnerFactionsAgainst'].keys():
                                player[gameTypeId]['winnerFactionsAgainst'][game.losFaction[0].name] = 1
                            else:
                                player[gameTypeId]['winnerFactionsAgainst'][game.losFaction[0].name] += 1
                            if game.mission[0].name not in player[gameTypeId]['winnerMissions'].keys():
                                player[gameTypeId]['winnerMissions'][game.mission[0].name] = 1
                            else:
                                player[gameTypeId]['winnerMissions'][game.mission[0].name] += 1
                            if game.winSecondaryFirst[0].name not in player[gameTypeId]['winnerSecondaries'].keys():
                                player[gameTypeId]['winnerSecondaries'][game.winSecondaryFirst[0].name] = 1
                            else:
                                player[gameTypeId]['winnerSecondaries'][game.winSecondaryFirst[0].name] += 1
                            if game.winSecondarySecond[0].name not in player[gameTypeId]['winnerSecondaries'].keys():
                                player[gameTypeId]['winnerSecondaries'][game.winSecondarySecond[0].name] = 1
                            else:
                                player[gameTypeId]['winnerSecondaries'][game.winSecondarySecond[0].name] += 1
                            if game.winSecondaryThird[0].name not in player[gameTypeId]['winnerSecondaries'].keys():
                                player[gameTypeId]['winnerSecondaries'][game.winSecondaryThird[0].name] = 1
                            else:
                                player[gameTypeId]['winnerSecondaries'][game.winSecondaryThird[0].name] += 1
                        playerGl['sql'].score += game.winTotal
                for game in Game.query.filter(Game.date >= update.date).filter(Game.date <= update.dateEnd).filter_by(loserId=playerGl['sql'].steamId).all():
                    if game.gameType == gameType.id or gameType.id == 0:
                        otherPl = Player.query.filter_by(steamId=game.winnerId).first()
                        if game.tie:
                            playerGl['sql'].gamesTied.append(game)
                            playerGl['sql'].ties += 1
                            player[gameTypeId]['ties'] += 1
                            if otherPl:
                                if otherPl.username not in player[gameTypeId]['tiePlayers'].keys():
                                    player[gameTypeId]['tiePlayers'][otherPl.username] = 1
                                else:
                                    player[gameTypeId]['tiePlayers'][otherPl.username] += 1
                            if game.winFaction[0].name not in player[gameTypeId]['tieFactions'].keys():
                                player[gameTypeId]['tieFactions'][game.winFaction[0].name] = 1
                            else:
                                player[gameTypeId]['tieFactions'][game.winFaction[0].name] += 1
                            if game.winFaction[0].name not in player[gameTypeId]['tieFactionsAgainst'].keys():
                                player[gameTypeId]['tieFactionsAgainst'][game.winFaction[0].name] = 1
                            else:
                                player[gameTypeId]['tieFactionsAgainst'][game.winFaction[0].name] += 1
                            if game.mission[0].name not in player[gameTypeId]['tieMissions'].keys():
                                player[gameTypeId]['tieMissions'][game.mission[0].name] = 1
                            else:
                                player[gameTypeId]['tieMissions'][game.mission[0].name] += 1
                            if game.losSecondaryFirst[0].name not in player[gameTypeId]['tieSecondaries'].keys():
                                player[gameTypeId]['tieSecondaries'][game.losSecondaryFirst[0].name] = 1
                            else:
                                player[gameTypeId]['tieSecondaries'][game.losSecondaryFirst[0].name] += 1
                            if game.losSecondarySecond[0].name not in player[gameTypeId]['tieSecondaries'].keys():
                                player[gameTypeId]['tieSecondaries'][game.losSecondarySecond[0].name] = 1
                            else:
                                player[gameTypeId]['tieSecondaries'][game.losSecondarySecond[0].name] += 1
                            if game.losSecondaryThird[0].name not in player[gameTypeId]['tieSecondaries'].keys():
                                player[gameTypeId]['tieSecondaries'][game.losSecondaryThird[0].name] = 1
                            else:
                                player[gameTypeId]['tieSecondaries'][game.losSecondaryThird[0].name] += 1
                        else:
                            playerGl['sql'].gamesLost.append(game)
                            playerGl['sql'].loses += 1
                            player[gameTypeId]['loses'] += 1
                            if otherPl:
                                if otherPl.username not in player[gameTypeId]['loserPlayers'].keys():
                                    player[gameTypeId]['loserPlayers'][otherPl.username] = 1
                                else:
                                    player[gameTypeId]['loserPlayers'][otherPl.username] += 1
                            if game.losFaction[0].name not in player[gameTypeId]['loserFactions'].keys():
                                player[gameTypeId]['loserFactions'][game.losFaction[0].name] = 1
                            else:
                                player[gameTypeId]['loserFactions'][game.losFaction[0].name] += 1
                            if game.winFaction[0].name not in player[gameTypeId]['loserFactionsAgainst'].keys():
                                player[gameTypeId]['loserFactionsAgainst'][game.winFaction[0].name] = 1
                            else:
                                player[gameTypeId]['loserFactionsAgainst'][game.winFaction[0].name] += 1
                            if game.mission[0].name not in player[gameTypeId]['loserMissions'].keys():
                                player[gameTypeId]['loserMissions'][game.mission[0].name] = 1
                            else:
                                player[gameTypeId]['loserMissions'][game.mission[0].name] += 1
                            if game.losSecondaryFirst[0].name not in player[gameTypeId]['loserSecondaries'].keys():
                                player[gameTypeId]['loserSecondaries'][game.losSecondaryFirst[0].name] = 1
                            else:
                                player[gameTypeId]['loserSecondaries'][game.losSecondaryFirst[0].name] += 1
                            if game.losSecondarySecond[0].name not in player[gameTypeId]['loserSecondaries'].keys():
                                player[gameTypeId]['loserSecondaries'][game.losSecondarySecond[0].name] = 1
                            else:
                                player[gameTypeId]['loserSecondaries'][game.losSecondarySecond[0].name] += 1
                            if game.losSecondaryThird[0].name not in player[gameTypeId]['loserSecondaries'].keys():
                                player[gameTypeId]['loserSecondaries'][game.losSecondaryThird[0].name] = 1
                            else:
                                player[gameTypeId]['loserSecondaries'][game.losSecondaryThird[0].name] += 1
                        playerGl['sql'].score += game.losTotal
                player[gameTypeId]['totalGames'] = player[gameTypeId]['wins'] + player[gameTypeId]['loses'] + player[gameTypeId]['ties']
                try:
                    player[gameTypeId]['winRate'] = float("{:.2f}".format(player[gameTypeId]['wins'] * 100 / player[gameTypeId]['totalGames']))
                except ZeroDivisionError:
                    player[gameTypeId]['winRate'] = 0
                playerGl['sql'].rank = [Rank.query.filter(Rank.score <= playerGl['sql'].score).order_by(desc(Rank.score)).first()]
                for otherPl in player[gameTypeId]['winnerPlayers'].keys():
                    oPl = Player.query.filter_by(username=otherPl).first()
                    tot = player[gameTypeId]['winnerPlayers'][otherPl] + (
                        player[gameTypeId]['loserPlayers'][otherPl] if otherPl in player[gameTypeId]['loserPlayers'].keys() else 0) + (
                              player[gameTypeId]['tiePlayers'][otherPl] if otherPl in player[gameTypeId]['tiePlayers'].keys() else 0)
                    rate = PlayerWinRatesPlayer.query.filter_by(fromUpdate=update.id).filter_by(fromGameType=gameType.id).filter_by(player1=playerGl['sql'].id).filter_by(player2=oPl.id).first()
                    if not rate:
                        rate = PlayerWinRatesPlayer(
                            player1=playerGl['sql'].id,
                            player2=oPl.id,
                            fromUpdate=update.id,
                            fromGameType=gameType.id,
                        )
                    rate.rate1 = float("{:.2f}".format(player[gameTypeId]['winnerPlayers'][otherPl] * 100 / tot)) if tot > 0 else 0
                    db.session.add(rate)
                    db.session.commit()
                for otherPl in player[gameTypeId]['loserPlayers'].keys():
                    oPl = Player.query.filter_by(username=otherPl).first()
                    tot = player[gameTypeId]['loserPlayers'][otherPl] + (
                        player[gameTypeId]['winnerPlayers'][otherPl] if otherPl in player[gameTypeId]['winnerPlayers'].keys() else 0) + (
                              player[gameTypeId]['tiePlayers'][otherPl] if otherPl in player[gameTypeId]['tiePlayers'].keys() else 0)
                    rate = PlayerWinRatesPlayer.query.filter_by(fromUpdate=update.id).filter_by(fromGameType=gameType.id).filter_by(player1=playerGl['sql'].id).filter_by(player2=oPl.id).first()
                    if not rate:
                        rate = PlayerWinRatesPlayer(
                            player1=playerGl['sql'].id,
                            player2=oPl.id,
                            fromUpdate=update.id,
                            fromGameType=gameType.id,
                        )
                    rate.rate2 = float("{:.2f}".format(player[gameTypeId]['loserPlayers'][otherPl] * 100 / tot)) if tot > 0 else 0
                    db.session.add(rate)
                    db.session.commit()
                for otherPl in player[gameTypeId]['tiePlayers'].keys():
                    oPl = Player.query.filter_by(username=otherPl).first()
                    tot = player[gameTypeId]['tiePlayers'][otherPl] + (
                        player[gameTypeId]['winnerPlayers'][otherPl] if otherPl in player[gameTypeId]['winnerPlayers'].keys() else 0) + (
                              player[gameTypeId]['loserPlayers'][otherPl] if otherPl in player[gameTypeId]['loserPlayers'].keys() else 0)
                    rate = PlayerWinRatesPlayer.query.filter_by(fromUpdate=update.id).filter_by(fromGameType=gameType.id).filter_by(player1=playerGl['sql'].id).filter_by(player2=oPl.id).first()
                    if not rate:
                        rate = PlayerWinRatesPlayer(
                            player1=playerGl['sql'].id,
                            player2=oPl.id,
                            fromUpdate=update.id,
                            fromGameType=gameType.id,
                        )
                    rate.rate3 = float("{:.2f}".format(player[gameTypeId]['tiePlayers'][otherPl] * 100 / tot)) if tot > 0 else 0
                    db.session.add(rate)
                    db.session.commit()
                for faction in player[gameTypeId]['winnerFactions'].keys():
                    fct = Faction.query.filter_by(name=faction).first()
                    tot = player[gameTypeId]['winnerFactions'][faction] + (
                        player[gameTypeId]['loserFactions'][faction] if faction in player[gameTypeId]['loserFactions'].keys() else 0) + (
                              player[gameTypeId]['tieFactions'][faction] if faction in player[gameTypeId]['tieFactions'].keys() else 0)
                    rate = PlayerWinRates.query.filter_by(fromUpdate=update.id).filter_by(fromGameType=gameType.id).filter_by(player=playerGl['sql'].id).filter_by(faction=fct.id).first()
                    if not rate:
                        rate = PlayerWinRates(
                            player=playerGl['sql'].id,
                            faction=fct.id,
                            fromUpdate=update.id,
                            fromGameType=gameType.id,
                        )
                    rate.rate1 = float("{:.2f}".format(player[gameTypeId]['winnerFactions'][faction] * 100 / tot)) if tot > 0 else 0
                    db.session.add(rate)
                    db.session.commit()
                for faction in player[gameTypeId]['loserFactions'].keys():
                    fct = Faction.query.filter_by(name=faction).first()
                    tot = player[gameTypeId]['loserFactions'][faction] + (
                        player[gameTypeId]['winnerFactions'][faction] if faction in player[gameTypeId]['winnerFactions'].keys() else 0) + (
                              player[gameTypeId]['tieFactions'][faction] if faction in player[gameTypeId]['tieFactions'].keys() else 0)
                    rate = PlayerWinRates.query.filter_by(fromUpdate=update.id).filter_by(fromGameType=gameType.id).filter_by(player=playerGl['sql'].id).filter_by(faction=fct.id).first()
                    if not rate:
                        rate = PlayerWinRates(
                            player=playerGl['sql'].id,
                            faction=fct.id,
                            fromUpdate=update.id,
                            fromGameType=gameType.id,
                        )
                    rate.rate2 = float("{:.2f}".format(player[gameTypeId]['loserFactions'][faction] * 100 / tot)) if tot > 0 else 0
                    db.session.add(rate)
                    db.session.commit()
                for faction in player[gameTypeId]['tieFactions'].keys():
                    fct = Faction.query.filter_by(name=faction).first()
                    tot = player[gameTypeId]['tieFactions'][faction] + (
                        player[gameTypeId]['winnerFactions'][faction] if faction in player[gameTypeId]['winnerFactions'].keys() else 0) + (
                              player[gameTypeId]['loserFactions'][faction] if faction in player[gameTypeId]['loserFactions'].keys() else 0)
                    rate = PlayerWinRates.query.filter_by(fromUpdate=update.id).filter_by(fromGameType=gameType.id).filter_by(player=playerGl['sql'].id).filter_by(faction=fct.id).first()
                    if not rate:
                        rate = PlayerWinRates(
                            player=playerGl['sql'].id,
                            faction=fct.id,
                            fromUpdate=update.id,
                            fromGameType=gameType.id,
                        )
                    rate.rate3 = float("{:.2f}".format(player[gameTypeId]['tieFactions'][faction] * 100 / tot)) if tot > 0 else 0
                    db.session.add(rate)
                    db.session.commit()

                for faction in player[gameTypeId]['winnerFactionsAgainst'].keys():
                    fct = Faction.query.filter_by(name=faction).first()
                    tot = player[gameTypeId]['winnerFactionsAgainst'][faction] + (
                        player[gameTypeId]['loserFactionsAgainst'][faction] if faction in player[gameTypeId]['loserFactionsAgainst'].keys() else 0) + (
                              player[gameTypeId]['tieFactionsAgainst'][faction] if faction in player[gameTypeId]['tieFactionsAgainst'].keys() else 0)
                    rate = PlayerWinRatesAgainst.query.filter_by(fromUpdate=update.id).filter_by(fromGameType=gameType.id).filter_by(player=playerGl['sql'].id).filter_by(faction=fct.id).first()
                    if not rate:
                        rate = PlayerWinRatesAgainst(
                            player=playerGl['sql'].id,
                            faction=fct.id,
                            fromUpdate=update.id,
                            fromGameType=gameType.id,
                        )
                    rate.rate1 = float("{:.2f}".format(player[gameTypeId]['winnerFactionsAgainst'][faction] * 100 / tot)) if tot > 0 else 0
                    db.session.add(rate)
                    db.session.commit()
                for faction in player[gameTypeId]['loserFactionsAgainst'].keys():
                    fct = Faction.query.filter_by(name=faction).first()
                    tot = player[gameTypeId]['loserFactionsAgainst'][faction] + (
                        player[gameTypeId]['winnerFactionsAgainst'][faction] if faction in player[gameTypeId][
                            'winnerFactionsAgainst'].keys() else 0) + (
                              player[gameTypeId]['tieFactionsAgainst'][faction] if faction in player[gameTypeId]['tieFactionsAgainst'].keys() else 0)
                    rate = PlayerWinRatesAgainst.query.filter_by(fromUpdate=update.id).filter_by(fromGameType=gameType.id).filter_by(player=playerGl['sql'].id).filter_by(faction=fct.id).first()
                    if not rate:
                        rate = PlayerWinRatesAgainst(
                            player=playerGl['sql'].id,
                            faction=fct.id,
                            fromUpdate=update.id,
                            fromGameType=gameType.id,
                        )
                    rate.rate2 = float("{:.2f}".format(player[gameTypeId]['loserFactionsAgainst'][faction] * 100 / tot)) if tot > 0 else 0
                    db.session.add(rate)
                    db.session.commit()
                for faction in player[gameTypeId]['tieFactionsAgainst'].keys():
                    fct = Faction.query.filter_by(name=faction).first()
                    tot = player[gameTypeId]['tieFactionsAgainst'][faction] + (
                        player[gameTypeId]['winnerFactionsAgainst'][faction] if faction in player[gameTypeId][
                            'winnerFactionsAgainst'].keys() else 0) + (
                              player[gameTypeId]['loserFactionsAgainst'][faction] if faction in player[gameTypeId][
                                  'loserFactionsAgainst'].keys() else 0)
                    rate = PlayerWinRatesAgainst.query.filter_by(fromUpdate=update.id).filter_by(fromGameType=gameType.id).filter_by(player=playerGl['sql'].id).filter_by(faction=fct.id).first()
                    if not rate:
                        rate = PlayerWinRatesAgainst(
                            player=playerGl['sql'].id,
                            faction=fct.id,
                            fromUpdate=update.id,
                            fromGameType=gameType.id,
                        )
                    rate.rate3 = float("{:.2f}".format(player[gameTypeId]['tieFactionsAgainst'][faction] * 100 / tot)) if tot > 0 else 0
                    db.session.add(rate)
                    db.session.commit()

                for mission in player[gameTypeId]['winnerMissions'].keys():
                    fct = Mission.query.filter_by(name=mission).first()
                    tot = player[gameTypeId]['winnerMissions'][mission] + (
                        player[gameTypeId]['loserMissions'][mission] if mission in player[gameTypeId]['loserMissions'].keys() else 0) + (
                              player[gameTypeId]['tieMissions'][mission] if mission in player[gameTypeId]['tieMissions'].keys() else 0)
                    rate = PlayerMissionRates.query.filter_by(fromUpdate=update.id).filter_by(fromGameType=gameType.id).filter_by(player=playerGl['sql'].id).filter_by(mission=fct.id).first()
                    if not rate:
                        rate = PlayerMissionRates(
                            player=playerGl['sql'].id,
                            mission=fct.id,
                            fromUpdate=update.id,
                            fromGameType=gameType.id,
                        )
                    rate.rate1 = float("{:.2f}".format(player[gameTypeId]['winnerMissions'][mission] * 100 / tot)) if tot > 0 else 0
                    db.session.add(rate)
                    db.session.commit()
                for mission in player[gameTypeId]['loserMissions'].keys():
                    fct = Mission.query.filter_by(name=mission).first()
                    tot = player[gameTypeId]['loserMissions'][mission] + (
                        player[gameTypeId]['winnerMissions'][mission] if mission in player[gameTypeId]['winnerMissions'].keys() else 0) + (
                              player[gameTypeId]['tieMissions'][mission] if mission in player[gameTypeId]['tieMissions'].keys() else 0)
                    rate = PlayerMissionRates.query.filter_by(fromUpdate=update.id).filter_by(fromGameType=gameType.id).filter_by(player=playerGl['sql'].id).filter_by(mission=fct.id).first()
                    if not rate:
                        rate = PlayerMissionRates(
                            player=playerGl['sql'].id,
                            mission=fct.id,
                            fromUpdate=update.id,
                            fromGameType=gameType.id,
                        )
                    rate.rate2 = float("{:.2f}".format(player[gameTypeId]['loserMissions'][mission] * 100 / tot)) if tot > 0 else 0
                    db.session.add(rate)
                    db.session.commit()
                for mission in player[gameTypeId]['tieMissions'].keys():
                    fct = Mission.query.filter_by(name=mission).first()
                    tot = player[gameTypeId]['tieMissions'][mission] + (
                        player[gameTypeId]['winnerMissions'][mission] if mission in player[gameTypeId]['winnerMissions'].keys() else 0) + (
                              player[gameTypeId]['loserMissions'][mission] if mission in player[gameTypeId]['loserMissions'].keys() else 0)
                    rate = PlayerMissionRates.query.filter_by(fromUpdate=update.id).filter_by(fromGameType=gameType.id).filter_by(player=playerGl['sql'].id).filter_by(mission=fct.id).first()
                    if not rate:
                        rate = PlayerMissionRates(
                            player=playerGl['sql'].id,
                            mission=fct.id,
                            fromUpdate=update.id,
                            fromGameType=gameType.id,
                        )
                    rate.rate3 = float("{:.2f}".format(player[gameTypeId]['tieMissions'][mission] * 100 / tot)) if tot > 0 else 0
                    db.session.add(rate)
                    db.session.commit()
                for secondary in player[gameTypeId]['winnerSecondaries'].keys():
                    fct = Secondary.query.filter_by(name=secondary).first()
                    tot = player[gameTypeId]['winnerSecondaries'][secondary] + (
                        player[gameTypeId]['loserSecondaries'][secondary] if secondary in player[gameTypeId]['loserSecondaries'].keys() else 0) + (
                              player[gameTypeId]['tieSecondaries'][secondary] if secondary in player[gameTypeId]['tieSecondaries'].keys() else 0)
                    rate = PlayerSecondaryRates.query.filter_by(fromUpdate=update.id).filter_by(fromGameType=gameType.id).filter_by(player=playerGl['sql'].id).filter_by(secondary=fct.id).first()
                    if not rate:
                        rate = PlayerSecondaryRates(
                            player=playerGl['sql'].id,
                            secondary=fct.id,
                            fromUpdate=update.id,
                            fromGameType=gameType.id,
                        )
                    rate.rate1 = float("{:.2f}".format(player[gameTypeId]['winnerSecondaries'][secondary] * 100 / tot)) if tot > 0 else 0
                    db.session.add(rate)
                    db.session.commit()
                for secondary in player[gameTypeId]['loserSecondaries'].keys():
                    fct = Secondary.query.filter_by(name=secondary).first()
                    tot = player[gameTypeId]['loserSecondaries'][secondary] + (
                        player[gameTypeId]['winnerSecondaries'][secondary] if secondary in player[gameTypeId]['winnerSecondaries'].keys() else 0) + (
                              player[gameTypeId]['tieSecondaries'][secondary] if secondary in player[gameTypeId]['tieSecondaries'].keys() else 0)
                    rate = PlayerSecondaryRates.query.filter_by(fromUpdate=update.id).filter_by(fromGameType=gameType.id).filter_by(player=playerGl['sql'].id).filter_by(secondary=fct.id).first()
                    if not rate:
                        rate = PlayerSecondaryRates(
                            player=playerGl['sql'].id,
                            secondary=fct.id,
                            fromUpdate=update.id,
                            fromGameType=gameType.id,
                        )
                    rate.rate2 = float("{:.2f}".format(player[gameTypeId]['loserSecondaries'][secondary] * 100 / tot)) if tot > 0 else 0
                    db.session.add(rate)
                    db.session.commit()
                for secondary in player[gameTypeId]['tieSecondaries'].keys():
                    fct = Secondary.query.filter_by(name=secondary).first()
                    tot = player[gameTypeId]['tieSecondaries'][secondary] + (
                        player[gameTypeId]['winnerSecondaries'][secondary] if secondary in player[gameTypeId]['winnerSecondaries'].keys() else 0) + (
                              player[gameTypeId]['loserSecondaries'][secondary] if secondary in player[gameTypeId]['loserSecondaries'].keys() else 0)
                    rate = PlayerSecondaryRates.query.filter_by(fromUpdate=update.id).filter_by(fromGameType=gameType.id).filter_by(player=playerGl['sql'].id).filter_by(secondary=fct.id).first()
                    if not rate:
                        rate = PlayerSecondaryRates(
                            player=playerGl['sql'].id,
                            secondary=fct.id,
                            fromUpdate=update.id,
                            fromGameType=gameType.id,
                        )
                    rate.rate3 = float("{:.2f}".format(player[gameTypeId]['tieSecondaries'][secondary] * 100 / tot)) if tot > 0 else 0
                    db.session.add(rate)
                    db.session.commit()
            playerGl['updates'][str(update.id)] = player
        db.session.add(playerGl['sql'])
        db.session.commit()
    return playerGl


def getPlayers():
    players = {}
    for player in Player.query.all():
        playerInd = getPlayer(player.id)
        if playerInd['sql'].steamLink:
            players[playerInd['sql'].shortName] = playerInd
    return [player for player in players.values()]


def getPlayer(pl):
    playerGl = {
        'sql': Player.query.filter_by(id=pl).first(),
        'updates': {}
    }
    if playerGl['sql']:
        if playerGl['sql'].steamLink:
            if playerGl['sql'].allowSharing:
                playerGl['name'] = playerGl['sql'].username
                for update in Update.query.all():
                    player = {}
                    for gameType in GameType.query.all():
                        gameTypeId = str(gameType.id)
                        player[gameTypeId] = {
                            'factionRates': [], 'factionRatesAgainst': [],
                            'missionRates': [], 'secondaryRates': [],
                            'playerRates': [],
                        }
                        if gameType.id == 0:
                            player[gameTypeId]['wins'] = len(Game.query.filter(Game.date >= update.date).filter(Game.date <= update.dateEnd).filter_by(winnerId=playerGl['sql'].steamId).filter_by(tie=False).all())
                            player[gameTypeId]['loses'] = len(Game.query.filter(Game.date >= update.date).filter(Game.date <= update.dateEnd).filter_by(loserId=playerGl['sql'].steamId).filter_by(tie=False).all())
                            player[gameTypeId]['ties'] = len(Game.query.filter(Game.date >= update.date).filter(Game.date <= update.dateEnd).filter_by(winnerId=playerGl['sql'].steamId).filter_by(tie=True).all()) + len(Game.query.filter(Game.date >= update.date).filter(Game.date <= update.dateEnd).filter_by(loserId=playerGl['sql'].steamId).filter_by(tie=True).all())
                        else:
                            player[gameTypeId]['wins'] = len(Game.query.filter_by(gameType=gameType.id).filter(Game.date >= update.date).filter(Game.date <= update.dateEnd).filter_by(winnerId=playerGl['sql'].steamId).filter_by(tie=False).all())
                            player[gameTypeId]['loses'] = len(Game.query.filter_by(gameType=gameType.id).filter(Game.date >= update.date).filter(Game.date <= update.dateEnd).filter_by(loserId=playerGl['sql'].steamId).filter_by(tie=False).all())
                            player[gameTypeId]['ties'] = len(Game.query.filter_by(gameType=gameType.id).filter(Game.date >= update.date).filter(Game.date <= update.dateEnd).filter_by(winnerId=playerGl['sql'].steamId).filter_by(tie=True).all()) + len(Game.query.filter(Game.date >= update.date).filter(Game.date <= update.dateEnd).filter_by(loserId=playerGl['sql'].steamId).filter_by(tie=True).all())
                        player[gameTypeId]['totalGames'] = player[gameTypeId]['wins'] + player[gameTypeId]['loses'] + player[gameTypeId]['ties']
                        try:
                            player[gameTypeId]['winRate'] = float("{:.2f}".format(player[gameTypeId]['wins'] * 100 / player[gameTypeId]['totalGames']))
                        except ZeroDivisionError:
                            player[gameTypeId]['winRate'] = 0
                        for rate in PlayerWinRates.query.filter_by(fromUpdate=update.id).filter_by(fromGameType=gameType.id).filter_by(player=playerGl['sql'].id).order_by(
                                desc(PlayerWinRates.rate1)).all():
                            fct = Faction.query.filter_by(id=rate.faction).first()
                            player[gameTypeId]['factionRates'].append({
                                'id': fct.id,
                                'name': fct.name,
                                'shortName': fct.shortName,
                                'winRate': rate.rate1 if rate.rate1 else 0,
                                'loseRate': rate.rate2 if rate.rate2 else 0,
                                'tieRate': rate.rate3 if rate.rate3 else 0,
                                'games': rate.games
                            })
                        for rate in PlayerWinRatesAgainst.query.filter_by(fromUpdate=update.id).filter_by(fromGameType=gameType.id).filter_by(player=playerGl['sql'].id).order_by(
                                desc(PlayerWinRatesAgainst.rate1)).all():
                            fct = Faction.query.filter_by(id=rate.faction).first()
                            player[gameTypeId]['factionRatesAgainst'].append({
                                'id': fct.id,
                                'name': fct.name,
                                'shortName': fct.shortName,
                                'winRate': rate.rate1 if rate.rate1 else 0,
                                'loseRate': rate.rate2 if rate.rate2 else 0,
                                'tieRate': rate.rate3 if rate.rate3 else 0,
                                'games': rate.games
                            })
                        for rate in PlayerMissionRates.query.filter_by(fromUpdate=update.id).filter_by(fromGameType=gameType.id).filter_by(player=playerGl['sql'].id).order_by(
                                desc(PlayerMissionRates.rate1)).all():
                            ms = Mission.query.filter_by(id=rate.mission).first()
                            player[gameTypeId]['missionRates'].append({
                                'id': ms.id,
                                'name': ms.name,
                                'shortName': ms.shortName,
                                'winRate': rate.rate1 if rate.rate1 else 0,
                                'loseRate': rate.rate2 if rate.rate2 else 0,
                                'tieRate': rate.rate3 if rate.rate3 else 0,
                                'games': rate.games
                            })
                        for rate in PlayerSecondaryRates.query.filter_by(fromUpdate=update.id).filter_by(fromGameType=gameType.id).filter_by(player=playerGl['sql'].id).order_by(
                                desc(PlayerSecondaryRates.rate1)).all():
                            sec = Secondary.query.filter_by(id=rate.secondary).first()
                            player[gameTypeId]['secondaryRates'].append({
                                'id': sec.id,
                                'name': sec.name,
                                'shortName': sec.shortName,
                                'winRate': rate.rate1 if rate.rate1 else 0,
                                'loseRate': rate.rate2 if rate.rate2 else 0,
                                'tieRate': rate.rate3 if rate.rate3 else 0,
                                'games': rate.games
                            })
                        for rate in PlayerWinRatesPlayer.query.filter_by(fromUpdate=update.id).filter_by(fromGameType=gameType.id).filter_by(player1=playerGl['sql'].id).order_by(
                                desc(PlayerWinRatesPlayer.rate1)).all():
                            oPl = Player.query.filter_by(id=rate.player2).first()
                            if oPl.allowSharing:
                                player[gameTypeId]['playerRates'].append({
                                    'id': oPl.id,
                                    'name': oPl.username,
                                    'winRate': rate.rate1 if rate.rate1 else 0,
                                    'loseRate': rate.rate2 if rate.rate2 else 0,
                                    'tieRate': rate.rate3 if rate.rate3 else 0,
                                    'games': rate.games
                                })
                    playerGl['updates'][str(update.id)] = player
            else:
                playerGl['name'] = "Anonymous"
    return playerGl


def getPlayerById(userId):
    return Player.query.filter_by(id=userId).first()
