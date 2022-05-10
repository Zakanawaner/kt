import json

from flask import Blueprint, request, render_template, current_app
from flask_login import current_user
from utils import getUpdates
from utils.games import getGames, getGame
from utils.dataHandlers import handleGameData


gameBP = Blueprint('gameBluePrint', __name__)


@gameBP.route("/gamedata", methods={"GET", "POST"})
def data():
    handleGameData(json.loads(request.data.decode()), current_app.config['database'])
    return {'status': 'ok'}, 200


@gameBP.route("/games", methods={"GET", "POST"})
def games():
    gms = getGames()
    return render_template(
        'games.html',
        title="Games",
        user=current_user if not current_user.is_anonymous else None,
        games=gms,
        upd=getUpdates(),
        preferred=request.cookies['preferred_update'] if 'preferred_update' in request.cookies.keys() else '1'
    )


@gameBP.route("/game/<gm>", methods={"GET", "POST"})
def game(gm):
    gm = getGame(gm)
    return render_template(
        'game.html',
        title="Game",
        user=current_user if not current_user.is_anonymous else None,
        game=gm,
        upd=getUpdates(),
        preferred=request.cookies['preferred_update'] if 'preferred_update' in request.cookies.keys() else '1'
    )
