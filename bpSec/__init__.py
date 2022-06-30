from flask import Blueprint, request, render_template
from flask_login import current_user

from utils import getUpdates
from utils.secondary import getSecondaries, getSecondary
from utils.games import getGameTypes
from utils.log import logAccess


secondaryBP = Blueprint('secondaryBluePrint', __name__)


@secondaryBP.route("/secondaries", methods={"GET", "POST"})
def secondaries():
    scs = getSecondaries()
    logAccess('/secondaries', current_user, request)
    return render_template(
        'secondaries.html',
        title="Secondaries",
        user=current_user if not current_user.is_anonymous else None,
        secondaries=scs,
        upd=getUpdates(),
        gt=getGameTypes(),
        preferredGameType=request.cookies['preferred_gameType'] if 'preferred_gameType' in request.cookies.keys() else '1',
        preferred=request.cookies['preferred_update'] if 'preferred_update' in request.cookies.keys() else '1',
        language=request.cookies['preferred_language'] if 'preferred_language' in request.cookies.keys() else 'en'
    )


@secondaryBP.route("/secondary/<sc>", methods={"GET", "POST"})
def secondary(sc):
    logAccess('/secondary/{}'.format(sc), current_user, request)
    sc = getSecondary(sc)
    return render_template(
        'secondary.html',
        title=sc['sql'].name,
        user=current_user if not current_user.is_anonymous else None,
        secondary=sc,
        upd=getUpdates(),
        gt=getGameTypes(),
        preferredGameType=request.cookies['preferred_gameType'] if 'preferred_gameType' in request.cookies.keys() else '1',
        preferred=request.cookies['preferred_update'] if 'preferred_update' in request.cookies.keys() else '1',
        language=request.cookies['preferred_language'] if 'preferred_language' in request.cookies.keys() else 'en'
    )