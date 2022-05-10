from flask import Blueprint, request, render_template
from flask_login import current_user

from utils import getUpdates
from utils.mission import getMission, getMissions


missionBP = Blueprint('missionBluePrint', __name__)


@missionBP.route("/missions", methods={"GET", "POST"})
def missions():
    mss = getMissions()
    return render_template(
        'missions.html',
        title="Missions",
        user=current_user if not current_user.is_anonymous else None,
        missions=mss,
        upd=getUpdates(),
        preferred=request.cookies['preferred_update'] if 'preferred_update' in request.cookies.keys() else '1'
    )


@missionBP.route("/mission/<ms>", methods={"GET", "POST"})
def mission(ms):
    mss = getMission(ms)
    return render_template(
        'mission.html',
        title=mss['sql'].name,
        user=current_user if not current_user.is_anonymous else None,
        mission=mss,
        upd=getUpdates(),
        preferred=request.cookies['preferred_update'] if 'preferred_update' in request.cookies.keys() else '1'
    )
