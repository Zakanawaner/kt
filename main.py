from flask import Flask, request, render_template, url_for, redirect
from utils import *
from database import db
import json
import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


@app.route("/gamedata", methods={"GET", "POST"})
def data():
    createDatabase(db)
    handleGameData(json.loads(request.data.decode()), db)
    return {'status': 'ok'}, 200


@app.route("/games", methods={"GET", "POST"})
def games():
    gms = getGames()
    return render_template('games.html', title="Games", games=gms)


@app.route("/players", methods={"GET", "POST"})
def players():
    pls = getPlayers()
    return render_template('players.html', title="Players", players=pls)


@app.route("/factions", methods={"GET", "POST"})
def factions():
    fct = getFactions()
    return render_template('factions.html', title="Factions", factions=fct)


@app.route("/update", methods={"GET", "POST"})
def update():
    updateFactions(db)
    updateMissions(db)
    return redirect(url_for('general'))


@app.route("/faction/<fact>", methods={"GET", "POST"})
def faction(fact):
    fct = getFaction(fact)
    return render_template('faction.html', title=fct['sql'].name, faction=fct)


@app.route("/missions", methods={"GET", "POST"})
def missions():
    mss = getMissions()
    return render_template('missions.html', title="Missions", missions=mss)


@app.route("/mission/<ms>", methods={"GET", "POST"})
def mission(ms):
    mss = getMission(ms)
    return render_template('mission.html', title=mss['sql'].name, mission=mss)


@app.route("/randomize", methods={"GET", "POST"})
def randomize():
    createDatabase(db)
    if os.path.exists('database.sqlite'):
        os.remove('database.sqlite')
    randomize_data(db)
    return redirect(url_for('update'))


@app.route("/", methods={"GET", "POST"})
def general():
    createDatabase(db)
    gen = getGeneral()
    return render_template('general.html', title="General", gen=gen)


if __name__ == '__main__':
    app.run()
