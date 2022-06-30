from flask import Blueprint, request, render_template
from flask_login import current_user

from utils import getUpdates, getGeneral
from utils.games import getGameTypes
from utils.log import logAccess


genericBP = Blueprint('genericBluePrint', __name__)


@genericBP.route("/", methods={"GET", "POST"})
def general():
    gen = getGeneral()
    logAccess('/', current_user, request)
    return render_template(
        'general.html',
        title="General",
        user=current_user if not current_user.is_anonymous else None,
        gen=gen,
        upd=getUpdates(),
        gt=getGameTypes(),
        preferredGameType=request.cookies['preferred_gameType'] if 'preferred_gameType' in request.cookies.keys() else '1',
        preferred=request.cookies['preferred_update'] if 'preferred_update' in request.cookies.keys() else '1',
        language=request.cookies['preferred_language'] if 'preferred_language' in request.cookies.keys() else 'en'
    )


@genericBP.route("/about", methods={"GET", "POST"})
def about():
    logAccess('/about', current_user, request)
    return render_template(
        'about.html',
        title="About",
        user=current_user if not current_user.is_anonymous else None
    )


@genericBP.route("/team", methods={"GET", "POST"})
def team():
    logAccess('/team', current_user, request)
    return render_template(
        'teamKTD.html',
        title="Team KTD",
        user=current_user if not current_user.is_anonymous else None
    )