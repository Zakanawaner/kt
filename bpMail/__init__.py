from flask import Blueprint, request, flash, redirect, url_for
from flask_mail import Mail
from flask_login import login_required, current_user

from utils.mail import subscribeUser, unSubscribeUser

mailBP = Blueprint('mailBlueprint', __name__)

mailManager = Mail()


@mailBP.route("/subscribe", methods=['POST'])
@login_required
def subscribe():
    if subscribeUser(current_user, request.form):
        flash("Subscribed! Check your email")
        return redirect(url_for('genericBluePrint.general'))
    flash("That's not a correct mail address")
    return redirect(url_for('playerBluePrint.player', pl=current_user.id))


@mailBP.route("/unsubscribe", methods=['POST'])
@login_required
def unSubscribe():
    unSubscribeUser(current_user)
    flash("Unsubscribed :(")
    return redirect(url_for('genericBluePrint.general'))
