from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask_login import current_user
from utils import getUpdates, getPlayers, getPlayer, getGameTypes


playerBP = Blueprint('playerBluePrint', __name__)


@playerBP.route("/players", methods={"GET", "POST"})
def players():
    pls = getPlayers()
    return render_template(
        'players.html',
        title="Players",
        user=current_user if not current_user.is_anonymous else None,
        players=pls,
        upd=getUpdates(),
        gt=getGameTypes(),
        preferredGameType=request.cookies['preferred_gameType'] if 'preferred_gameType' in request.cookies.keys() else '1',
        preferred=request.cookies['preferred_update'] if 'preferred_update' in request.cookies.keys() else '1'
    )


@playerBP.route("/player/<pl>", methods={"GET", "POST"})
def player(pl):
    pl = getPlayer(pl)
    if pl['sql'] == current_user:
        return render_template(
            'profile.html',
            title=pl['sql'].username,
            user=current_user,
            player=pl,
            upd=getUpdates(),
            gt=getGameTypes(),
            preferredGameType=request.cookies['preferred_gameType'] if 'preferred_gameType' in request.cookies.keys() else '1',
            preferred=request.cookies['preferred_update'] if 'preferred_update' in request.cookies.keys() else '1'
        )
    if not pl['sql'].allowSharing:
        flash("Player hidden")
        return redirect(url_for('genericBluePrint.general'))
    return render_template(
        'player.html',
        title=pl['sql'].username,
        user=current_user if not current_user.is_anonymous else None,
        player=pl,
        upd=getUpdates(),
        gt=getGameTypes(),
        preferredGameType=request.cookies['preferred_gameType'] if 'preferred_gameType' in request.cookies.keys() else '1',
        preferred=request.cookies['preferred_update'] if 'preferred_update' in request.cookies.keys() else '1'
    )