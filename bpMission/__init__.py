from flask import Blueprint, request, render_template
from flask_login import current_user

from utils import getUpdates
from utils.mission import getMission, getMissions
from utils.games import getGameTypes
from utils.log import logAccess


missionBP = Blueprint('missionBluePrint', __name__)


@missionBP.route("/missions", methods={"GET", "POST"})
def missions():
    mss = getMissions()
    logAccess('/missions', current_user, request)
    return render_template(
        'missions.html',
        title="Missions",
        user=current_user if not current_user.is_anonymous else None,
        missions=mss,
        upd=getUpdates(),
        gt=getGameTypes(),
        preferredGameType=request.cookies['preferred_gameType'] if 'preferred_gameType' in request.cookies.keys() else '1',
        preferred=request.cookies['preferred_update'] if 'preferred_update' in request.cookies.keys() else '1'
    )


@missionBP.route("/mission/<ms>", methods={"GET", "POST"})
def mission(ms):
    logAccess('/player/{}'.format(ms), current_user, request)
    mss = getMission(ms)
    return render_template(
        'mission.html',
        title=mss['sql'].name,
        user=current_user if not current_user.is_anonymous else None,
        mission=mss,
        upd=getUpdates(),
        gt=getGameTypes(),
        preferredGameType=request.cookies['preferred_gameType'] if 'preferred_gameType' in request.cookies.keys() else '1',
        preferred=request.cookies['preferred_update'] if 'preferred_update' in request.cookies.keys() else '1'
    )
