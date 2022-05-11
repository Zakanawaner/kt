from flask import Blueprint, request, render_template
from flask_login import current_user

from utils import getUpdates
from utils.faction import getFactions, getFaction
from utils.games import getGameTypes


factionBP = Blueprint('factionBluePrint', __name__)


@factionBP.route("/factions", methods={"GET", "POST"})
def factions():
    fct = getFactions()
    return render_template(
        'factions.html',
        title="Factions",
        user=current_user if not current_user.is_anonymous else None,
        factions=fct,
        upd=getUpdates(),
        gt=getGameTypes(),
        preferredGameType=request.cookies['preferred_gameType'] if 'preferred_gameType' in request.cookies.keys() else '0',
        preferred=request.cookies['preferred_update'] if 'preferred_update' in request.cookies.keys() else '0'
    )


@factionBP.route("/faction/<fact>", methods={"GET", "POST"})
def faction(fact):
    fct = getFaction(fact)
    return render_template(
        'faction.html',
        title=fct['sql'].name,
        user=current_user if not current_user.is_anonymous else None,
        faction=fct,
        upd=getUpdates(),
        gt=getGameTypes(),
        preferredGameType=request.cookies['preferred_gameType'] if 'preferred_gameType' in request.cookies.keys() else '0',
        preferred=request.cookies['preferred_update'] if 'preferred_update' in request.cookies.keys() else '0'
    )
