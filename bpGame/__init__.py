import json

from flask import Blueprint, request, render_template, current_app, request
from flask_login import current_user, login_required

from utils import getUpdates
from utils.games import getGames, getGame, getGameTypes
from utils.dataHandlers import handleGameData
from utils.decorators import only_adamantium
from utils.faction import getFactions
from utils.mission import getMissions
from utils.secondary import getSecondaries
from utils.player import getPlayers
from utils.log import logAccess


gameBP = Blueprint('gameBluePrint', __name__)


@gameBP.route("/gamedata", methods={"GET", "POST"})
def data():
    logAccess('/gamedata', current_user, request)
    gameData = handleGameData(json.loads(request.data.decode()), current_app.config['database'])
    if gameData == "Already saved":
        return {'status': gameData}, 200
    if gameData == "Bad game data":
        return {'status': gameData}, 200
    current_app.config['twitterClient'].newGame(gameData)
    return {'status': 'ok'}, 200


@gameBP.route("/games", methods={"GET", "POST"})
def games():
    gms = getGames()
    logAccess('/games', current_user, request)
    return render_template(
        'games.html',
        title="Games",
        user=current_user if not current_user.is_anonymous else None,
        games=gms,
        upd=getUpdates(),
        gt=getGameTypes(),
        preferredGameType=request.cookies['preferred_gameType'] if 'preferred_gameType' in request.cookies.keys() else '1',
        preferred=request.cookies['preferred_update'] if 'preferred_update' in request.cookies.keys() else '1',
        language=request.cookies['preferred_language'] if 'preferred_language' in request.cookies.keys() else 'en'
    )


@gameBP.route("/game/<gm>", methods={"GET", "POST"})
def game(gm):
    logAccess('/game/{}'.format(gm), current_user, request)
    gm = getGame(gm)
    return render_template(
        'game.html',
        title="Game",
        user=current_user if not current_user.is_anonymous else None,
        game=gm,
        upd=getUpdates(),
        gt=getGameTypes(),
        preferredGameType=request.cookies['preferred_gameType'] if 'preferred_gameType' in request.cookies.keys() else '1',
        preferred=request.cookies['preferred_update'] if 'preferred_update' in request.cookies.keys() else '1',
        language=request.cookies['preferred_language'] if 'preferred_language' in request.cookies.keys() else 'en'
    )


@gameBP.route("/game/add", methods={"GET", "POST"})
@login_required
@only_adamantium
def addGame():
    logAccess('/game/add', current_user, request)
    return render_template(
        'addgame.html',
        title="New Game",
        user=current_user if not current_user.is_anonymous else None,
        factions=getFactions(),
        missions=getMissions(),
        secondaries=getSecondaries(),
        players=getPlayers(),
        gameTypes=getGameTypes()
    )
