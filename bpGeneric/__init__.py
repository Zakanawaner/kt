from flask import Blueprint, request, render_template
from flask_login import current_user

from utils import getUpdates, getGeneral
from utils.games import getGameTypes


genericBP = Blueprint('genericBluePrint', __name__)


@genericBP.route("/", methods={"GET", "POST"})
def general():
    gen = getGeneral()
    return render_template(
        'general.html',
        title="General",
        user=current_user if not current_user.is_anonymous else None,
        gen=gen,
        upd=getUpdates(),
        gt=getGameTypes(),
        preferredGameType=request.cookies['preferred_gameType'] if 'preferred_gameType' in request.cookies.keys() else '0',
        preferred=request.cookies['preferred_update'] if 'preferred_update' in request.cookies.keys() else '0'
    )


@genericBP.route("/about", methods={"GET", "POST"})
def about():
    return render_template(
        'about.html',
        title="About",
        user=current_user if not current_user.is_anonymous else None
    )


@genericBP.route("/team", methods={"GET", "POST"})
def team():
    return render_template(
        'teamKTD.html',
        title="Team KTD",
        user=current_user if not current_user.is_anonymous else None
    )