from flask import Blueprint, request, render_template, flash, redirect, url_for, current_app
from flask_login import current_user, login_required
from flask_babel import gettext

from utils import getUpdates, getPlayers, getPlayer, getGameTypes, setPlayerPermission, getEditions, updatePlayers, updatePlayer
from utils.log import logAccess
from utils.decorators import only_left_hand, only_admin


playerBP = Blueprint('playerBluePrint', __name__)


@playerBP.route("/players", methods={"GET", "POST"})
def players():
    pls = getPlayers(int(request.cookies['preferred_update']) if 'preferred_update' in request.cookies.keys() else 1,
                     int(request.cookies['preferred_gameType'] if 'preferred_gameType' in request.cookies.keys() else 1),
                     int(request.cookies['preferred_edition'] if 'preferred_edition' in request.cookies.keys() else 1))
    logAccess('/players', current_user, request)
    return render_template(
        'players.html',
        title="Players",
        user=current_user if not current_user.is_anonymous else None,
        players=pls,
        upd=getUpdates(),
        gt=getGameTypes(),
        ed=getEditions(),
        preferredEdition=request.cookies['preferred_edition'] if 'preferred_edition' in request.cookies.keys() else '1',
        preferredGameType=request.cookies['preferred_gameType'] if 'preferred_gameType' in request.cookies.keys() else '1',
        preferred=request.cookies['preferred_update'] if 'preferred_update' in request.cookies.keys() else '1',
        language=request.cookies['preferred_language'] if 'preferred_language' in request.cookies.keys() else 'en'
    )


@playerBP.route("/player/<pl>", methods={"GET", "POST"})
def player(pl):
    logAccess('/player/{}'.format(pl), current_user, request)
    pl = getPlayer(pl,
                   int(request.cookies['preferred_update']) if 'preferred_update' in request.cookies.keys() else 1,
                   int(request.cookies['preferred_gameType'] if 'preferred_gameType' in request.cookies.keys() else 1),
                   int(request.cookies['preferred_edition'] if 'preferred_edition' in request.cookies.keys() else 1))
    if pl['sql'] == current_user:
        return render_template(
            'profile.html',
            title=pl['sql'].username,
            user=current_user,
            player=pl,
            upd=getUpdates(),
            gt=getGameTypes(),
            ed=getEditions(),
            preferredEdition=request.cookies['preferred_edition'] if 'preferred_edition' in request.cookies.keys() else '1',
            preferredGameType=request.cookies['preferred_gameType'] if 'preferred_gameType' in request.cookies.keys() else '1',
            preferred=request.cookies['preferred_update'] if 'preferred_update' in request.cookies.keys() else '1',
            language=request.cookies['preferred_language'] if 'preferred_language' in request.cookies.keys() else 'en'
        )
    if not pl['sql'].allowSharing:
        flash(gettext("Player hidden"))
        return redirect(url_for('genericBluePrint.general'))
    return render_template(
        'player.html',
        title=pl['sql'].username,
        user=current_user if not current_user.is_anonymous else None,
        player=pl,
        upd=getUpdates(),
        gt=getGameTypes(),
        ed=getEditions(),
        preferredEdition=request.cookies['preferred_edition'] if 'preferred_edition' in request.cookies.keys() else '1',
        preferredGameType=request.cookies['preferred_gameType'] if 'preferred_gameType' in request.cookies.keys() else '1',
        preferred=request.cookies['preferred_update'] if 'preferred_update' in request.cookies.keys() else '1',
        language=request.cookies['preferred_language'] if 'preferred_language' in request.cookies.keys() else 'en',
        permissions=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    )


@playerBP.route("/player/<pl>/permission", methods={"GET", "POST"})
@login_required
@only_left_hand
def changePlayerPermissions(pl):
    logAccess('/player/{}/permission'.format(pl), current_user, request)
    if setPlayerPermission(current_app.config["database"], pl, request.form):
        flash("OK")
    else:
        flash("No OK")
    pl = getPlayer(pl, 1, 1, 1)
    return redirect(url_for('playerBluePrint.player', pl=pl['sql'].id))


@playerBP.route("/player/update", methods={"GET", "POST"})
@login_required
@only_admin
def updatePlayerGl():
    logAccess('/player/update', current_user, request)
    updatePlayers(current_app.config['database'])
    return redirect(url_for('playerBluePrint.players'))


@playerBP.route("/player/update/<pl>", methods={"GET", "POST"})
@login_required
@only_admin
def updatePlayerUnique(pl):
    logAccess('/player/update', current_user, request)
    updatePlayer(current_app.config['database'], int(pl))
    return redirect(url_for('playerBluePrint.players'))