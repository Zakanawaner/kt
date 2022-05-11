from database import Game, Player, Tournament, Update, GameType
from sqlalchemy import desc


#########
# Games #
def getGames():
    games = {
        'updates': {}
    }
    for upd in Update.query.order_by(desc(Update.date)).all():
        games['updates'][str(upd.id)] = Game.query.filter(Game.date >= upd.date).filter(Game.date < upd.dateEnd).order_by(desc(Game.date)).all()
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
    game['type'] = GameType.query.filter_by(id=game['sql'].gameType).first()
    return game


def getGameTypes():
    return GameType.query.all()
