from flask import Blueprint, request, flash, redirect, url_for
from flask_mail import Mail
from flask_login import login_required, current_user
from flask_babel import gettext

from utils.mail import subscribeUser, unSubscribeUser
from utils.log import logAccess

mailBP = Blueprint('mailBlueprint', __name__)

mailManager = Mail()


@mailBP.route("/subscribe", methods=['POST'])
@login_required
def subscribe():
    if subscribeUser(current_user, request.form):
        flash(gettext("Subscribed! Check your email"))
        return redirect(url_for('genericBluePrint.general'))
    logAccess('/subscribe', current_user, request)
    flash(gettext("That's not a correct mail address"))
    return redirect(url_for('playerBluePrint.player', pl=current_user.id))


@mailBP.route("/unsubscribe", methods=['POST'])
@login_required
def unSubscribe():
    unSubscribeUser(current_user)
    logAccess('/unsubscribe', current_user, request)
    flash(gettext("Unsubscribed :("))
    return redirect(url_for('genericBluePrint.general'))
