from sqlalchemy import desc
from database import (
    Game, Player, Mission, Rank, Secondary, Faction,
    PlayerMissionRates,
    PlayerWinRates, PlayerWinRatesPlayer, PlayerSecondaryRates,
    PlayerWinRatesAgainst, Update
)


###########
# Players #
def updatePlayers(db):
    for player in Player.query.all():
        updatePlayer(db, player.id)


def updatePlayer(db, pl):
    playerGl = {
        'sql': Player.query.filter_by(id=pl).first(),
        'updates': [],
    }
    playerGl['sql'].gamesWon = []
    playerGl['sql'].gamesLost = []
    playerGl['sql'].gamesTied = []
    playerGl['sql'].wins = 0
    playerGl['sql'].loses = 0
    playerGl['sql'].ties = 0
    if playerGl['sql'].steamLink:
        for update in Update.query.all():
            player = {
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
            for game in Game.query.filter(Game.date >= update.date).filter(Game.date <=  update.dateEnd).filter_by(winnerId=playerGl['sql'].steamId).all():
                otherPl = Player.query.filter_by(steamId=game.loserId).first()
                if game.tie:
                    playerGl['sql'].gamesTied.append(game)
                    playerGl['sql'].ties += 1
                    player['ties'] += 1
                    if otherPl:
                        if otherPl.username not in player['tiePlayers'].keys():
                            player['tiePlayers'][otherPl.username] = 1
                        else:
                            player['tiePlayers'][otherPl.username] += 1
                    if game.winFaction[0].name not in player['tieFactions'].keys():
                        player['tieFactions'][game.winFaction[0].name] = 1
                    else:
                        player['tieFactions'][game.winFaction[0].name] += 1
                    if game.losFaction[0].name not in player['tieFactionsAgainst'].keys():
                        player['tieFactionsAgainst'][game.losFaction[0].name] = 1
                    else:
                        player['tieFactionsAgainst'][game.losFaction[0].name] += 1
                    if game.mission[0].name not in player['tieMissions'].keys():
                        player['tieMissions'][game.mission[0].name] = 1
                    else:
                        player['tieMissions'][game.mission[0].name] += 1
                    if game.winSecondaryFirst[0].name not in player['tieSecondaries'].keys():
                        player['tieSecondaries'][game.winSecondaryFirst[0].name] = 1
                    else:
                        player['tieSecondaries'][game.winSecondaryFirst[0].name] += 1
                    if game.winSecondarySecond[0].name not in player['tieSecondaries'].keys():
                        player['tieSecondaries'][game.winSecondarySecond[0].name] = 1
                    else:
                        player['tieSecondaries'][game.winSecondarySecond[0].name] += 1
                    if game.winSecondaryThird[0].name not in player['tieSecondaries'].keys():
                        player['tieSecondaries'][game.winSecondaryThird[0].name] = 1
                    else:
                        player['tieSecondaries'][game.winSecondaryThird[0].name] += 1
                else:
                    playerGl['sql'].gamesWon.append(game)
                    playerGl['sql'].wins += 1
                    player['wins'] += 1
                    if otherPl:
                        if otherPl.username not in player['winnerPlayers'].keys():
                            player['winnerPlayers'][otherPl.username] = 1
                        else:
                            player['winnerPlayers'][otherPl.username] += 1
                    if game.winFaction[0].name not in player['winnerFactions'].keys():
                        player['winnerFactions'][game.winFaction[0].name] = 1
                    else:
                        player['winnerFactions'][game.winFaction[0].name] += 1
                    if game.losFaction[0].name not in player['winnerFactionsAgainst'].keys():
                        player['winnerFactionsAgainst'][game.losFaction[0].name] = 1
                    else:
                        player['winnerFactionsAgainst'][game.losFaction[0].name] += 1
                    if game.mission[0].name not in player['winnerMissions'].keys():
                        player['winnerMissions'][game.mission[0].name] = 1
                    else:
                        player['winnerMissions'][game.mission[0].name] += 1
                    if game.winSecondaryFirst[0].name not in player['winnerSecondaries'].keys():
                        player['winnerSecondaries'][game.winSecondaryFirst[0].name] = 1
                    else:
                        player['winnerSecondaries'][game.winSecondaryFirst[0].name] += 1
                    if game.winSecondarySecond[0].name not in player['winnerSecondaries'].keys():
                        player['winnerSecondaries'][game.winSecondarySecond[0].name] = 1
                    else:
                        player['winnerSecondaries'][game.winSecondarySecond[0].name] += 1
                    if game.winSecondaryThird[0].name not in player['winnerSecondaries'].keys():
                        player['winnerSecondaries'][game.winSecondaryThird[0].name] = 1
                    else:
                        player['winnerSecondaries'][game.winSecondaryThird[0].name] += 1
                playerGl['sql'].score += game.winTotal
            for game in Game.query.filter(Game.date >= update.date).filter(Game.date <=  update.dateEnd).filter_by(loserId=playerGl['sql'].steamId).all():
                otherPl = Player.query.filter_by(steamId=game.winnerId).first()
                if game.tie:
                    playerGl['sql'].gamesTied.append(game)
                    playerGl['sql'].ties += 1
                    player['ties'] += 1
                    if otherPl:
                        if otherPl.username not in player['tiePlayers'].keys():
                            player['tiePlayers'][otherPl.username] = 1
                        else:
                            player['tiePlayers'][otherPl.username] += 1
                    if game.winFaction[0].name not in player['tieFactions'].keys():
                        player['tieFactions'][game.winFaction[0].name] = 1
                    else:
                        player['tieFactions'][game.winFaction[0].name] += 1
                    if game.winFaction[0].name not in player['tieFactionsAgainst'].keys():
                        player['tieFactionsAgainst'][game.winFaction[0].name] = 1
                    else:
                        player['tieFactionsAgainst'][game.winFaction[0].name] += 1
                    if game.mission[0].name not in player['tieMissions'].keys():
                        player['tieMissions'][game.mission[0].name] = 1
                    else:
                        player['tieMissions'][game.mission[0].name] += 1
                    if game.losSecondaryFirst[0].name not in player['tieSecondaries'].keys():
                        player['tieSecondaries'][game.losSecondaryFirst[0].name] = 1
                    else:
                        player['tieSecondaries'][game.losSecondaryFirst[0].name] += 1
                    if game.losSecondarySecond[0].name not in player['tieSecondaries'].keys():
                        player['tieSecondaries'][game.losSecondarySecond[0].name] = 1
                    else:
                        player['tieSecondaries'][game.losSecondarySecond[0].name] += 1
                    if game.losSecondaryThird[0].name not in player['tieSecondaries'].keys():
                        player['tieSecondaries'][game.losSecondaryThird[0].name] = 1
                    else:
                        player['tieSecondaries'][game.losSecondaryThird[0].name] += 1
                else:
                    playerGl['sql'].gamesLost.append(game)
                    playerGl['sql'].loses += 1
                    player['loses'] += 1
                    if otherPl:
                        if otherPl.username not in player['loserPlayers'].keys():
                            player['loserPlayers'][otherPl.username] = 1
                        else:
                            player['loserPlayers'][otherPl.username] += 1
                    if game.losFaction[0].name not in player['loserFactions'].keys():
                        player['loserFactions'][game.losFaction[0].name] = 1
                    else:
                        player['loserFactions'][game.losFaction[0].name] += 1
                    if game.winFaction[0].name not in player['loserFactionsAgainst'].keys():
                        player['loserFactionsAgainst'][game.winFaction[0].name] = 1
                    else:
                        player['loserFactionsAgainst'][game.winFaction[0].name] += 1
                    if game.mission[0].name not in player['loserMissions'].keys():
                        player['loserMissions'][game.mission[0].name] = 1
                    else:
                        player['loserMissions'][game.mission[0].name] += 1
                    if game.losSecondaryFirst[0].name not in player['loserSecondaries'].keys():
                        player['loserSecondaries'][game.losSecondaryFirst[0].name] = 1
                    else:
                        player['loserSecondaries'][game.losSecondaryFirst[0].name] += 1
                    if game.losSecondarySecond[0].name not in player['loserSecondaries'].keys():
                        player['loserSecondaries'][game.losSecondarySecond[0].name] = 1
                    else:
                        player['loserSecondaries'][game.losSecondarySecond[0].name] += 1
                    if game.losSecondaryThird[0].name not in player['loserSecondaries'].keys():
                        player['loserSecondaries'][game.losSecondaryThird[0].name] = 1
                    else:
                        player['loserSecondaries'][game.losSecondaryThird[0].name] += 1
                playerGl['sql'].score += game.losTotal
            player['totalGames'] = player['wins'] + player['loses'] + player['ties']
            player['winRate'] = float(
                "{:.2f}".format(player['wins'] * 100 / player['totalGames'] if player['totalGames'] > 0 else 0))
            playerGl['sql'].rank = [Rank.query.filter(Rank.score <= playerGl['sql'].score).order_by(desc(Rank.score)).first()]
            for otherPl in player['winnerPlayers'].keys():
                oPl = Player.query.filter_by(username=otherPl).first()
                tot = player['winnerPlayers'][otherPl] + (
                    player['loserPlayers'][otherPl] if otherPl in player['loserPlayers'].keys() else 0) + (
                          player['tiePlayers'][otherPl] if otherPl in player['tiePlayers'].keys() else 0)
                rate = PlayerWinRatesPlayer.query.filter_by(fromUpdate=update.id).filter_by(player1=playerGl['sql'].id).filter_by(player2=oPl.id).first()
                if not rate:
                    rate = PlayerWinRatesPlayer(
                        player1=playerGl['sql'].id,
                        player2=oPl.id,
                        fromUpdate=update.id,
                    )
                rate.rate1 = float("{:.2f}".format(player['winnerPlayers'][otherPl] * 100 / tot)) if tot > 0 else 0
                db.session.add(rate)
                db.session.commit()
            for otherPl in player['loserPlayers'].keys():
                oPl = Player.query.filter_by(username=otherPl).first()
                tot = player['loserPlayers'][otherPl] + (
                    player['winnerPlayers'][otherPl] if otherPl in player['winnerPlayers'].keys() else 0) + (
                          player['tiePlayers'][otherPl] if otherPl in player['tiePlayers'].keys() else 0)
                rate = PlayerWinRatesPlayer.query.filter_by(fromUpdate=update.id).filter_by(player1=playerGl['sql'].id).filter_by(player2=oPl.id).first()
                if not rate:
                    rate = PlayerWinRatesPlayer(
                        player1=playerGl['sql'].id,
                        player2=oPl.id,
                        fromUpdate=update.id
                    )
                rate.rate2 = float("{:.2f}".format(player['loserPlayers'][otherPl] * 100 / tot)) if tot > 0 else 0
                db.session.add(rate)
                db.session.commit()
            for otherPl in player['tiePlayers'].keys():
                oPl = Player.query.filter_by(username=otherPl).first()
                tot = player['tiePlayers'][otherPl] + (
                    player['winnerPlayers'][otherPl] if otherPl in player['winnerPlayers'].keys() else 0) + (
                          player['loserPlayers'][otherPl] if otherPl in player['loserPlayers'].keys() else 0)
                rate = PlayerWinRatesPlayer.query.filter_by(fromUpdate=update.id).filter_by(player1=playerGl['sql'].id).filter_by(player2=oPl.id).first()
                if not rate:
                    rate = PlayerWinRatesPlayer(
                        player1=playerGl['sql'].id,
                        player2=oPl.id,
                        fromUpdate=update.id
                    )
                rate.rate3 = float("{:.2f}".format(player['tiePlayers'][otherPl] * 100 / tot)) if tot > 0 else 0
                db.session.add(rate)
                db.session.commit()
            for faction in player['winnerFactions'].keys():
                fct = Faction.query.filter_by(name=faction).first()
                tot = player['winnerFactions'][faction] + (
                    player['loserFactions'][faction] if faction in player['loserFactions'].keys() else 0) + (
                          player['tieFactions'][faction] if faction in player['tieFactions'].keys() else 0)
                rate = PlayerWinRates.query.filter_by(fromUpdate=update.id).filter_by(player=playerGl['sql'].id).filter_by(faction=fct.id).first()
                if not rate:
                    rate = PlayerWinRates(
                        player=playerGl['sql'].id,
                        faction=fct.id,
                        fromUpdate=update.id
                    )
                rate.rate1 = float("{:.2f}".format(player['winnerFactions'][faction] * 100 / tot)) if tot > 0 else 0
                db.session.add(rate)
                db.session.commit()
            for faction in player['loserFactions'].keys():
                fct = Faction.query.filter_by(name=faction).first()
                tot = player['loserFactions'][faction] + (
                    player['winnerFactions'][faction] if faction in player['winnerFactions'].keys() else 0) + (
                          player['tieFactions'][faction] if faction in player['tieFactions'].keys() else 0)
                rate = PlayerWinRates.query.filter_by(fromUpdate=update.id).filter_by(player=playerGl['sql'].id).filter_by(faction=fct.id).first()
                if not rate:
                    rate = PlayerWinRates(
                        player=playerGl['sql'].id,
                        faction=fct.id,
                        fromUpdate=update.id
                    )
                rate.rate2 = float("{:.2f}".format(player['loserFactions'][faction] * 100 / tot)) if tot > 0 else 0
                db.session.add(rate)
                db.session.commit()
            for faction in player['tieFactions'].keys():
                fct = Faction.query.filter_by(name=faction).first()
                tot = player['tieFactions'][faction] + (
                    player['winnerFactions'][faction] if faction in player['winnerFactions'].keys() else 0) + (
                          player['loserFactions'][faction] if faction in player['loserFactions'].keys() else 0)
                rate = PlayerWinRates.query.filter_by(fromUpdate=update.id).filter_by(player=playerGl['sql'].id).filter_by(faction=fct.id).first()
                if not rate:
                    rate = PlayerWinRates(
                        player=playerGl['sql'].id,
                        faction=fct.id,
                        fromUpdate=update.id
                    )
                rate.rate3 = float("{:.2f}".format(player['tieFactions'][faction] * 100 / tot)) if tot > 0 else 0
                db.session.add(rate)
                db.session.commit()

            for faction in player['winnerFactionsAgainst'].keys():
                fct = Faction.query.filter_by(name=faction).first()
                tot = player['winnerFactionsAgainst'][faction] + (
                    player['loserFactionsAgainst'][faction] if faction in player['loserFactionsAgainst'].keys() else 0) + (
                          player['tieFactionsAgainst'][faction] if faction in player['tieFactionsAgainst'].keys() else 0)
                rate = PlayerWinRatesAgainst.query.filter_by(fromUpdate=update.id).filter_by(player=playerGl['sql'].id).filter_by(faction=fct.id).first()
                if not rate:
                    rate = PlayerWinRatesAgainst(
                        player=playerGl['sql'].id,
                        faction=fct.id,
                        fromUpdate=update.id
                    )
                rate.rate1 = float("{:.2f}".format(player['winnerFactionsAgainst'][faction] * 100 / tot)) if tot > 0 else 0
                db.session.add(rate)
                db.session.commit()
            for faction in player['loserFactionsAgainst'].keys():
                fct = Faction.query.filter_by(name=faction).first()
                tot = player['loserFactionsAgainst'][faction] + (
                    player['winnerFactionsAgainst'][faction] if faction in player[
                        'winnerFactionsAgainst'].keys() else 0) + (
                          player['tieFactionsAgainst'][faction] if faction in player['tieFactionsAgainst'].keys() else 0)
                rate = PlayerWinRatesAgainst.query.filter_by(fromUpdate=update.id).filter_by(player=playerGl['sql'].id).filter_by(faction=fct.id).first()
                if not rate:
                    rate = PlayerWinRatesAgainst(
                        player=playerGl['sql'].id,
                        faction=fct.id,
                        fromUpdate=update.id
                    )
                rate.rate2 = float("{:.2f}".format(player['loserFactionsAgainst'][faction] * 100 / tot)) if tot > 0 else 0
                db.session.add(rate)
                db.session.commit()
            for faction in player['tieFactionsAgainst'].keys():
                fct = Faction.query.filter_by(name=faction).first()
                tot = player['tieFactionsAgainst'][faction] + (
                    player['winnerFactionsAgainst'][faction] if faction in player[
                        'winnerFactionsAgainst'].keys() else 0) + (
                          player['loserFactionsAgainst'][faction] if faction in player[
                              'loserFactionsAgainst'].keys() else 0)
                rate = PlayerWinRatesAgainst.query.filter_by(fromUpdate=update.id).filter_by(player=playerGl['sql'].id).filter_by(faction=fct.id).first()
                if not rate:
                    rate = PlayerWinRatesAgainst(
                        player=playerGl['sql'].id,
                        faction=fct.id,
                        fromUpdate=update.id
                    )
                rate.rate3 = float("{:.2f}".format(player['tieFactionsAgainst'][faction] * 100 / tot)) if tot > 0 else 0
                db.session.add(rate)
                db.session.commit()

            for mission in player['winnerMissions'].keys():
                fct = Mission.query.filter_by(name=mission).first()
                tot = player['winnerMissions'][mission] + (
                    player['loserMissions'][mission] if mission in player['loserMissions'].keys() else 0) + (
                          player['tieMissions'][mission] if mission in player['tieMissions'].keys() else 0)
                rate = PlayerMissionRates.query.filter_by(fromUpdate=update.id).filter_by(player=playerGl['sql'].id).filter_by(mission=fct.id).first()
                if not rate:
                    rate = PlayerMissionRates(
                        player=playerGl['sql'].id,
                        mission=fct.id,
                        fromUpdate=update.id
                    )
                rate.rate1 = float("{:.2f}".format(player['winnerMissions'][mission] * 100 / tot)) if tot > 0 else 0
                db.session.add(rate)
                db.session.commit()
            for mission in player['loserMissions'].keys():
                fct = Mission.query.filter_by(name=mission).first()
                tot = player['loserMissions'][mission] + (
                    player['winnerMissions'][mission] if mission in player['winnerMissions'].keys() else 0) + (
                          player['tieMissions'][mission] if mission in player['tieMissions'].keys() else 0)
                rate = PlayerMissionRates.query.filter_by(fromUpdate=update.id).filter_by(player=playerGl['sql'].id).filter_by(mission=fct.id).first()
                if not rate:
                    rate = PlayerMissionRates(
                        player=playerGl['sql'].id,
                        mission=fct.id,
                        fromUpdate=update.id
                    )
                rate.rate2 = float("{:.2f}".format(player['loserMissions'][mission] * 100 / tot)) if tot > 0 else 0
                db.session.add(rate)
                db.session.commit()
            for mission in player['tieMissions'].keys():
                fct = Mission.query.filter_by(name=mission).first()
                tot = player['tieMissions'][mission] + (
                    player['winnerMissions'][mission] if mission in player['winnerMissions'].keys() else 0) + (
                          player['loserMissions'][mission] if mission in player['loserMissions'].keys() else 0)
                rate = PlayerMissionRates.query.filter_by(fromUpdate=update.id).filter_by(player=playerGl['sql'].id).filter_by(mission=fct.id).first()
                if not rate:
                    rate = PlayerMissionRates(
                        player=playerGl['sql'].id,
                        mission=fct.id,
                        fromUpdate=update.id
                    )
                rate.rate3 = float("{:.2f}".format(player['tieMissions'][mission] * 100 / tot)) if tot > 0 else 0
                db.session.add(rate)
                db.session.commit()
            for secondary in player['winnerSecondaries'].keys():
                fct = Secondary.query.filter_by(name=secondary).first()
                tot = player['winnerSecondaries'][secondary] + (
                    player['loserSecondaries'][secondary] if secondary in player['loserSecondaries'].keys() else 0) + (
                          player['tieSecondaries'][secondary] if secondary in player['tieSecondaries'].keys() else 0)
                rate = PlayerSecondaryRates.query.filter_by(fromUpdate=update.id).filter_by(player=playerGl['sql'].id).filter_by(secondary=fct.id).first()
                if not rate:
                    rate = PlayerSecondaryRates(
                        player=playerGl['sql'].id,
                        secondary=fct.id,
                        fromUpdate=update.id
                    )
                rate.rate1 = float("{:.2f}".format(player['winnerSecondaries'][secondary] * 100 / tot)) if tot > 0 else 0
                db.session.add(rate)
                db.session.commit()
            for secondary in player['loserSecondaries'].keys():
                fct = Secondary.query.filter_by(name=secondary).first()
                tot = player['loserSecondaries'][secondary] + (
                    player['winnerSecondaries'][secondary] if secondary in player['winnerSecondaries'].keys() else 0) + (
                          player['tieSecondaries'][secondary] if secondary in player['tieSecondaries'].keys() else 0)
                rate = PlayerSecondaryRates.query.filter_by(fromUpdate=update.id).filter_by(player=playerGl['sql'].id).filter_by(secondary=fct.id).first()
                if not rate:
                    rate = PlayerSecondaryRates(
                        player=playerGl['sql'].id,
                        secondary=fct.id,
                        fromUpdate=update.id
                    )
                rate.rate2 = float("{:.2f}".format(player['loserSecondaries'][secondary] * 100 / tot)) if tot > 0 else 0
                db.session.add(rate)
                db.session.commit()
            for secondary in player['tieSecondaries'].keys():
                fct = Secondary.query.filter_by(name=secondary).first()
                tot = player['tieSecondaries'][secondary] + (
                    player['winnerSecondaries'][secondary] if secondary in player['winnerSecondaries'].keys() else 0) + (
                          player['loserSecondaries'][secondary] if secondary in player['loserSecondaries'].keys() else 0)
                rate = PlayerSecondaryRates.query.filter_by(fromUpdate=update.id).filter_by(player=playerGl['sql'].id).filter_by(secondary=fct.id).first()
                if not rate:
                    rate = PlayerSecondaryRates(
                        player=playerGl['sql'].id,
                        secondary=fct.id,
                        fromUpdate=update.id
                    )
                rate.rate3 = float("{:.2f}".format(player['tieSecondaries'][secondary] * 100 / tot)) if tot > 0 else 0
                db.session.add(rate)
                db.session.commit()
            playerGl['updates'].append(player)
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
                    player = {
                        'factionRates': [], 'factionRatesAgainst': [],
                        'missionRates': [], 'secondaryRates': [],
                        'playerRates': [],
                    }
                    player['wins'] = len(Game.query.filter(Game.date >= update.date).filter(Game.date <= update.dateEnd).filter_by(winnerId=playerGl['sql'].steamId).filter_by(tie=False).all())
                    player['loses'] = len(Game.query.filter(Game.date >= update.date).filter(Game.date <= update.dateEnd).filter_by(loserId=playerGl['sql'].steamId).filter_by(tie=False).all())
                    player['ties'] = len(Game.query.filter(Game.date >= update.date).filter(Game.date <= update.dateEnd).filter_by(winnerId=playerGl['sql'].steamId).filter_by(tie=True).all()) + len(Game.query.filter(Game.date >= update.date).filter(Game.date <= update.dateEnd).filter_by(loserId=playerGl['sql'].steamId).filter_by(tie=True).all())
                    player['totalGames'] = player['wins'] + player['loses'] + player['ties']
                    player['winRate'] = float(
                        "{:.2f}".format(player['wins'] * 100 / player['totalGames'] if player['totalGames'] > 0 else 0))
                    for rate in PlayerWinRates.query.filter_by(fromUpdate=update.id).filter_by(player=playerGl['sql'].id).order_by(
                            desc(PlayerWinRates.rate1)).all():
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
                    for rate in PlayerWinRatesAgainst.query.filter_by(fromUpdate=update.id).filter_by(player=playerGl['sql'].id).order_by(
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
                    for rate in PlayerMissionRates.query.filter_by(fromUpdate=update.id).filter_by(player=playerGl['sql'].id).order_by(
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
                    for rate in PlayerSecondaryRates.query.filter_by(fromUpdate=update.id).filter_by(player=playerGl['sql'].id).order_by(
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
                    for rate in PlayerWinRatesPlayer.query.filter_by(fromUpdate=update.id).filter_by(player1=playerGl['sql'].id).order_by(
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
                    playerGl['updates'][str(update.id)] = player
                player = {
                    'factionRates': [], 'factionRatesAgainst': [],
                    'missionRates': [], 'secondaryRates': [],
                    'playerRates': [],
                }
                player['wins'] = len(
                    Game.query.filter_by(
                        winnerId=playerGl['sql'].steamId).filter_by(tie=False).all())
                player['loses'] = len(
                    Game.query.filter_by(
                        loserId=playerGl['sql'].steamId).filter_by(tie=False).all())
                player['ties'] = len(
                    Game.query.filter_by(
                        winnerId=playerGl['sql'].steamId).filter_by(tie=True).all()) + len(
                    Game.query.filter_by(
                        loserId=playerGl['sql'].steamId).filter_by(tie=True).all())
                player['totalGames'] = player['wins'] + player['loses'] + player['ties']
                player['winRate'] = float(
                    "{:.2f}".format(
                        player['wins'] * 100 / player['totalGames'] if player['totalGames'] > 0 else 0))
                for rate in PlayerWinRates.query.filter_by(
                        player=playerGl['sql'].id).order_by(
                        desc(PlayerWinRates.rate1)).all():
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
                for rate in PlayerWinRatesAgainst.query.filter_by(
                        player=playerGl['sql'].id).order_by(
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
                for rate in PlayerMissionRates.query.filter_by(
                        player=playerGl['sql'].id).order_by(
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
                for rate in PlayerSecondaryRates.query.filter_by(
                        player=playerGl['sql'].id).order_by(
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
                for rate in PlayerWinRatesPlayer.query.filter_by(
                        player1=playerGl['sql'].id).order_by(
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
                playerGl['updates'][str(0)] = player
            else:
                playerGl['name'] = "Anonymous"
    return playerGl


def getPlayerById(userId):
    return Player.query.filter_by(id=userId).first()
