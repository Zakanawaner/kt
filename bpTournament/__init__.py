import json

from flask import Blueprint, request, render_template, current_app, request, url_for, redirect, flash
from flask_login import current_user, login_required

from utils import getUpdates
from utils.games import getGames, getGame, getGameTypes, getEditions
from utils.tournament import getTournaments, addNewTournament, getTournament
from utils.decorators import only_tournament_organizer
from utils.faction import getFactions
from utils.mission import getMissions
from utils.secondary import getSecondaries
from utils.player import getPlayers
from utils.log import logAccess


tournamentBP = Blueprint('tournamentBluePrint', __name__)


@tournamentBP.route("/tournaments", methods={"GET", "POST"})
def tournaments():
    tours = getTournaments(int(request.cookies['preferred_update']) if 'preferred_update' in request.cookies.keys() else 1,
                           int(request.cookies['preferred_gameType'] if 'preferred_gameType' in request.cookies.keys() else 1),
                           int(request.cookies['preferred_edition'] if 'preferred_edition' in request.cookies.keys() else 1))
    logAccess('/tournaments', current_user, request)
    return render_template(
        'tournaments.html',
        title="Tournaments",
        user=current_user if not current_user.is_anonymous else None,
        tournaments=tours,
        upd=getUpdates(),
        gt=getGameTypes(),
        ed=getEditions(),
        preferredEdition=request.cookies['preferred_edition'] if 'preferred_edition' in request.cookies.keys() else '1',
        preferredGameType=request.cookies['preferred_gameType'] if 'preferred_gameType' in request.cookies.keys() else '1',
        preferred=request.cookies['preferred_update'] if 'preferred_update' in request.cookies.keys() else '1',
        language=request.cookies['preferred_language'] if 'preferred_language' in request.cookies.keys() else 'en'
    )


@tournamentBP.route("/tournament/<tr>", methods={"GET", "POST"})
def tournament(tr):
    logAccess('/tournament/{}'.format(tr), current_user, request)
    tr = getTournament(tr, 1, 1, 1)
    return render_template(
        'tournament.html',
        title="Tournament",
        user=current_user if not current_user.is_anonymous else None,
        tournament=tr,
        upd=getUpdates(),
        gt=getGameTypes(),
        ed=getEditions(),
        preferredEdition=request.cookies['preferred_edition'] if 'preferred_edition' in request.cookies.keys() else '1',
        preferredGameType=request.cookies['preferred_gameType'] if 'preferred_gameType' in request.cookies.keys() else '1',
        preferred=request.cookies['preferred_update'] if 'preferred_update' in request.cookies.keys() else '1',
        language=request.cookies['preferred_language'] if 'preferred_language' in request.cookies.keys() else 'en'
    )


@tournamentBP.route("/tournament/add", methods={"GET", "POST"})
@login_required
@only_tournament_organizer
def addTournament():
    logAccess('/tournament/add', current_user, request)
    if request.method == "POST":
        resp = addNewTournament(request.form, current_app.config['database'])
        flash(resp)
        return redirect(url_for('tournamentBluePrint.tournaments'))
    return render_template(
        'addtournament.html',
        title="New Tournament",
        user=current_user if not current_user.is_anonymous else None,
        factions=getFactions(1, 1, 1),
        missions=getMissions(1, 1, 1),
        secondaries=getSecondaries(1, 1, 1),
        players=getPlayers(1, 1, 1),
        gameTypes=getGameTypes(),
        editions=getEditions()
    )
