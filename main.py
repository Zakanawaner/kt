from flask import Flask, request, render_template
from utils import *
from source.db.db import db
import json
import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.abspath('source/db/db.sqlite')
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


@app.route("/missions", methods={"GET", "POST"})
def missions():
    mss = getMissions()
    return render_template('missions.html', title="Missions", missions=mss)


@app.route("/randomize", methods={"GET", "POST"})
def randomize():
    os.remove(os.path.abspath('source/db/db.sqlite'))
    randomize_data(db)
    return {'status': 'ok'}, 200


@app.route("/", methods={"GET", "POST"})
def general():
    gen = getGeneral()
    return render_template('general.html', title="General", gen=gen)


app.run(port=3000)
