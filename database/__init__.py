from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


player_game_winner = db.Table(
    'player_game_winner',
    db.Column('game_id', db.Integer, db.ForeignKey('game.id'), primary_key=True, unique=False),
    db.Column('player_id', db.Integer, db.ForeignKey('player.id'), primary_key=True, unique=False)
)
player_game_loser = db.Table(
    'player_game_loser',
    db.Column('game_id', db.Integer, db.ForeignKey('game.id'), primary_key=True, unique=False),
    db.Column('player_id', db.Integer, db.ForeignKey('player.id'), primary_key=True, unique=False)
)
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


class Game(db.Model):
    __tablename__ = 'game'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    timestamp = db.Column(db.Integer)
    mission = db.relationship("Mission", secondary=game_mission)
    initFirst = db.relationship("Faction", secondary=faction_game_init_1)
    initSecond = db.relationship("Faction", secondary=faction_game_init_2)
    initThird = db.relationship("Faction", secondary=faction_game_init_3)
    initFourth = db.relationship("Faction", secondary=faction_game_init_4)
    initFifth = db.relationship("Faction", secondary=faction_game_init_5)
    winner = db.relationship("Player", secondary=player_game_winner)
    winScouting = db.Column(db.String(20))
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
    loser = db.relationship("Player", secondary=player_game_loser)
    losScouting = db.Column(db.String(20))
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

    bestCounter = {},
    worstCounter = {},
    counterRates = {},
    bestMission = {},
    worstMission = {},
    bestSecondary = {},
    worstSecondary = {},
    tieCounter = {}


class WinRates(db.Model):
    __tablename__ = 'winrates'
    id = db.Column(db.Integer, primary_key=True)
    faction1 = db.Column(db.Integer, db.ForeignKey('faction.id'))
    faction2 = db.Column(db.Integer, db.ForeignKey('faction.id'))
    rate1 = db.Column(db.Float)
    rate2 = db.Column(db.Float)
    rate3 = db.Column(db.Float)


class MissionRates(db.Model):
    __tablename__ = 'missionrates'
    id = db.Column(db.Integer, primary_key=True)
    faction = db.Column(db.Integer, db.ForeignKey('faction.id'))
    mission = db.Column(db.Integer, db.ForeignKey('mission.id'))
    rate1 = db.Column(db.Float)
    rate2 = db.Column(db.Float)
    rate3 = db.Column(db.Float)


class SecondaryRates(db.Model):
    __tablename__ = 'cesondaryrates'
    id = db.Column(db.Integer, primary_key=True)
    faction = db.Column(db.Integer, db.ForeignKey('faction.id'))
    secondary = db.Column(db.Integer, db.ForeignKey('secondary.id'))
    rate1 = db.Column(db.Float)
    rate2 = db.Column(db.Float)
    rate3 = db.Column(db.Float)


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
    gamesWon = db.relationship("Game", secondary=player_game_won)
    gamesLost = db.relationship("Game", secondary=player_game_lost)
    gamesTied = db.relationship("Game", secondary=player_game_tie)
    wins = db.Column(db.Integer)
    ties = db.Column(db.Integer)
    loses = db.Column(db.Integer)
