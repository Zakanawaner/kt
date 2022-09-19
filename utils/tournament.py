from sqlalchemy import extract, desc
from datetime import datetime
from collections import OrderedDict
from database import (
    Tournament, Player, Faction, TournamentOrganizers
)


###############
# Tournaments #
def addNewTournament(info, sender, db):
    if not Tournament.query.filter_by(shortName=info['name'].lower().replace(" ", "")).first():
        tournament = Tournament(
            name=info['name'],
            shortName=info['name'].lower().replace(" ", ""),
            dateInit=datetime.strptime(info['dateInit'], '%Y-%m-%d'),
            dateEnd=datetime.strptime(info['dateEnd'], '%Y-%m-%d'),
        )
        db.session.add(tournament)
        db.session.commit()
        organizer = TournamentOrganizers(
            tournament=tournament.id,
            organizer=sender.id,
        )
        db.session.add(organizer)
        db.session.commit()
        return "Tournament added"
    else:
        return "Tournament Already Exists"


def getTournaments(up, tp, ed):
    tournaments = {}
    for tournament in Tournament.query.all():
        if tournament.name:
            tournaments[tournament.id] = getTournament(tournament.id, up, tp, ed)
    return [item for item in tournaments.values()]


def getTournament(tour, up, tp, ed):
    tournamentGl = {
        'sql': Tournament.query.filter_by(id=tour).first(),
        'rates': {}
    }
    tournament = {
        'totalGames': len(tournamentGl['sql'].games),
        'totalPlayers': len(tournamentGl['sql'].players),
        'playerRates': {},
        'winner': None,
        'factionWinner': None,
        'factionRates': {}
    }

    for game in tournamentGl['sql'].games:
        winner = Player.query.filter_by(steamId=game.winnerId).first()
        loser = Player.query.filter_by(steamId=game.loserId).first()
        if winner:
            if str(winner.id) not in tournament['playerRates'].keys():
                player = {
                    'sql': winner,
                    'faction': game.winFaction[0],
                    'wins': 0,
                    'loses': 0,
                    'ties': 0,
                    'total': 0
                }
                player['wins'] += 1 if not game.tie else 0
                player['ties'] += 1 if game.tie else 0
                player['total'] += 1
                tournament['playerRates'][str(winner.id)] = player
            else:
               tournament['playerRates'][str(winner.id)]['wins'] += 1 if not game.tie else 0
               tournament['playerRates'][str(winner.id)]['ties'] += 1 if game.tie else 0
               tournament['playerRates'][str(winner.id)]['total'] += 1
        if loser:
            if str(loser.id) not in tournament['playerRates'].keys():
                player = {
                    'sql': loser,
                    'faction': game.losFaction[0],
                    'wins': 0,
                    'loses': 0,
                    'ties': 0,
                    'total': 0
                }
                player['loses'] += 1 if not game.tie else 0
                player['ties'] += 1 if game.tie else 0
                player['total'] += 1
                tournament['playerRates'][str(loser.id)] = player
            else:
                tournament['playerRates'][str(loser.id)]['loses'] += 1 if not game.tie else 0
                tournament['playerRates'][str(loser.id)]['ties'] += 1 if game.tie else 0
                tournament['playerRates'][str(loser.id)]['total'] += 1
        winFaction = game.winFaction[0]
        losFaction = game.losFaction[0]
        if str(winFaction.id) not in tournament['factionRates'].keys():
            faction = {
                'sql': winFaction,
                'wins': 0,
                'loses': 0,
                'ties': 0,
                'total': 0
            }
            faction['wins'] += 1 if not game.tie else 0
            faction['ties'] += 1 if game.tie else 0
            faction['total'] += 1
            tournament['factionRates'][str(winFaction.id)] = faction
        else:
            tournament['factionRates'][str(winFaction.id)]['wins'] += 1 if not game.tie else 0
            tournament['factionRates'][str(winFaction.id)]['ties'] += 1 if game.tie else 0
            tournament['factionRates'][str(winFaction.id)]['total'] += 1
        if str(losFaction.id) not in tournament['factionRates'].keys():
            faction = {
                'sql': losFaction,
                'wins': 0,
                'loses': 0,
                'ties': 0,
                'total': 0
            }
            faction['wins'] += 1 if not game.tie else 0
            faction['ties'] += 1 if game.tie else 0
            faction['total'] += 1
            tournament['factionRates'][str(losFaction.id)] = faction
        else:
            tournament['factionRates'][str(losFaction.id)]['wins'] += 1 if not game.tie else 0
            tournament['factionRates'][str(losFaction.id)]['ties'] += 1 if game.tie else 0
            tournament['factionRates'][str(losFaction.id)]['total'] += 1
    bestPlayer = {'winRate': 0}
    for player in tournament['playerRates'].keys():
        try:
            tournament['playerRates'][player]['winRate'] = round((tournament['playerRates'][player]['wins'] * 100) / tournament['playerRates'][player]['total'], 2)
            tournament['playerRates'][player]['loseRate'] = round((tournament['playerRates'][player]['loses'] * 100) / tournament['playerRates'][player]['total'], 2)
            tournament['playerRates'][player]['tieRate'] = round((tournament['playerRates'][player]['ties'] * 100) / tournament['playerRates'][player]['total'], 2)
        except ZeroDivisionError:
            tournament['playerRates'][player]['winRate'] = 0
            tournament['playerRates'][player]['loseRate'] = 0
            tournament['playerRates'][player]['tieRate'] = 0
        bestPlayer = tournament['playerRates'][player] if tournament['playerRates'][player]['winRate'] > bestPlayer['winRate'] else bestPlayer
    for faction in tournament['factionRates'].keys():
        try:
            tournament['factionRates'][faction]['winRate'] = round((tournament['factionRates'][faction]['wins'] * 100) / tournament['factionRates'][faction]['total'], 2)
            tournament['factionRates'][faction]['loseRate'] = round((tournament['factionRates'][faction]['loses'] * 100) / tournament['factionRates'][faction]['total'], 2)
            tournament['factionRates'][faction]['tieRate'] = round((tournament['factionRates'][faction]['ties'] * 100) / tournament['factionRates'][faction]['total'], 2)
        except ZeroDivisionError:
            tournament['factionRates'][faction]['winRate'] = 0
            tournament['factionRates'][faction]['loseRate'] = 0
            tournament['factionRates'][faction]['tieRate'] = 0
    tournamentGl['rates'] = tournament
    # TODO set winner if tournament ended
    return tournamentGl
