from sqlalchemy import desc
from database import (
    Game, Player, Mission, Rank, Secondary, Faction,
    PlayerMissionRates,
    PlayerWinRates, PlayerWinRatesPlayer, PlayerSecondaryRates,
    PlayerWinRatesAgainst, Update, GameType, Edition
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
            for edition in Edition.query.all():
                editionId = str(edition.id)
                player[editionId] = {}
                for gameType in GameType.query.all():
                    gameTypeId = str(gameType.id)
                    player[editionId][gameTypeId] = {
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
                    for game in Game.query.filter(Game.update == update.id if update.id > 1 else Game.update).filter(Game.gameType == gameType.id if gameType.id > 1 else Game.gameType).filter(Game.edition == edition.id if edition.id > 1 else Game.edition).filter_by(winnerId=playerGl['sql'].steamId).all():
                        if game.gameType == gameType.id or gameType.id == 1:
                            otherPl = Player.query.filter_by(steamId=game.loserId).first()
                            if game.tie:
                                playerGl['sql'].gamesTied.append(game)
                                playerGl['sql'].ties += 1
                                player[editionId][gameTypeId]['ties'] += 1
                                if otherPl:
                                    if otherPl.username not in player[editionId][gameTypeId]['tiePlayers'].keys():
                                        player[editionId][gameTypeId]['tiePlayers'][otherPl.username] = 1
                                    else:
                                        player[editionId][gameTypeId]['tiePlayers'][otherPl.username] += 1
                                if game.winFaction[0].name not in player[editionId][gameTypeId]['tieFactions'].keys():
                                    player[editionId][gameTypeId]['tieFactions'][game.winFaction[0].name] = 1
                                else:
                                    player[editionId][gameTypeId]['tieFactions'][game.winFaction[0].name] += 1
                                if game.losFaction[0].name not in player[editionId][gameTypeId]['tieFactionsAgainst'].keys():
                                    player[editionId][gameTypeId]['tieFactionsAgainst'][game.losFaction[0].name] = 1
                                else:
                                    player[editionId][gameTypeId]['tieFactionsAgainst'][game.losFaction[0].name] += 1
                                if game.mission[0].name not in player[editionId][gameTypeId]['tieMissions'].keys():
                                    player[editionId][gameTypeId]['tieMissions'][game.mission[0].name] = 1
                                else:
                                    player[editionId][gameTypeId]['tieMissions'][game.mission[0].name] += 1
                                if game.winSecondaryFirst[0].name not in player[editionId][gameTypeId]['tieSecondaries'].keys():
                                    player[editionId][gameTypeId]['tieSecondaries'][game.winSecondaryFirst[0].name] = 1
                                else:
                                    player[editionId][gameTypeId]['tieSecondaries'][game.winSecondaryFirst[0].name] += 1
                                if game.winSecondarySecond[0].name not in player[editionId][gameTypeId]['tieSecondaries'].keys():
                                    player[editionId][gameTypeId]['tieSecondaries'][game.winSecondarySecond[0].name] = 1
                                else:
                                    player[editionId][gameTypeId]['tieSecondaries'][game.winSecondarySecond[0].name] += 1
                                if game.winSecondaryThird[0].name not in player[editionId][gameTypeId]['tieSecondaries'].keys():
                                    player[editionId][gameTypeId]['tieSecondaries'][game.winSecondaryThird[0].name] = 1
                                else:
                                    player[editionId][gameTypeId]['tieSecondaries'][game.winSecondaryThird[0].name] += 1
                            else:
                                playerGl['sql'].gamesWon.append(game)
                                playerGl['sql'].wins += 1
                                player[editionId][gameTypeId]['wins'] += 1
                                if otherPl:
                                    if otherPl.username not in player[editionId][gameTypeId]['winnerPlayers'].keys():
                                        player[editionId][gameTypeId]['winnerPlayers'][otherPl.username] = 1
                                    else:
                                        player[editionId][gameTypeId]['winnerPlayers'][otherPl.username] += 1
                                if game.winFaction[0].name not in player[editionId][gameTypeId]['winnerFactions'].keys():
                                    player[editionId][gameTypeId]['winnerFactions'][game.winFaction[0].name] = 1
                                else:
                                    player[editionId][gameTypeId]['winnerFactions'][game.winFaction[0].name] += 1
                                if game.losFaction[0].name not in player[editionId][gameTypeId]['winnerFactionsAgainst'].keys():
                                    player[editionId][gameTypeId]['winnerFactionsAgainst'][game.losFaction[0].name] = 1
                                else:
                                    player[editionId][gameTypeId]['winnerFactionsAgainst'][game.losFaction[0].name] += 1
                                if game.mission[0].name not in player[editionId][gameTypeId]['winnerMissions'].keys():
                                    player[editionId][gameTypeId]['winnerMissions'][game.mission[0].name] = 1
                                else:
                                    player[editionId][gameTypeId]['winnerMissions'][game.mission[0].name] += 1
                                if game.winSecondaryFirst[0].name not in player[editionId][gameTypeId]['winnerSecondaries'].keys():
                                    player[editionId][gameTypeId]['winnerSecondaries'][game.winSecondaryFirst[0].name] = 1
                                else:
                                    player[editionId][gameTypeId]['winnerSecondaries'][game.winSecondaryFirst[0].name] += 1
                                if game.winSecondarySecond[0].name not in player[editionId][gameTypeId]['winnerSecondaries'].keys():
                                    player[editionId][gameTypeId]['winnerSecondaries'][game.winSecondarySecond[0].name] = 1
                                else:
                                    player[editionId][gameTypeId]['winnerSecondaries'][game.winSecondarySecond[0].name] += 1
                                if game.winSecondaryThird[0].name not in player[editionId][gameTypeId]['winnerSecondaries'].keys():
                                    player[editionId][gameTypeId]['winnerSecondaries'][game.winSecondaryThird[0].name] = 1
                                else:
                                    player[editionId][gameTypeId]['winnerSecondaries'][game.winSecondaryThird[0].name] += 1
                            playerGl['sql'].score += game.winTotal
                    for game in Game.query.filter(Game.update == update.id if update.id > 1 else Game.update).filter(Game.gameType == gameType.id if gameType.id > 1 else Game.gameType).filter(Game.edition == edition.id if edition.id > 1 else Game.edition).filter_by(loserId=playerGl['sql'].steamId).all():
                        if game.gameType == gameType.id or gameType.id == 1:
                            otherPl = Player.query.filter_by(steamId=game.winnerId).first()
                            if game.tie:
                                playerGl['sql'].gamesTied.append(game)
                                playerGl['sql'].ties += 1
                                player[editionId][gameTypeId]['ties'] += 1
                                if otherPl:
                                    if otherPl.username not in player[editionId][gameTypeId]['tiePlayers'].keys():
                                        player[editionId][gameTypeId]['tiePlayers'][otherPl.username] = 1
                                    else:
                                        player[editionId][gameTypeId]['tiePlayers'][otherPl.username] += 1
                                if game.winFaction[0].name not in player[editionId][gameTypeId]['tieFactions'].keys():
                                    player[editionId][gameTypeId]['tieFactions'][game.winFaction[0].name] = 1
                                else:
                                    player[editionId][gameTypeId]['tieFactions'][game.winFaction[0].name] += 1
                                if game.winFaction[0].name not in player[editionId][gameTypeId]['tieFactionsAgainst'].keys():
                                    player[editionId][gameTypeId]['tieFactionsAgainst'][game.winFaction[0].name] = 1
                                else:
                                    player[editionId][gameTypeId]['tieFactionsAgainst'][game.winFaction[0].name] += 1
                                if game.mission[0].name not in player[editionId][gameTypeId]['tieMissions'].keys():
                                    player[editionId][gameTypeId]['tieMissions'][game.mission[0].name] = 1
                                else:
                                    player[editionId][gameTypeId]['tieMissions'][game.mission[0].name] += 1
                                if game.losSecondaryFirst[0].name not in player[editionId][gameTypeId]['tieSecondaries'].keys():
                                    player[editionId][gameTypeId]['tieSecondaries'][game.losSecondaryFirst[0].name] = 1
                                else:
                                    player[editionId][gameTypeId]['tieSecondaries'][game.losSecondaryFirst[0].name] += 1
                                if game.losSecondarySecond[0].name not in player[editionId][gameTypeId]['tieSecondaries'].keys():
                                    player[editionId][gameTypeId]['tieSecondaries'][game.losSecondarySecond[0].name] = 1
                                else:
                                    player[editionId][gameTypeId]['tieSecondaries'][game.losSecondarySecond[0].name] += 1
                                if game.losSecondaryThird[0].name not in player[editionId][gameTypeId]['tieSecondaries'].keys():
                                    player[editionId][gameTypeId]['tieSecondaries'][game.losSecondaryThird[0].name] = 1
                                else:
                                    player[editionId][gameTypeId]['tieSecondaries'][game.losSecondaryThird[0].name] += 1
                            else:
                                playerGl['sql'].gamesLost.append(game)
                                playerGl['sql'].loses += 1
                                player[editionId][gameTypeId]['loses'] += 1
                                if otherPl:
                                    if otherPl.username not in player[editionId][gameTypeId]['loserPlayers'].keys():
                                        player[editionId][gameTypeId]['loserPlayers'][otherPl.username] = 1
                                    else:
                                        player[editionId][gameTypeId]['loserPlayers'][otherPl.username] += 1
                                if game.losFaction[0].name not in player[editionId][gameTypeId]['loserFactions'].keys():
                                    player[editionId][gameTypeId]['loserFactions'][game.losFaction[0].name] = 1
                                else:
                                    player[editionId][gameTypeId]['loserFactions'][game.losFaction[0].name] += 1
                                if game.winFaction[0].name not in player[editionId][gameTypeId]['loserFactionsAgainst'].keys():
                                    player[editionId][gameTypeId]['loserFactionsAgainst'][game.winFaction[0].name] = 1
                                else:
                                    player[editionId][gameTypeId]['loserFactionsAgainst'][game.winFaction[0].name] += 1
                                if game.mission[0].name not in player[editionId][gameTypeId]['loserMissions'].keys():
                                    player[editionId][gameTypeId]['loserMissions'][game.mission[0].name] = 1
                                else:
                                    player[editionId][gameTypeId]['loserMissions'][game.mission[0].name] += 1
                                if game.losSecondaryFirst[0].name not in player[editionId][gameTypeId]['loserSecondaries'].keys():
                                    player[editionId][gameTypeId]['loserSecondaries'][game.losSecondaryFirst[0].name] = 1
                                else:
                                    player[editionId][gameTypeId]['loserSecondaries'][game.losSecondaryFirst[0].name] += 1
                                if game.losSecondarySecond[0].name not in player[editionId][gameTypeId]['loserSecondaries'].keys():
                                    player[editionId][gameTypeId]['loserSecondaries'][game.losSecondarySecond[0].name] = 1
                                else:
                                    player[editionId][gameTypeId]['loserSecondaries'][game.losSecondarySecond[0].name] += 1
                                if game.losSecondaryThird[0].name not in player[editionId][gameTypeId]['loserSecondaries'].keys():
                                    player[editionId][gameTypeId]['loserSecondaries'][game.losSecondaryThird[0].name] = 1
                                else:
                                    player[editionId][gameTypeId]['loserSecondaries'][game.losSecondaryThird[0].name] += 1
                            playerGl['sql'].score += game.losTotal
                    player[editionId][gameTypeId]['totalGames'] = player[editionId][gameTypeId]['wins'] + player[editionId][gameTypeId]['loses'] + player[editionId][gameTypeId]['ties']
                    try:
                        player[editionId][gameTypeId]['winRate'] = float("{:.2f}".format(player[editionId][gameTypeId]['wins'] * 100 / player[editionId][gameTypeId]['totalGames']))
                    except ZeroDivisionError:
                        player[editionId][gameTypeId]['winRate'] = 0
                    playerGl['sql'].rank = [Rank.query.filter(Rank.score <= playerGl['sql'].score).order_by(desc(Rank.score)).first()]
                    for otherPl in player[editionId][gameTypeId]['winnerPlayers'].keys():
                        oPl = Player.query.filter_by(username=otherPl).first()
                        tot = player[editionId][gameTypeId]['winnerPlayers'][otherPl] + (
                            player[editionId][gameTypeId]['loserPlayers'][otherPl] if otherPl in player[editionId][gameTypeId]['loserPlayers'].keys() else 0) + (
                                  player[editionId][gameTypeId]['tiePlayers'][otherPl] if otherPl in player[editionId][gameTypeId]['tiePlayers'].keys() else 0)
                        rate = PlayerWinRatesPlayer.query.filter_by(fromUpdate=update.id).filter_by(fromGameType=gameType.id).filter_by(fromEdition=edition.id).filter_by(player1=playerGl['sql'].id).filter_by(player2=oPl.id).first()
                        if not rate:
                            rate = PlayerWinRatesPlayer(
                                player1=playerGl['sql'].id,
                                player2=oPl.id,
                                fromUpdate=update.id,
                                fromGameType=gameType.id,
                                fromEdition=edition.id,
                            )
                        rate.rate1 = float("{:.2f}".format(player[editionId][gameTypeId]['winnerPlayers'][otherPl] * 100 / tot)) if tot > 0 else 0
                        db.session.add(rate)
                        db.session.commit()
                    for otherPl in player[editionId][gameTypeId]['loserPlayers'].keys():
                        oPl = Player.query.filter_by(username=otherPl).first()
                        tot = player[editionId][gameTypeId]['loserPlayers'][otherPl] + (
                            player[editionId][gameTypeId]['winnerPlayers'][otherPl] if otherPl in player[editionId][gameTypeId]['winnerPlayers'].keys() else 0) + (
                                  player[editionId][gameTypeId]['tiePlayers'][otherPl] if otherPl in player[editionId][gameTypeId]['tiePlayers'].keys() else 0)
                        rate = PlayerWinRatesPlayer.query.filter_by(fromUpdate=update.id).filter_by(fromGameType=gameType.id).filter_by(fromEdition=edition.id).filter_by(player1=playerGl['sql'].id).filter_by(player2=oPl.id).first()
                        if not rate:
                            rate = PlayerWinRatesPlayer(
                                player1=playerGl['sql'].id,
                                player2=oPl.id,
                                fromUpdate=update.id,
                                fromGameType=gameType.id,
                                fromEdition=edition.id,
                            )
                        rate.rate2 = float("{:.2f}".format(player[editionId][gameTypeId]['loserPlayers'][otherPl] * 100 / tot)) if tot > 0 else 0
                        db.session.add(rate)
                        db.session.commit()
                    for otherPl in player[editionId][gameTypeId]['tiePlayers'].keys():
                        oPl = Player.query.filter_by(username=otherPl).first()
                        tot = player[editionId][gameTypeId]['tiePlayers'][otherPl] + (
                            player[editionId][gameTypeId]['winnerPlayers'][otherPl] if otherPl in player[editionId][gameTypeId]['winnerPlayers'].keys() else 0) + (
                                  player[editionId][gameTypeId]['loserPlayers'][otherPl] if otherPl in player[editionId][gameTypeId]['loserPlayers'].keys() else 0)
                        rate = PlayerWinRatesPlayer.query.filter_by(fromUpdate=update.id).filter_by(fromGameType=gameType.id).filter_by(fromEdition=edition.id).filter_by(player1=playerGl['sql'].id).filter_by(player2=oPl.id).first()
                        if not rate:
                            rate = PlayerWinRatesPlayer(
                                player1=playerGl['sql'].id,
                                player2=oPl.id,
                                fromUpdate=update.id,
                                fromGameType=gameType.id,
                                fromEdition=edition.id,
                            )
                        rate.rate3 = float("{:.2f}".format(player[editionId][gameTypeId]['tiePlayers'][otherPl] * 100 / tot)) if tot > 0 else 0
                        db.session.add(rate)
                        db.session.commit()
                    for faction in player[editionId][gameTypeId]['winnerFactions'].keys():
                        fct = Faction.query.filter_by(name=faction).first()
                        tot = player[editionId][gameTypeId]['winnerFactions'][faction] + (
                            player[editionId][gameTypeId]['loserFactions'][faction] if faction in player[editionId][gameTypeId]['loserFactions'].keys() else 0) + (
                                  player[editionId][gameTypeId]['tieFactions'][faction] if faction in player[editionId][gameTypeId]['tieFactions'].keys() else 0)
                        rate = PlayerWinRates.query.filter_by(fromUpdate=update.id).filter_by(fromGameType=gameType.id).filter_by(fromEdition=edition.id).filter_by(player=playerGl['sql'].id).filter_by(faction=fct.id).first()
                        if not rate:
                            rate = PlayerWinRates(
                                player=playerGl['sql'].id,
                                faction=fct.id,
                                fromUpdate=update.id,
                                fromGameType=gameType.id,
                                fromEdition=edition.id,
                            )
                        rate.rate1 = float("{:.2f}".format(player[editionId][gameTypeId]['winnerFactions'][faction] * 100 / tot)) if tot > 0 else 0
                        db.session.add(rate)
                        db.session.commit()
                    for faction in player[editionId][gameTypeId]['loserFactions'].keys():
                        fct = Faction.query.filter_by(name=faction).first()
                        tot = player[editionId][gameTypeId]['loserFactions'][faction] + (
                            player[editionId][gameTypeId]['winnerFactions'][faction] if faction in player[editionId][gameTypeId]['winnerFactions'].keys() else 0) + (
                                  player[editionId][gameTypeId]['tieFactions'][faction] if faction in player[editionId][gameTypeId]['tieFactions'].keys() else 0)
                        rate = PlayerWinRates.query.filter_by(fromUpdate=update.id).filter_by(fromGameType=gameType.id).filter_by(fromEdition=edition.id).filter_by(player=playerGl['sql'].id).filter_by(faction=fct.id).first()
                        if not rate:
                            rate = PlayerWinRates(
                                player=playerGl['sql'].id,
                                faction=fct.id,
                                fromUpdate=update.id,
                                fromGameType=gameType.id,
                                fromEdition=edition.id,
                            )
                        rate.rate2 = float("{:.2f}".format(player[editionId][gameTypeId]['loserFactions'][faction] * 100 / tot)) if tot > 0 else 0
                        db.session.add(rate)
                        db.session.commit()
                    for faction in player[editionId][gameTypeId]['tieFactions'].keys():
                        fct = Faction.query.filter_by(name=faction).first()
                        tot = player[editionId][gameTypeId]['tieFactions'][faction] + (
                            player[editionId][gameTypeId]['winnerFactions'][faction] if faction in player[editionId][gameTypeId]['winnerFactions'].keys() else 0) + (
                                  player[editionId][gameTypeId]['loserFactions'][faction] if faction in player[editionId][gameTypeId]['loserFactions'].keys() else 0)
                        rate = PlayerWinRates.query.filter_by(fromUpdate=update.id).filter_by(fromGameType=gameType.id).filter_by(fromEdition=edition.id).filter_by(player=playerGl['sql'].id).filter_by(faction=fct.id).first()
                        if not rate:
                            rate = PlayerWinRates(
                                player=playerGl['sql'].id,
                                faction=fct.id,
                                fromUpdate=update.id,
                                fromGameType=gameType.id,
                                fromEdition=edition.id,
                            )
                        rate.rate3 = float("{:.2f}".format(player[editionId][gameTypeId]['tieFactions'][faction] * 100 / tot)) if tot > 0 else 0
                        db.session.add(rate)
                        db.session.commit()

                    for faction in player[editionId][gameTypeId]['winnerFactionsAgainst'].keys():
                        fct = Faction.query.filter_by(name=faction).first()
                        tot = player[editionId][gameTypeId]['winnerFactionsAgainst'][faction] + (
                            player[editionId][gameTypeId]['loserFactionsAgainst'][faction] if faction in player[editionId][gameTypeId]['loserFactionsAgainst'].keys() else 0) + (
                                  player[editionId][gameTypeId]['tieFactionsAgainst'][faction] if faction in player[editionId][gameTypeId]['tieFactionsAgainst'].keys() else 0)
                        rate = PlayerWinRatesAgainst.query.filter_by(fromUpdate=update.id).filter_by(fromGameType=gameType.id).filter_by(fromEdition=edition.id).filter_by(player=playerGl['sql'].id).filter_by(faction=fct.id).first()
                        if not rate:
                            rate = PlayerWinRatesAgainst(
                                player=playerGl['sql'].id,
                                faction=fct.id,
                                fromUpdate=update.id,
                                fromGameType=gameType.id,
                                fromEdition=edition.id,
                            )
                        rate.rate1 = float("{:.2f}".format(player[editionId][gameTypeId]['winnerFactionsAgainst'][faction] * 100 / tot)) if tot > 0 else 0
                        db.session.add(rate)
                        db.session.commit()
                    for faction in player[editionId][gameTypeId]['loserFactionsAgainst'].keys():
                        fct = Faction.query.filter_by(name=faction).first()
                        tot = player[editionId][gameTypeId]['loserFactionsAgainst'][faction] + (
                            player[editionId][gameTypeId]['winnerFactionsAgainst'][faction] if faction in player[editionId][gameTypeId][
                                'winnerFactionsAgainst'].keys() else 0) + (
                                  player[editionId][gameTypeId]['tieFactionsAgainst'][faction] if faction in player[editionId][gameTypeId]['tieFactionsAgainst'].keys() else 0)
                        rate = PlayerWinRatesAgainst.query.filter_by(fromUpdate=update.id).filter_by(fromGameType=gameType.id).filter_by(fromEdition=edition.id).filter_by(player=playerGl['sql'].id).filter_by(faction=fct.id).first()
                        if not rate:
                            rate = PlayerWinRatesAgainst(
                                player=playerGl['sql'].id,
                                faction=fct.id,
                                fromUpdate=update.id,
                                fromGameType=gameType.id,
                                fromEdition=edition.id,
                            )
                        rate.rate2 = float("{:.2f}".format(player[editionId][gameTypeId]['loserFactionsAgainst'][faction] * 100 / tot)) if tot > 0 else 0
                        db.session.add(rate)
                        db.session.commit()
                    for faction in player[editionId][gameTypeId]['tieFactionsAgainst'].keys():
                        fct = Faction.query.filter_by(name=faction).first()
                        tot = player[editionId][gameTypeId]['tieFactionsAgainst'][faction] + (
                            player[editionId][gameTypeId]['winnerFactionsAgainst'][faction] if faction in player[editionId][gameTypeId][
                                'winnerFactionsAgainst'].keys() else 0) + (
                                  player[editionId][gameTypeId]['loserFactionsAgainst'][faction] if faction in player[editionId][gameTypeId][
                                      'loserFactionsAgainst'].keys() else 0)
                        rate = PlayerWinRatesAgainst.query.filter_by(fromUpdate=update.id).filter_by(fromGameType=gameType.id).filter_by(fromEdition=edition.id).filter_by(player=playerGl['sql'].id).filter_by(faction=fct.id).first()
                        if not rate:
                            rate = PlayerWinRatesAgainst(
                                player=playerGl['sql'].id,
                                faction=fct.id,
                                fromUpdate=update.id,
                                fromGameType=gameType.id,
                                fromEdition=edition.id,
                            )
                        rate.rate3 = float("{:.2f}".format(player[editionId][gameTypeId]['tieFactionsAgainst'][faction] * 100 / tot)) if tot > 0 else 0
                        db.session.add(rate)
                        db.session.commit()

                    for mission in player[editionId][gameTypeId]['winnerMissions'].keys():
                        fct = Mission.query.filter_by(name=mission).first()
                        tot = player[editionId][gameTypeId]['winnerMissions'][mission] + (
                            player[editionId][gameTypeId]['loserMissions'][mission] if mission in player[editionId][gameTypeId]['loserMissions'].keys() else 0) + (
                                  player[editionId][gameTypeId]['tieMissions'][mission] if mission in player[editionId][gameTypeId]['tieMissions'].keys() else 0)
                        rate = PlayerMissionRates.query.filter_by(fromUpdate=update.id).filter_by(fromGameType=gameType.id).filter_by(fromEdition=edition.id).filter_by(player=playerGl['sql'].id).filter_by(mission=fct.id).first()
                        if not rate:
                            rate = PlayerMissionRates(
                                player=playerGl['sql'].id,
                                mission=fct.id,
                                fromUpdate=update.id,
                                fromGameType=gameType.id,
                                fromEdition=edition.id,
                            )
                        rate.rate1 = float("{:.2f}".format(player[editionId][gameTypeId]['winnerMissions'][mission] * 100 / tot)) if tot > 0 else 0
                        db.session.add(rate)
                        db.session.commit()
                    for mission in player[editionId][gameTypeId]['loserMissions'].keys():
                        fct = Mission.query.filter_by(name=mission).first()
                        tot = player[editionId][gameTypeId]['loserMissions'][mission] + (
                            player[editionId][gameTypeId]['winnerMissions'][mission] if mission in player[editionId][gameTypeId]['winnerMissions'].keys() else 0) + (
                                  player[editionId][gameTypeId]['tieMissions'][mission] if mission in player[editionId][gameTypeId]['tieMissions'].keys() else 0)
                        rate = PlayerMissionRates.query.filter_by(fromUpdate=update.id).filter_by(fromGameType=gameType.id).filter_by(fromEdition=edition.id).filter_by(player=playerGl['sql'].id).filter_by(mission=fct.id).first()
                        if not rate:
                            rate = PlayerMissionRates(
                                player=playerGl['sql'].id,
                                mission=fct.id,
                                fromUpdate=update.id,
                                fromGameType=gameType.id,
                                fromEdition=edition.id,
                            )
                        rate.rate2 = float("{:.2f}".format(player[editionId][gameTypeId]['loserMissions'][mission] * 100 / tot)) if tot > 0 else 0
                        db.session.add(rate)
                        db.session.commit()
                    for mission in player[editionId][gameTypeId]['tieMissions'].keys():
                        fct = Mission.query.filter_by(name=mission).first()
                        tot = player[editionId][gameTypeId]['tieMissions'][mission] + (
                            player[editionId][gameTypeId]['winnerMissions'][mission] if mission in player[editionId][gameTypeId]['winnerMissions'].keys() else 0) + (
                                  player[editionId][gameTypeId]['loserMissions'][mission] if mission in player[editionId][gameTypeId]['loserMissions'].keys() else 0)
                        rate = PlayerMissionRates.query.filter_by(fromUpdate=update.id).filter_by(fromGameType=gameType.id).filter_by(fromEdition=edition.id).filter_by(player=playerGl['sql'].id).filter_by(mission=fct.id).first()
                        if not rate:
                            rate = PlayerMissionRates(
                                player=playerGl['sql'].id,
                                mission=fct.id,
                                fromUpdate=update.id,
                                fromGameType=gameType.id,
                                fromEdition=edition.id,
                            )
                        rate.rate3 = float("{:.2f}".format(player[editionId][gameTypeId]['tieMissions'][mission] * 100 / tot)) if tot > 0 else 0
                        db.session.add(rate)
                        db.session.commit()
                    for secondary in player[editionId][gameTypeId]['winnerSecondaries'].keys():
                        fct = Secondary.query.filter_by(name=secondary).first()
                        tot = player[editionId][gameTypeId]['winnerSecondaries'][secondary] + (
                            player[editionId][gameTypeId]['loserSecondaries'][secondary] if secondary in player[editionId][gameTypeId]['loserSecondaries'].keys() else 0) + (
                                  player[editionId][gameTypeId]['tieSecondaries'][secondary] if secondary in player[editionId][gameTypeId]['tieSecondaries'].keys() else 0)
                        rate = PlayerSecondaryRates.query.filter_by(fromUpdate=update.id).filter_by(fromGameType=gameType.id).filter_by(fromEdition=edition.id).filter_by(player=playerGl['sql'].id).filter_by(secondary=fct.id).first()
                        if not rate:
                            rate = PlayerSecondaryRates(
                                player=playerGl['sql'].id,
                                secondary=fct.id,
                                fromUpdate=update.id,
                                fromGameType=gameType.id,
                                fromEdition=edition.id,
                            )
                        rate.rate1 = float("{:.2f}".format(player[editionId][gameTypeId]['winnerSecondaries'][secondary] * 100 / tot)) if tot > 0 else 0
                        db.session.add(rate)
                        db.session.commit()
                    for secondary in player[editionId][gameTypeId]['loserSecondaries'].keys():
                        fct = Secondary.query.filter_by(name=secondary).first()
                        tot = player[editionId][gameTypeId]['loserSecondaries'][secondary] + (
                            player[editionId][gameTypeId]['winnerSecondaries'][secondary] if secondary in player[editionId][gameTypeId]['winnerSecondaries'].keys() else 0) + (
                                  player[editionId][gameTypeId]['tieSecondaries'][secondary] if secondary in player[editionId][gameTypeId]['tieSecondaries'].keys() else 0)
                        rate = PlayerSecondaryRates.query.filter_by(fromUpdate=update.id).filter_by(fromGameType=gameType.id).filter_by(fromEdition=edition.id).filter_by(player=playerGl['sql'].id).filter_by(secondary=fct.id).first()
                        if not rate:
                            rate = PlayerSecondaryRates(
                                player=playerGl['sql'].id,
                                secondary=fct.id,
                                fromUpdate=update.id,
                                fromGameType=gameType.id,
                                fromEdition=edition.id,
                            )
                        rate.rate2 = float("{:.2f}".format(player[editionId][gameTypeId]['loserSecondaries'][secondary] * 100 / tot)) if tot > 0 else 0
                        db.session.add(rate)
                        db.session.commit()
                    for secondary in player[editionId][gameTypeId]['tieSecondaries'].keys():
                        fct = Secondary.query.filter_by(name=secondary).first()
                        tot = player[editionId][gameTypeId]['tieSecondaries'][secondary] + (
                            player[editionId][gameTypeId]['winnerSecondaries'][secondary] if secondary in player[editionId][gameTypeId]['winnerSecondaries'].keys() else 0) + (
                                  player[editionId][gameTypeId]['loserSecondaries'][secondary] if secondary in player[editionId][gameTypeId]['loserSecondaries'].keys() else 0)
                        rate = PlayerSecondaryRates.query.filter_by(fromUpdate=update.id).filter_by(fromGameType=gameType.id).filter_by(fromEdition=edition.id).filter_by(player=playerGl['sql'].id).filter_by(secondary=fct.id).first()
                        if not rate:
                            rate = PlayerSecondaryRates(
                                player=playerGl['sql'].id,
                                secondary=fct.id,
                                fromUpdate=update.id,
                                fromGameType=gameType.id,
                                fromEdition=edition.id,
                            )
                        rate.rate3 = float("{:.2f}".format(player[editionId][gameTypeId]['tieSecondaries'][secondary] * 100 / tot)) if tot > 0 else 0
                        db.session.add(rate)
                        db.session.commit()
            playerGl['updates'][str(update.id)] = player
        db.session.add(playerGl['sql'])
        db.session.commit()
    return playerGl


def getPlayers(up, tp, ed):
    players = {}
    for player in Player.query.all():
        playerInd = getPlayer(player.id, up, tp, ed)
        if playerInd['sql'].steamLink:
            players[playerInd['sql'].shortName] = playerInd
    return [player for player in players.values()]


def getPlayer(pl, up, tp, ed):
    playerGl = {
        'sql': Player.query.filter_by(id=pl).first(),
        'rates': {}
    }
    if playerGl['sql']:
        if playerGl['sql'].steamLink:
            if playerGl['sql'].allowSharing:
                playerGl['name'] = playerGl['sql'].username
                player = {
                    'factionRates': [], 'factionRatesAgainst': [],
                    'missionRates': [], 'secondaryRates': [],
                    'playerRates': [], 'wins': 0, 'loses': 0,
                    'ties': 0,
                }
                for game in Game.query.filter(Game.update == up if up > 1 else Game.update).filter(Game.gameType == tp if tp > 1 else Game.gameType).filter(Game.edition == ed if ed > 1 else Game.edition).all():
                    if game.winnerId == playerGl['sql'].steamId:
                        if game.tie:
                            player['ties'] += 1
                        else:
                            player['wins'] += 1
                    if game.loserId == playerGl['sql'].steamId:
                        if game.tie:
                            player['ties'] += 1
                        else:
                            player['loses'] += 1
                player['totalGames'] = player['wins'] + player['loses'] + player['ties']
                try:
                    player['winRate'] = float("{:.2f}".format(player['wins'] * 100 / player['totalGames']))
                except ZeroDivisionError:
                    player['winRate'] = 0
                for rate in PlayerWinRates.query.filter_by(fromUpdate=up).filter_by(fromGameType=tp).filter_by(fromEdition=ed).filter_by(player=playerGl['sql'].id).order_by(desc(PlayerWinRates.rate1)).all():
                    fct = Faction.query.filter_by(id=rate.faction).first()
                    player['factionRates'].append({
                        'id': fct.id,
                        'name': fct.name,
                        'shortName': fct.shortName,
                        'winRate': rate.rate1 if rate.rate1 else 0,
                        'loseRate': rate.rate2 if rate.rate2 else 0,
                        'tieRate': rate.rate3 if rate.rate3 else 0,
                        'games': rate.games
                    })
                for rate in PlayerWinRatesAgainst.query.filter_by(fromUpdate=up).filter_by(fromGameType=tp).filter_by(fromEdition=ed).filter_by(player=playerGl['sql'].id).order_by(
                        desc(PlayerWinRatesAgainst.rate1)).all():
                    fct = Faction.query.filter_by(id=rate.faction).first()
                    player['factionRatesAgainst'].append({
                        'id': fct.id,
                        'name': fct.name,
                        'shortName': fct.shortName,
                        'winRate': rate.rate1 if rate.rate1 else 0,
                        'loseRate': rate.rate2 if rate.rate2 else 0,
                        'tieRate': rate.rate3 if rate.rate3 else 0,
                        'games': rate.games
                    })
                for rate in PlayerMissionRates.query.filter_by(fromUpdate=up).filter_by(fromGameType=tp).filter_by(fromEdition=ed).filter_by(player=playerGl['sql'].id).order_by(
                        desc(PlayerMissionRates.rate1)).all():
                    ms = Mission.query.filter_by(id=rate.mission).first()
                    player['missionRates'].append({
                        'id': ms.id,
                        'name': ms.name,
                        'shortName': ms.shortName,
                        'winRate': rate.rate1 if rate.rate1 else 0,
                        'loseRate': rate.rate2 if rate.rate2 else 0,
                        'tieRate': rate.rate3 if rate.rate3 else 0,
                        'games': rate.games
                    })
                for rate in PlayerSecondaryRates.query.filter_by(fromUpdate=up).filter_by(fromGameType=tp).filter_by(fromEdition=ed).filter_by(player=playerGl['sql'].id).order_by(
                        desc(PlayerSecondaryRates.rate1)).all():
                    sec = Secondary.query.filter_by(id=rate.secondary).first()
                    player['secondaryRates'].append({
                        'id': sec.id,
                        'name': sec.name,
                        'shortName': sec.shortName,
                        'winRate': rate.rate1 if rate.rate1 else 0,
                        'loseRate': rate.rate2 if rate.rate2 else 0,
                        'tieRate': rate.rate3 if rate.rate3 else 0,
                        'games': rate.games
                    })
                for rate in PlayerWinRatesPlayer.query.filter_by(fromUpdate=up).filter_by(fromGameType=tp).filter_by(fromEdition=ed).filter_by(player1=playerGl['sql'].id).order_by(
                        desc(PlayerWinRatesPlayer.rate1)).all():
                    oPl = Player.query.filter_by(id=rate.player2).first()
                    if oPl.allowSharing:
                        player['playerRates'].append({
                            'id': oPl.id,
                            'name': oPl.username,
                            'winRate': rate.rate1 if rate.rate1 else 0,
                            'loseRate': rate.rate2 if rate.rate2 else 0,
                            'tieRate': rate.rate3 if rate.rate3 else 0,
                            'games': rate.games
                        })
                playerGl['rates'] = player
            else:
                playerGl['name'] = "Anonymous"
    return playerGl


def getPlayerById(userId):
    return Player.query.filter_by(id=userId).first()


def setPlayerPermission(db, userId, form):
    try:
        lvl = form['permission']
        usr = Player.query.filter_by(id=userId).first()
        usr.permissions = int(lvl)
        db.session.commit()
    except:
        return False
    return True
