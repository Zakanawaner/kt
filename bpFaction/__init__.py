from flask import Blueprint, request, render_template, current_app, redirect, url_for
from flask_login import current_user, login_required

from utils import getUpdates
from utils.decorators import only_admin
from utils.faction import getFactions, getFaction, updateFactions
from utils.games import getGameTypes, getEditions
from utils.log import logAccess


factionBP = Blueprint('factionBluePrint', __name__)


@factionBP.route("/factions", methods={"GET", "POST"})
def factions():
    fct = getFactions(int(request.cookies['preferred_update']) if 'preferred_update' in request.cookies.keys() else 1,
                      int(request.cookies['preferred_gameType'] if 'preferred_gameType' in request.cookies.keys() else 1),
                      int(request.cookies['preferred_edition'] if 'preferred_edition' in request.cookies.keys() else 1))
    logAccess('/factions', current_user, request)
    return render_template(
        'factions.html',
        title="Factions",
        user=current_user if not current_user.is_anonymous else None,
        factions=fct,
        upd=getUpdates(),
        gt=getGameTypes(),
        ed=getEditions(),
        preferredGameType=request.cookies['preferred_gameType'] if 'preferred_gameType' in request.cookies.keys() else '1',
        preferredEdition=request.cookies['preferred_edition'] if 'preferred_edition' in request.cookies.keys() else '1',
        preferred=request.cookies['preferred_update'] if 'preferred_update' in request.cookies.keys() else '1',
        language=request.cookies['preferred_language'] if 'preferred_language' in request.cookies.keys() else 'en'
    )


@factionBP.route("/faction/<fact>", methods={"GET", "POST"})
def faction(fact):
    fct = getFaction(fact,
                     int(request.cookies['preferred_update']) if 'preferred_update' in request.cookies.keys() else 1,
                     int(request.cookies['preferred_gameType'] if 'preferred_gameType' in request.cookies.keys() else 1),
                     int(request.cookies['preferred_edition'] if 'preferred_edition' in request.cookies.keys() else 1))
    logAccess('/faction/{}'.format(fact), current_user, request)
    return render_template(
        'faction.html',
        title=fct['sql'].name,
        user=current_user if not current_user.is_anonymous else None,
        faction=fct,
        upd=getUpdates(),
        gt=getGameTypes(),
        ed=getEditions(),
        preferredGameType=request.cookies['preferred_gameType'] if 'preferred_gameType' in request.cookies.keys() else '1',
        preferredEdition=request.cookies['preferred_edition'] if 'preferred_edition' in request.cookies.keys() else '1',
        preferred=request.cookies['preferred_update'] if 'preferred_update' in request.cookies.keys() else '1',
        language=request.cookies['preferred_language'] if 'preferred_language' in request.cookies.keys() else 'en'
    )


@factionBP.route("/faction/update", methods={"GET", "POST"})
@login_required
@only_admin
def updateTournament():
    logAccess('/faction/update', current_user, request)
    updateFactions(current_app.config['database'])
    return redirect(url_for('factionBluePrint.factions'))
