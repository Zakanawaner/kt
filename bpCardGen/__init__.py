from flask import Blueprint, current_app, flash, redirect, url_for, render_template, request
from flask_login import login_required, current_user

from utils.log import logAccess

cardGenBP = Blueprint('cardGeneratorBluePrint', __name__)


@cardGenBP.route("/cards", methods={"GET", "POST"})
@login_required
def cards():
    logAccess('/cards', current_user, request)
    cardGen = current_app.config["cardGenerator"]
    cardGen.addCard("ff", tit="hola", ab1="que tal", ab2="bien y tu?")
    return render_template("cardGenerator.html", cards=cardGen.html)
