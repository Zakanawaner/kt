from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


player_game_winner = db.Table(
    'player_game_winner',
    db.Column('game_id', db.Integer, db.ForeignKey('game.id'), primary_key=True),
    db.Column('player_id', db.Integer, db.ForeignKey('player.id'), primary_key=True)
)
player_game_loser = db.Table(
    'player_game_loser',
    db.Column('game_id', db.Integer, db.ForeignKey('game.id'), primary_key=True),
    db.Column('player_id', db.Integer, db.ForeignKey('player.id'), primary_key=True)
)
player_game_init_1 = db.Table(
    'player_game_init_1',
    db.Column('game_id', db.Integer, db.ForeignKey('game.id'), primary_key=True),
    db.Column('player_id', db.Integer, db.ForeignKey('player.id'), primary_key=True)
)
player_game_init_2 = db.Table(
    'player_game_init_2',
    db.Column('game_id', db.Integer, db.ForeignKey('game.id'), primary_key=True),
    db.Column('player_id', db.Integer, db.ForeignKey('player.id'), primary_key=True)
)
player_game_init_3 = db.Table(
    'player_game_init_3',
    db.Column('game_id', db.Integer, db.ForeignKey('game.id'), primary_key=True),
    db.Column('player_id', db.Integer, db.ForeignKey('player.id'), primary_key=True)
)
player_game_init_4 = db.Table(
    'player_game_init_4',
    db.Column('game_id', db.Integer, db.ForeignKey('game.id'), primary_key=True),
    db.Column('player_id', db.Integer, db.ForeignKey('player.id'), primary_key=True)
)
player_game_init_5 = db.Table(
    'player_game_init_5',
    db.Column('game_id', db.Integer, db.ForeignKey('game.id'), primary_key=True),
    db.Column('player_id', db.Integer, db.ForeignKey('player.id'), primary_key=True)
)
player_game_roloff = db.Table(
    'player_game_roloff',
    db.Column('game_id', db.Integer, db.ForeignKey('game.id'), primary_key=True),
    db.Column('player_id', db.Integer, db.ForeignKey('player.id'), primary_key=True)
)
player_rank = db.Table(
    'player_rank',
    db.Column('rank_id', db.Integer, db.ForeignKey('rank.id'), primary_key=True),
    db.Column('player_id', db.Integer, db.ForeignKey('player.id'), primary_key=True)
)
player_faction = db.Table(
    'player_faction',
    db.Column('faction_id', db.Integer, db.ForeignKey('faction.id'), primary_key=True),
    db.Column('player_id', db.Integer, db.ForeignKey('player.id'), primary_key=True)
)
game_faction_winner = db.Table(
    'game_faction_winner',
    db.Column('faction_id', db.Integer, db.ForeignKey('faction.id'), primary_key=True),
    db.Column('game_id', db.Integer, db.ForeignKey('game.id'), primary_key=True)
)
game_faction_loser = db.Table(
    'game_faction_loser',
    db.Column('faction_id', db.Integer, db.ForeignKey('faction.id'), primary_key=True),
    db.Column('game_id', db.Integer, db.ForeignKey('game.id'), primary_key=True)
)
game_mission = db.Table(
    'game_mission',
    db.Column('mission_id', db.Integer, db.ForeignKey('mission.id'), primary_key=True),
    db.Column('game_id', db.Integer, db.ForeignKey('game.id'), primary_key=True)
)
game_tournament = db.Table(
    'game_tournament',
    db.Column('tournament_id', db.Integer, db.ForeignKey('tournament.id'), primary_key=True),
    db.Column('game_id', db.Integer, db.ForeignKey('game.id'), primary_key=True)
)
game_secondary_1 = db.Table(
    'game_secondary_1',
    db.Column('secondary_id', db.Integer, db.ForeignKey('secondary.id'), primary_key=True),
    db.Column('game_id', db.Integer, db.ForeignKey('game.id'), primary_key=True)
)
game_secondary_2 = db.Table(
    'game_secondary_2',
    db.Column('secondary_id', db.Integer, db.ForeignKey('secondary.id'), primary_key=True),
    db.Column('game_id', db.Integer, db.ForeignKey('game.id'), primary_key=True)
)
game_secondary_3 = db.Table(
    'game_secondary_3',
    db.Column('secondary_id', db.Integer, db.ForeignKey('secondary.id'), primary_key=True),
    db.Column('game_id', db.Integer, db.ForeignKey('game.id'), primary_key=True)
)
game_secondary_4 = db.Table(
    'game_secondary_4',
    db.Column('secondary_id', db.Integer, db.ForeignKey('secondary.id'), primary_key=True),
    db.Column('game_id', db.Integer, db.ForeignKey('game.id'), primary_key=True)
)
game_secondary_5 = db.Table(
    'game_secondary_5',
    db.Column('secondary_id', db.Integer, db.ForeignKey('secondary.id'), primary_key=True),
    db.Column('game_id', db.Integer, db.ForeignKey('game.id'), primary_key=True)
)
game_secondary_6 = db.Table(
    'game_secondary_6',
    db.Column('secondary_id', db.Integer, db.ForeignKey('secondary.id'), primary_key=True),
    db.Column('game_id', db.Integer, db.ForeignKey('game.id'), primary_key=True)
)
game_secondary_7 = db.Table(
    'game_secondary_7',
    db.Column('secondary_id', db.Integer, db.ForeignKey('secondary.id'), primary_key=True),
    db.Column('game_id', db.Integer, db.ForeignKey('game.id'), primary_key=True)
)
game_secondary_8 = db.Table(
    'game_secondary_8',
    db.Column('secondary_id', db.Integer, db.ForeignKey('secondary.id'), primary_key=True),
    db.Column('game_id', db.Integer, db.ForeignKey('game.id'), primary_key=True)
)


class Game(db.Model):
    __tablename__ = 'game'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    mission = db.relationship("Mission", secondary=game_mission)
    initFirst = db.relationship("Player", secondary=player_game_init_1)
    initSecond = db.relationship("Player", secondary=player_game_init_2)
    initThird = db.relationship("Player", secondary=player_game_init_3)
    initFourth = db.relationship("Player", secondary=player_game_init_4)
    initFifth = db.relationship("Player", secondary=player_game_init_5)
    winner = db.relationship("Player", secondary=player_game_winner)
    winFaction = db.relationship("Faction", secondary=game_faction_winner)
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
    winSecondarySecond = db.relationship("Secondary", secondary=game_secondary_2)
    winSecondarySecondScore = db.Column(db.Integer)
    winSecondaryThird = db.relationship("Secondary", secondary=game_secondary_3)
    winSecondaryThirdScore = db.Column(db.Integer)
    winSecondaryFourth = db.relationship("Secondary", secondary=game_secondary_4)
    winSecondaryFourthScore = db.Column(db.Integer)
    loser = db.relationship("Player", secondary=player_game_loser)
    losFaction = db.relationship("Faction", secondary=game_faction_loser)
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
    losSecondarySecond = db.relationship("Secondary", secondary=game_secondary_6)
    losSecondarySecondScore = db.Column(db.Integer)
    losSecondaryThird = db.relationship("Secondary", secondary=game_secondary_7)
    losSecondaryThirdScore = db.Column(db.Integer)
    losSecondaryFourth = db.relationship("Secondary", secondary=game_secondary_8)
    losSecondaryFourthScore = db.Column(db.Integer)
    rollOffWinner = db.relationship("Player", secondary=player_game_roloff)
    rollOffSelection = db.Column(db.String(20))
    tie = db.Column(db.Boolean)


class Mission(db.Model):
    __tablename__ = 'mission'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    shortName = db.Column(db.String(50))
    code = db.Column(db.Float)


class Secondary(db.Model):
    __tablename__ = 'secondary'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    shortName = db.Column(db.String(100))


class Faction(db.Model):
    __tablename__ = 'faction'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    shortName = db.Column(db.String(100))


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
    games = db.relationship("Game", secondary=game_tournament)


class Player(db.Model):
    __tablename__ = 'player'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False)
    shortName = db.Column(db.String(30))
    rank = db.relationship("Rank", secondary=player_rank)
    score = db.Column(db.Integer)
    wins = db.Column(db.Integer)
    ties = db.Column(db.Integer)
    loses = db.Column(db.Integer)
