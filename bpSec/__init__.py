from flask import Blueprint, request, render_template
from flask_login import current_user
from utils import getUpdates
from utils.secondary import getSecondaries, getSecondary


secondaryBP = Blueprint('secondaryBluePrint', __name__)


@secondaryBP.route("/secondaries", methods={"GET", "POST"})
def secondaries():
    scs = getSecondaries()
    return render_template(
        'secondaries.html',
        title="Secondaries",
        user=current_user if not current_user.is_anonymous else None,
        secondaries=scs,
        upd=getUpdates(),
        preferred=request.cookies['preferred_update'] if 'preferred_update' in request.cookies.keys() else '1'
    )


@secondaryBP.route("/secondary/<sc>", methods={"GET", "POST"})
def secondary(sc):
    sc = getSecondary(sc)
    return render_template(
        'secondary.html',
        title=sc['sql'].name,
        user=current_user if not current_user.is_anonymous else None,
        secondary=sc,
        upd=getUpdates(),
        preferred=request.cookies['preferred_update'] if 'preferred_update' in request.cookies.keys() else '1'
    )