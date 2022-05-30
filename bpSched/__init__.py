from flask import Blueprint, current_app, flash, redirect, url_for
from flask_apscheduler import APScheduler
from flask_login import login_required

from utils.decorators import only_admin
from utils.player import updatePlayers
from utils.faction import updateFactions
from utils.mission import updateMissions
from utils.secondary import updateSecondaries
from utils.mail import sendWeeklyMail


schedulerBP = Blueprint('schedulerBluePrint', __name__)

scheduler = APScheduler()
scheduler.api_enabled = True


@scheduler.task('interval', id='updateData', seconds=1800, misfire_grace_time=2000)
def updateData():
    with scheduler.app.app_context():
        updateFactions(current_app.config['database'])
        updateMissions(current_app.config['database'])
        updateSecondaries(current_app.config['database'])
        updatePlayers(current_app.config['database'])


@scheduler.task('cron', id='weeklyMail', week='*', day_of_week='sun')
def weeklyMail():
    with scheduler.app.app_context():
        games, factions = sendWeeklyMail()
        current_app.config['twitterClient'].weeklyTweet(games, factions)


@schedulerBP.route("/startroutines", methods={"GET", "POST"})
@login_required
@only_admin
def startRoutines():
    if scheduler.state == 0:
        scheduler.start()
    flash("Background routines started")
    return redirect(url_for('genericBluePrint.general'))


@schedulerBP.route("/stoproutines", methods={"GET", "POST"})
@login_required
@only_admin
def stopRoutines():
    if scheduler.state == 1:
        scheduler.shutdown()
    flash("Background routines stopped")
    return redirect(url_for('genericBluePrint.general'))
