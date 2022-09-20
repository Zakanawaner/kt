from flask import Blueprint, request, render_template, current_app, redirect, url_for
from flask_login import current_user, login_required

from utils import getUpdates
from utils.decorators import only_admin
from utils.mission import getMission, getMissions, updateMissions
from utils.games import getGameTypes, getEditions
from utils.log import logAccess


missionBP = Blueprint('missionBluePrint', __name__)


@missionBP.route("/missions", methods={"GET", "POST"})
def missions():
    mss = getMissions(int(request.cookies['preferred_update']) if 'preferred_update' in request.cookies.keys() else 1,
                      int(request.cookies['preferred_gameType'] if 'preferred_gameType' in request.cookies.keys() else 1),
                      int(request.cookies['preferred_edition'] if 'preferred_edition' in request.cookies.keys() else 1))
    logAccess('/missions', current_user, request)
    return render_template(
        'missions.html',
        title="Missions",
        user=current_user if not current_user.is_anonymous else None,
        missions=mss,
        upd=getUpdates(),
        gt=getGameTypes(),
        ed=getEditions(),
        preferredEdition=request.cookies['preferred_edition'] if 'preferred_edition' in request.cookies.keys() else '1',
        preferredGameType=request.cookies['preferred_gameType'] if 'preferred_gameType' in request.cookies.keys() else '1',
        preferred=request.cookies['preferred_update'] if 'preferred_update' in request.cookies.keys() else '1',
        language=request.cookies['preferred_language'] if 'preferred_language' in request.cookies.keys() else 'en'
    )


@missionBP.route("/mission/<ms>", methods={"GET", "POST"})
def mission(ms):
    logAccess('/player/{}'.format(ms), current_user, request)
    mss = getMission(ms,
                     int(request.cookies['preferred_update']) if 'preferred_update' in request.cookies.keys() else 1,
                     int(request.cookies['preferred_gameType'] if 'preferred_gameType' in request.cookies.keys() else 1),
                     int(request.cookies['preferred_edition'] if 'preferred_edition' in request.cookies.keys() else 1))
    return render_template(
        'mission.html',
        title=mss['sql'].name,
        user=current_user if not current_user.is_anonymous else None,
        mission=mss,
        upd=getUpdates(),
        gt=getGameTypes(),
        ed=getEditions(),
        preferredEdition=request.cookies['preferred_edition'] if 'preferred_edition' in request.cookies.keys() else '1',
        preferredGameType=request.cookies['preferred_gameType'] if 'preferred_gameType' in request.cookies.keys() else '1',
        preferred=request.cookies['preferred_update'] if 'preferred_update' in request.cookies.keys() else '1',
        language=request.cookies['preferred_language'] if 'preferred_language' in request.cookies.keys() else 'en'
    )


@missionBP.route("/mission/update", methods={"GET", "POST"})
@login_required
@only_admin
def updateTournament():
    logAccess('/mission/update', current_user, request)
    updateMissions(current_app.config['database'])
    return redirect(url_for('missionBluePrint.missions'))
