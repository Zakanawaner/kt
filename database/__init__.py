from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin


db = SQLAlchemy()


#############
# Global DB #
player_game_tie = db.Table(
    'player_game_tie',
    db.Column('game_id', db.Integer, db.ForeignKey('game.id'), primary_key=True, unique=False),
    db.Column('player_id', db.Integer, db.ForeignKey('player.id'), primary_key=True, unique=False)
)
player_game_won = db.Table(
    'player_game_won',
    db.Column('game_id', db.Integer, db.ForeignKey('game.id'), primary_key=True, unique=False),
    db.Column('player_id', db.Integer, db.ForeignKey('player.id'), primary_key=True, unique=False)
)
player_game_lost = db.Table(
    'player_game_lost',
    db.Column('game_id', db.Integer, db.ForeignKey('game.id'), primary_key=True, unique=False),
    db.Column('player_id', db.Integer, db.ForeignKey('player.id'), primary_key=True, unique=False)
)

faction_faction_winrate = db.Table(
    'faction_faction_winrate',
    db.Column('faction_id', db.Integer, db.ForeignKey('faction.id'), primary_key=True, unique=False),
    db.Column('win_id', db.Integer, db.ForeignKey('faction.id'), primary_key=True, unique=False)
)
faction_faction_loserate = db.Table(
    'faction_faction_loserate',
    db.Column('faction_id', db.Integer, db.ForeignKey('faction.id'), primary_key=True, unique=False),
    db.Column('lose_id', db.Integer, db.ForeignKey('faction.id'), primary_key=True, unique=False)
)
faction_faction_tierate = db.Table(
    'faction_faction_tierate',
    db.Column('faction_id', db.Integer, db.ForeignKey('faction.id'), primary_key=True, unique=False),
    db.Column('tie_id', db.Integer, db.ForeignKey('faction.id'), primary_key=True, unique=False)
)

game_faction_won = db.Table(
    'game_faction_won',
    db.Column('game_id', db.Integer, db.ForeignKey('game.id'), primary_key=True, unique=False),
    db.Column('faction_id', db.Integer, db.ForeignKey('faction.id'), primary_key=True, unique=False)
)
game_faction_lost = db.Table(
    'game_faction_lost',
    db.Column('game_id', db.Integer, db.ForeignKey('game.id'), primary_key=True, unique=False),
    db.Column('faction_id', db.Integer, db.ForeignKey('faction.id'), primary_key=True, unique=False)
)
game_faction_tied = db.Table(
    'game_faction_tied',
    db.Column('game_id', db.Integer, db.ForeignKey('game.id'), primary_key=True, unique=False),
    db.Column('faction_id', db.Integer, db.ForeignKey('faction.id'), primary_key=True, unique=False)
)

faction_game_init_1 = db.Table(
    'faction_game_init_1',
    db.Column('game_id', db.Integer, db.ForeignKey('game.id'), primary_key=True, unique=False),
    db.Column('faction_id', db.Integer, db.ForeignKey('faction.id'), primary_key=True, unique=False)
)
faction_game_init_2 = db.Table(
    'faction_game_init_2',
    db.Column('game_id', db.Integer, db.ForeignKey('game.id'), primary_key=True, unique=False),
    db.Column('faction_id', db.Integer, db.ForeignKey('faction.id'), primary_key=True, unique=False)
)
faction_game_init_3 = db.Table(
    'faction_game_init_3',
    db.Column('game_id', db.Integer, db.ForeignKey('game.id'), primary_key=True, unique=False),
    db.Column('faction_id', db.Integer, db.ForeignKey('faction.id'), primary_key=True, unique=False)
)
faction_game_init_4 = db.Table(
    'faction_game_init_4',
    db.Column('game_id', db.Integer, db.ForeignKey('game.id'), primary_key=True, unique=False),
    db.Column('faction_id', db.Integer, db.ForeignKey('faction.id'), primary_key=True, unique=False)
)
faction_game_init_5 = db.Table(
    'faction_game_init_5',
    db.Column('game_id', db.Integer, db.ForeignKey('game.id'), primary_key=True, unique=False),
    db.Column('faction_id', db.Integer, db.ForeignKey('faction.id'), primary_key=True, unique=False)
)
faction_game_roloff = db.Table(
    'faction_game_roloff',
    db.Column('game_id', db.Integer, db.ForeignKey('game.id'), primary_key=True, unique=False),
    db.Column('faction_id', db.Integer, db.ForeignKey('faction.id'), primary_key=True, unique=False)
)
player_rank = db.Table(
    'player_rank',
    db.Column('rank_id', db.Integer, db.ForeignKey('rank.id'), primary_key=True, unique=False),
    db.Column('player_id', db.Integer, db.ForeignKey('player.id'), primary_key=True, unique=False)
)
player_faction = db.Table(
    'player_faction',
    db.Column('faction_id', db.Integer, db.ForeignKey('faction.id'), primary_key=True, unique=False),
    db.Column('player_id', db.Integer, db.ForeignKey('player.id'), primary_key=True, unique=False)
)
game_faction_winner = db.Table(
    'game_faction_winner',
    db.Column('faction_id', db.Integer, db.ForeignKey('faction.id'), primary_key=True, unique=False),
    db.Column('game_id', db.Integer, db.ForeignKey('game.id'), primary_key=True, unique=False)
)
game_faction_loser = db.Table(
    'game_faction_loser',
    db.Column('faction_id', db.Integer, db.ForeignKey('faction.id'), primary_key=True, unique=False),
    db.Column('game_id', db.Integer, db.ForeignKey('game.id'), primary_key=True, unique=False)
)
game_mission = db.Table(
    'game_mission',
    db.Column('mission_id', db.Integer, db.ForeignKey('mission.id'), primary_key=True, unique=False),
    db.Column('game_id', db.Integer, db.ForeignKey('game.id'), primary_key=True, unique=False)
)
game_tournament = db.Table(
    'game_tournament',
    db.Column('tournament_id', db.Integer, db.ForeignKey('tournament.id'), primary_key=True, unique=False),
    db.Column('game_id', db.Integer, db.ForeignKey('game.id'), primary_key=True, unique=False)
)
game_gametype = db.Table(
    'game_gametype',
    db.Column('gametype_id', db.Integer, db.ForeignKey('gametype.id'), primary_key=True, unique=False),
    db.Column('game_id', db.Integer, db.ForeignKey('game.id'), primary_key=True, unique=False)
)
game_secondary_1 = db.Table(
    'game_secondary_1',
    db.Column('secondary_id', db.Integer, db.ForeignKey('secondary.id'), primary_key=True, unique=False),
    db.Column('game_id', db.Integer, db.ForeignKey('game.id'), primary_key=True, unique=False)
)
game_secondary_2 = db.Table(
    'game_secondary_2',
    db.Column('secondary_id', db.Integer, db.ForeignKey('secondary.id'), primary_key=True, unique=False),
    db.Column('game_id', db.Integer, db.ForeignKey('game.id'), primary_key=True, unique=False)
)
game_secondary_3 = db.Table(
    'game_secondary_3',
    db.Column('secondary_id', db.Integer, db.ForeignKey('secondary.id'), primary_key=True, unique=False),
    db.Column('game_id', db.Integer, db.ForeignKey('game.id'), primary_key=True, unique=False)
)
game_secondary_4 = db.Table(
    'game_secondary_4',
    db.Column('secondary_id', db.Integer, db.ForeignKey('secondary.id'), primary_key=True, unique=False),
    db.Column('game_id', db.Integer, db.ForeignKey('game.id'), primary_key=True, unique=False)
)
game_secondary_5 = db.Table(
    'game_secondary_5',
    db.Column('secondary_id', db.Integer, db.ForeignKey('secondary.id'), primary_key=True, unique=False),
    db.Column('game_id', db.Integer, db.ForeignKey('game.id'), primary_key=True, unique=False)
)
game_secondary_6 = db.Table(
    'game_secondary_6',
    db.Column('secondary_id', db.Integer, db.ForeignKey('secondary.id'), primary_key=True, unique=False),
    db.Column('game_id', db.Integer, db.ForeignKey('game.id'), primary_key=True, unique=False)
)
game_secondary_7 = db.Table(
    'game_secondary_7',
    db.Column('secondary_id', db.Integer, db.ForeignKey('secondary.id'), primary_key=True, unique=False),
    db.Column('game_id', db.Integer, db.ForeignKey('game.id'), primary_key=True, unique=False)
)
game_secondary_8 = db.Table(
    'game_secondary_8',
    db.Column('secondary_id', db.Integer, db.ForeignKey('secondary.id'), primary_key=True, unique=False),
    db.Column('game_id', db.Integer, db.ForeignKey('game.id'), primary_key=True, unique=False)
)
update_faction = db.Table(
    'update_faction',
    db.Column('update_id', db.Integer, db.ForeignKey('update.id'), primary_key=True, unique=False),
    db.Column('faction_id', db.Integer, db.ForeignKey('faction.id'), primary_key=True, unique=False)
)
player_team = db.Table(
    'player_team',
    db.Column('player_id', db.Integer, db.ForeignKey('player.id'), primary_key=True, unique=False),
    db.Column('team_id', db.Integer, db.ForeignKey('team.id'), primary_key=True, unique=False)
)
player_tournament = db.Table(
    'player_tournament',
    db.Column('player_id', db.Integer, db.ForeignKey('player.id'), primary_key=True, unique=False),
    db.Column('tournament_id', db.Integer, db.ForeignKey('tournament.id'), primary_key=True, unique=False)
)
team_tournament = db.Table(
    'team_tournament',
    db.Column('team_id', db.Integer, db.ForeignKey('team.id'), primary_key=True, unique=False),
    db.Column('tournament_id', db.Integer, db.ForeignKey('tournament.id'), primary_key=True, unique=False)
)
game_edition = db.Table(
    'game_edition',
    db.Column('game_id', db.Integer, db.ForeignKey('game.id'), primary_key=True, unique=False),
    db.Column('edition_id', db.Integer, db.ForeignKey('edition.id'), primary_key=True, unique=False)
)


class Game(db.Model):
    __tablename__ = 'game'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    tournament = db.Column(db.Integer, db.ForeignKey('tournament.id'))
    gameType = db.Column(db.Integer, db.ForeignKey('gametype.id'))
    edition = db.Column(db.Integer, db.ForeignKey('edition.id'))
    update = db.Column(db.Integer, db.ForeignKey('update.id'))
    timestamp = db.Column(db.Integer)
    mission = db.relationship("Mission", secondary=game_mission)
    initFirst = db.relationship("Faction", secondary=faction_game_init_1)
    initSecond = db.relationship("Faction", secondary=faction_game_init_2)
    initThird = db.relationship("Faction", secondary=faction_game_init_3)
    initFourth = db.relationship("Faction", secondary=faction_game_init_4)
    initFifth = db.relationship("Faction", secondary=faction_game_init_5)
    winner = db.Column(db.String(100))
    winnerId = db.Column(db.String(100))
    winScouting = db.Column(db.String(20))
    winFaction = db.relationship("Faction", secondary=game_faction_winner)
    winOperatives = db.Column(db.String(60))
    winOpKilled = db.Column(db.String(60))
    winTotal = db.Column(db.Integer)
    winPrimary = db.Column(db.Integer)
    winPrimaryFirst = db.Column(db.Integer)
    winPrimarySecond = db.Column(db.Integer)
    winPrimaryThird = db.Column(db.Integer)
    winPrimaryFourth = db.Column(db.Integer)
    winPrimaryFifth = db.Column(db.Integer)
    winSecondary = db.Column(db.Integer)
    winSecondaryFirst = db.relationship("Secondary", secondary=game_secondary_1)
    winSecondaryFirstScore = db.Column(db.Integer)
    winSecondaryFirstScoreTurn1 = db.Column(db.Integer)
    winSecondaryFirstScoreTurn2 = db.Column(db.Integer)
    winSecondaryFirstScoreTurn3 = db.Column(db.Integer)
    winSecondaryFirstScoreTurn4 = db.Column(db.Integer)
    winSecondarySecond = db.relationship("Secondary", secondary=game_secondary_2)
    winSecondarySecondScore = db.Column(db.Integer)
    winSecondarySecondScoreTurn1 = db.Column(db.Integer)
    winSecondarySecondScoreTurn2 = db.Column(db.Integer)
    winSecondarySecondScoreTurn3 = db.Column(db.Integer)
    winSecondarySecondScoreTurn4 = db.Column(db.Integer)
    winSecondaryThird = db.relationship("Secondary", secondary=game_secondary_3)
    winSecondaryThirdScore = db.Column(db.Integer)
    winSecondaryThirdScoreTurn1 = db.Column(db.Integer)
    winSecondaryThirdScoreTurn2 = db.Column(db.Integer)
    winSecondaryThirdScoreTurn3 = db.Column(db.Integer)
    winSecondaryThirdScoreTurn4 = db.Column(db.Integer)
    winSecondaryFourth = db.relationship("Secondary", secondary=game_secondary_4)
    winSecondaryFourthScore = db.Column(db.Integer)
    winSecondaryFourthScoreTurn1 = db.Column(db.Integer)
    winSecondaryFourthScoreTurn2 = db.Column(db.Integer)
    winSecondaryFourthScoreTurn3 = db.Column(db.Integer)
    winSecondaryFourthScoreTurn4 = db.Column(db.Integer)
    loser = db.Column(db.String(100))
    loserId = db.Column(db.String(100))
    losScouting = db.Column(db.String(20))
    losFaction = db.relationship("Faction", secondary=game_faction_loser)
    losOperatives = db.Column(db.String(60))
    losOpKilled = db.Column(db.String(60))
    losTotal = db.Column(db.Integer)
    losPrimary = db.Column(db.Integer)
    losPrimaryFirst = db.Column(db.Integer)
    losPrimarySecond = db.Column(db.Integer)
    losPrimaryThird = db.Column(db.Integer)
    losPrimaryFourth = db.Column(db.Integer)
    losPrimaryFifth = db.Column(db.Integer)
    losSecondary = db.Column(db.Integer)
    losSecondaryFirst = db.relationship("Secondary", secondary=game_secondary_5)
    losSecondaryFirstScore = db.Column(db.Integer)
    losSecondaryFirstScoreTurn1 = db.Column(db.Integer)
    losSecondaryFirstScoreTurn2 = db.Column(db.Integer)
    losSecondaryFirstScoreTurn3 = db.Column(db.Integer)
    losSecondaryFirstScoreTurn4 = db.Column(db.Integer)
    losSecondarySecond = db.relationship("Secondary", secondary=game_secondary_6)
    losSecondarySecondScore = db.Column(db.Integer)
    losSecondarySecondScoreTurn1 = db.Column(db.Integer)
    losSecondarySecondScoreTurn2 = db.Column(db.Integer)
    losSecondarySecondScoreTurn3 = db.Column(db.Integer)
    losSecondarySecondScoreTurn4 = db.Column(db.Integer)
    losSecondaryThird = db.relationship("Secondary", secondary=game_secondary_7)
    losSecondaryThirdScore = db.Column(db.Integer)
    losSecondaryThirdScoreTurn1 = db.Column(db.Integer)
    losSecondaryThirdScoreTurn2 = db.Column(db.Integer)
    losSecondaryThirdScoreTurn3 = db.Column(db.Integer)
    losSecondaryThirdScoreTurn4 = db.Column(db.Integer)
    losSecondaryFourth = db.relationship("Secondary", secondary=game_secondary_8)
    losSecondaryFourthScore = db.Column(db.Integer)
    losSecondaryFourthScoreTurn1 = db.Column(db.Integer)
    losSecondaryFourthScoreTurn2 = db.Column(db.Integer)
    losSecondaryFourthScoreTurn3 = db.Column(db.Integer)
    losSecondaryFourthScoreTurn4 = db.Column(db.Integer)
    rollOffWinner = db.relationship("Faction", secondary=faction_game_roloff)
    rollOffSelection = db.Column(db.String(20))
    tie = db.Column(db.Boolean)


class Mission(db.Model):
    __tablename__ = 'mission'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    shortName = db.Column(db.String(50))
    code = db.Column(db.Float)
    avgScore = db.Column(db.Float)
    avgScoreFirst = db.Column(db.Float)
    avgScoreSecond = db.Column(db.Float)
    avgScoreThird = db.Column(db.Float)
    avgScoreFourth = db.Column(db.Float)


class Secondary(db.Model):
    __tablename__ = 'secondary'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    shortName = db.Column(db.String(100))
    avgScore = db.Column(db.Float)
    avgScoreFirst = db.Column(db.Float)
    avgScoreSecond = db.Column(db.Float)
    avgScoreThird = db.Column(db.Float)
    avgScoreFourth = db.Column(db.Float)
    totalGames = db.Column(db.Integer)


class Faction(db.Model):
    __tablename__ = 'faction'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    shortName = db.Column(db.String(100))
    gamesWon = db.relationship("Game", secondary=game_faction_won)
    gamesLost = db.relationship("Game", secondary=game_faction_lost)
    gamesTied = db.relationship("Game", secondary=game_faction_tied)
    winnerRates = db.relationship("Faction", secondary=faction_faction_winrate,
                                  primaryjoin=id == faction_faction_winrate.c.faction_id,
                                  secondaryjoin=id == faction_faction_winrate.c.win_id)
    loserRates = db.relationship("Faction", secondary=faction_faction_loserate,
                                 primaryjoin=id == faction_faction_loserate.c.faction_id,
                                 secondaryjoin=id == faction_faction_loserate.c.lose_id)
    tieRates = db.relationship("Faction", secondary=faction_faction_tierate,
                               primaryjoin=id == faction_faction_tierate.c.faction_id,
                               secondaryjoin=id == faction_faction_tierate.c.tie_id)
    updates = db.relationship("Update", secondary=update_faction)


class WinRates(db.Model):
    __tablename__ = 'winrates'
    id = db.Column(db.Integer, primary_key=True)
    fromUpdate = db.Column(db.Integer, db.ForeignKey('update.id'))
    fromGameType = db.Column(db.Integer, db.ForeignKey('gametype.id'))
    fromEdition = db.Column(db.Integer, db.ForeignKey('edition.id'))
    faction1 = db.Column(db.Integer, db.ForeignKey('faction.id'))
    faction2 = db.Column(db.Integer, db.ForeignKey('faction.id'))
    rate1 = db.Column(db.Float)
    rate2 = db.Column(db.Float)
    rate3 = db.Column(db.Float)
    games = db.Column(db.Integer)


class MissionRates(db.Model):
    __tablename__ = 'missionrates'
    id = db.Column(db.Integer, primary_key=True)
    fromUpdate = db.Column(db.Integer, db.ForeignKey('update.id'))
    fromGameType = db.Column(db.Integer, db.ForeignKey('gametype.id'))
    fromEdition = db.Column(db.Integer, db.ForeignKey('edition.id'))
    faction = db.Column(db.Integer, db.ForeignKey('faction.id'))
    mission = db.Column(db.Integer, db.ForeignKey('mission.id'))
    rate1 = db.Column(db.Float)
    rate2 = db.Column(db.Float)
    rate3 = db.Column(db.Float)
    games = db.Column(db.Integer)


class SecondaryRates(db.Model):
    __tablename__ = 'secondaryrates'
    id = db.Column(db.Integer, primary_key=True)
    fromUpdate = db.Column(db.Integer, db.ForeignKey('update.id'))
    fromGameType = db.Column(db.Integer, db.ForeignKey('gametype.id'))
    fromEdition = db.Column(db.Integer, db.ForeignKey('edition.id'))
    faction = db.Column(db.Integer, db.ForeignKey('faction.id'))
    secondary = db.Column(db.Integer, db.ForeignKey('secondary.id'))
    rate1 = db.Column(db.Float)
    rate2 = db.Column(db.Float)
    rate3 = db.Column(db.Float)
    games = db.Column(db.Integer)


class PlayerWinRatesPlayer(db.Model):
    __tablename__ = 'playerwinratesplayer'
    id = db.Column(db.Integer, primary_key=True)
    fromUpdate = db.Column(db.Integer, db.ForeignKey('update.id'))
    fromGameType = db.Column(db.Integer, db.ForeignKey('gametype.id'))
    fromEdition = db.Column(db.Integer, db.ForeignKey('edition.id'))
    player1 = db.Column(db.Integer, db.ForeignKey('player.id'))
    player2 = db.Column(db.Integer, db.ForeignKey('player.id'))
    rate1 = db.Column(db.Float)
    rate2 = db.Column(db.Float)
    rate3 = db.Column(db.Float)
    games = db.Column(db.Integer)


class PlayerWinRates(db.Model):
    __tablename__ = 'playerwinrates'
    id = db.Column(db.Integer, primary_key=True)
    fromUpdate = db.Column(db.Integer, db.ForeignKey('update.id'))
    fromGameType = db.Column(db.Integer, db.ForeignKey('gametype.id'))
    fromEdition = db.Column(db.Integer, db.ForeignKey('edition.id'))
    player = db.Column(db.Integer, db.ForeignKey('player.id'))
    faction = db.Column(db.Integer, db.ForeignKey('faction.id'))
    rate1 = db.Column(db.Float)
    rate2 = db.Column(db.Float)
    rate3 = db.Column(db.Float)
    games = db.Column(db.Integer)


class PlayerWinRatesAgainst(db.Model):
    __tablename__ = 'playerwinratesagainst'
    id = db.Column(db.Integer, primary_key=True)
    fromUpdate = db.Column(db.Integer, db.ForeignKey('update.id'))
    fromGameType = db.Column(db.Integer, db.ForeignKey('gametype.id'))
    fromEdition = db.Column(db.Integer, db.ForeignKey('edition.id'))
    player = db.Column(db.Integer, db.ForeignKey('player.id'))
    faction = db.Column(db.Integer, db.ForeignKey('faction.id'))
    rate1 = db.Column(db.Float)
    rate2 = db.Column(db.Float)
    rate3 = db.Column(db.Float)
    games = db.Column(db.Integer)


class PlayerMissionRates(db.Model):
    __tablename__ = 'playermissionrates'
    id = db.Column(db.Integer, primary_key=True)
    fromUpdate = db.Column(db.Integer, db.ForeignKey('update.id'))
    fromGameType = db.Column(db.Integer, db.ForeignKey('gametype.id'))
    fromEdition = db.Column(db.Integer, db.ForeignKey('edition.id'))
    player = db.Column(db.Integer, db.ForeignKey('player.id'))
    mission = db.Column(db.Integer, db.ForeignKey('mission.id'))
    rate1 = db.Column(db.Float)
    rate2 = db.Column(db.Float)
    rate3 = db.Column(db.Float)
    games = db.Column(db.Integer)


class PlayerSecondaryRates(db.Model):
    __tablename__ = 'playersecondaryrates'
    id = db.Column(db.Integer, primary_key=True)
    fromUpdate = db.Column(db.Integer, db.ForeignKey('update.id'))
    fromGameType = db.Column(db.Integer, db.ForeignKey('gametype.id'))
    fromEdition = db.Column(db.Integer, db.ForeignKey('edition.id'))
    player = db.Column(db.Integer, db.ForeignKey('player.id'))
    secondary = db.Column(db.Integer, db.ForeignKey('secondary.id'))
    rate1 = db.Column(db.Float)
    rate2 = db.Column(db.Float)
    rate3 = db.Column(db.Float)
    games = db.Column(db.Integer)


class Rank(db.Model):
    __tablename__ = 'rank'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    shortName = db.Column(db.String(100))
    score = db.Column(db.Integer)


class Tournament(db.Model):
    __tablename__ = 'tournament'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    shortName = db.Column(db.String(100))
    dateInit = db.Column(db.DateTime)
    dateEnd = db.Column(db.DateTime)
    teamFormat = db.Column(db.Boolean)
    players = db.relationship("Player", secondary=player_tournament)
    teams = db.relationship("Team", secondary=team_tournament)
    games = db.relationship("Game", secondary=game_tournament)


class GameType(db.Model):
    __tablename__ = 'gametype'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    shortName = db.Column(db.String(100))
    games = db.relationship("Game", secondary=game_gametype)


class Player(db.Model, UserMixin):
    __tablename__ = 'player'
    id = db.Column(db.Integer, primary_key=True)
    publicId = db.Column(db.Integer)
    username = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(200))
    email = db.Column(db.String(200))
    subscribed = db.Column(db.Boolean)
    shortName = db.Column(db.String(30))
    permissions = db.Column(db.Integer)
    steamLink = db.Column(db.Boolean)
    steamId = db.Column(db.String(30))
    allowSharing = db.Column(db.Boolean)
    rank = db.relationship("Rank", secondary=player_rank)
    score = db.Column(db.Integer)
    gamesWon = db.relationship("Game", secondary=player_game_won)
    gamesLost = db.relationship("Game", secondary=player_game_lost)
    gamesTied = db.relationship("Game", secondary=player_game_tie)
    wins = db.Column(db.Integer)
    ties = db.Column(db.Integer)
    loses = db.Column(db.Integer)


class Update(db.Model):
    __tablename__ = 'update'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    date = db.Column(db.DateTime)
    dateEnd = db.Column(db.DateTime)
    factionAffected = db.Column(db.Integer, db.ForeignKey('faction.id'))
    description = db.Column(db.String(200))


class Edition(db.Model):
    __tablename__ = 'edition'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    shortName = db.Column(db.String(50))
    date = db.Column(db.DateTime)
    description = db.Column(db.String(200))
    games = db.relationship("Game", secondary=game_edition)


class Operative(db.Model):
    __tablename__ = 'operative'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    melee = db.Column(db.String(200))
    ranged = db.Column(db.String(200))
    faction = db.Column(db.Integer, db.ForeignKey('faction.id'))
    desc = db.Column(db.String(1000))


class Team(db.Model):
    __tablename__ = 'team'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    shortname = db.Column(db.String(50))
    desc = db.Column(db.String(300))
    score = db.Column(db.Integer)
    leader = db.Column(db.Integer, db.ForeignKey('player.id'))
    players = db.relationship("Player", secondary=player_team)


# ADDED after deploy
class TournamentOrganizers(db.Model):
    __tablename__ = 'tournamentorganozers'
    id = db.Column(db.Integer, primary_key=True)
    tournament = db.Column(db.Integer, db.ForeignKey('tournament.id'))
    organizer = db.Column(db.Integer, db.ForeignKey('player.id'))
