from flask import Blueprint, request, render_template, current_app, url_for, redirect
from flask_login import current_user, login_required

from utils import getUpdates
from utils.decorators import only_admin
from utils.secondary import getSecondaries, getSecondary, updateSecondaries
from utils.games import getGameTypes, getEditions
from utils.log import logAccess


secondaryBP = Blueprint('secondaryBluePrint', __name__)


@secondaryBP.route("/secondaries", methods={"GET", "POST"})
def secondaries():
    scs = getSecondaries(int(request.cookies['preferred_update']) if 'preferred_update' in request.cookies.keys() else 1,
                         int(request.cookies['preferred_gameType'] if 'preferred_gameType' in request.cookies.keys() else 1),
                         int(request.cookies['preferred_edition'] if 'preferred_edition' in request.cookies.keys() else 1))
    logAccess('/secondaries', current_user, request)
    return render_template(
        'secondaries.html',
        title="Secondaries",
        user=current_user if not current_user.is_anonymous else None,
        secondaries=scs,
        upd=getUpdates(),
        gt=getGameTypes(),
        ed=getEditions(),
        preferredEdition=request.cookies['preferred_edition'] if 'preferred_edition' in request.cookies.keys() else '1',
        preferredGameType=request.cookies['preferred_gameType'] if 'preferred_gameType' in request.cookies.keys() else '1',
        preferred=request.cookies['preferred_update'] if 'preferred_update' in request.cookies.keys() else '1',
        language=request.cookies['preferred_language'] if 'preferred_language' in request.cookies.keys() else 'en'
    )


@secondaryBP.route("/secondary/<sc>", methods={"GET", "POST"})
def secondary(sc):
    logAccess('/secondary/{}'.format(sc), current_user, request)
    sc = getSecondary(sc,
                      int(request.cookies['preferred_update']) if 'preferred_update' in request.cookies.keys() else 1,
                      int(request.cookies['preferred_gameType'] if 'preferred_gameType' in request.cookies.keys() else 1),
                      int(request.cookies['preferred_edition'] if 'preferred_edition' in request.cookies.keys() else 1))
    return render_template(
        'secondary.html',
        title=sc['sql'].name,
        user=current_user if not current_user.is_anonymous else None,
        secondary=sc,
        upd=getUpdates(),
        gt=getGameTypes(),
        ed=getEditions(),
        preferredEdition=request.cookies['preferred_edition'] if 'preferred_edition' in request.cookies.keys() else '1',
        preferredGameType=request.cookies['preferred_gameType'] if 'preferred_gameType' in request.cookies.keys() else '1',
        preferred=request.cookies['preferred_update'] if 'preferred_update' in request.cookies.keys() else '1',
        language=request.cookies['preferred_language'] if 'preferred_language' in request.cookies.keys() else 'en'
    )


@secondaryBP.route("/player/update", methods={"GET", "POST"})
@login_required
@only_admin
def updateTournament():
    logAccess('/secondary/update', current_user, request)
    updateSecondaries(current_app.config['database'])
    return redirect(url_for('secondaryBluePrint.secondaries'))
