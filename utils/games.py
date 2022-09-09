from database import Game, Player, Tournament, Update, GameType, Edition
from sqlalchemy import desc


#########
# Games #
def getGames(up, tp, ed):
    return Game.query.filter(Game.update == up if up > 1 else Game.update).filter(Game.gameType == tp if tp > 1 else Game.gameType).filter(Game.edition == ed if ed > 1 else Game.edition).order_by(desc(Game.date)).all()


def getGame(gm):
    game = {
        'sql': Game.query.filter_by(id=gm).first(),
    }
    game['winner'] = Player.query.filter_by(allowSharing=True).filter_by(steamId=game['sql'].winnerId).first()
    game['loser'] = Player.query.filter_by(allowSharing=True).filter_by(steamId=game['sql'].loserId).first()
    game['winner'] = game['winner'].username if game['winner'] else "Anonymous"
    game['loser'] = game['loser'].username if game['loser'] else "Anonymous"
    game['tournament'] = Tournament.query.filter_by(id=game['sql'].tournament).first()
    game['type'] = GameType.query.filter_by(id=game['sql'].gameType).first()
    return game


def getGameTypes():
    return GameType.query.all()


def getEditions():
    return Edition.query.all()
