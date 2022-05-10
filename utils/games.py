from database import Game, Player, Tournament


#########
# Games #
def getGames():
    games = Game.query.all()
    return games


def getGame(gm):
    game = {
        'sql': Game.query.filter_by(id=gm).first(),
    }
    game['winner'] = Player.query.filter_by(allowSharing=True).filter_by(steamId=game['sql'].winnerId).first()
    game['loser'] = Player.query.filter_by(allowSharing=True).filter_by(steamId=game['sql'].loserId).first()
    game['winner'] = game['winner'].username if game['winner'] else "Anonymous"
    game['loser'] = game['loser'].username if game['loser'] else "Anonymous"
    game['tournament'] = Tournament.query.filter_by(id=game['sql'].tournament).first()
    return game
