from flask import Blueprint, request, render_template, redirect, url_for, current_app
from flask_login import current_user, login_required

from database import Faction

from utils import randomize_data, addNewUpdate
from utils.decorators import only_admin, only_collaborator
from utils.player import updatePlayers
from utils.mission import updateMissions
from utils.secondary import updateSecondaries
from utils.faction import updateFactions


adminBP = Blueprint('adminBluePrint', __name__)


@adminBP.route("/randomize", methods={"GET", "POST"})
@login_required
@only_admin
def randomize():
    randomize_data()
    return redirect(url_for('genericBluePrint.general'))


@adminBP.route("/update", methods={"GET", "POST"})
@login_required
@only_admin
def update():
    updateFactions(current_app.config['database'])
    updateMissions(current_app.config['database'])
    updateSecondaries(current_app.config['database'])
    updatePlayers(current_app.config['database'])
    return redirect(url_for('genericBluePrint.general'))


@adminBP.route("/addupdate", methods={"GET", "POST"})
@login_required
@only_collaborator
def addUpdate():
    if request.method == 'POST':
        addNewUpdate(request.form)
        return redirect(url_for('adminBluePrint.update'))
    fct = Faction.query.all()
    return render_template(
        'addupdate.html',
        title="Update",
        user=current_user if not current_user.is_anonymous else None,
        factions=fct
    )
