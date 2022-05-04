from flask import Flask, request, render_template, url_for, redirect, make_response, flash, jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager, set_access_cookies, unset_jwt_cookies
from flask_login import LoginManager, login_user, login_required, logout_user
from utils import *
from database import db
from datetime import timedelta
import json

app = Flask(__name__)
app.config["SECRET_KEY"] = '8ed714601d86e030c1a5ffc941baf8b6'
app.config["JWT_SECRET_KEY"] = '8ed714601d86e030c1a5ffc941baf8b6'
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
loginManager = LoginManager(app)
app.config["loginManager"] = loginManager
jwt = JWTManager(app)
db.init_app(app)

# TODO adaptar nombre de facciones aquí quiándome del tts
# TODO añadir imágenes correspondientes
# TODO hacer subrutina de update
# TODO añadir en database los snapshots
# TODO hacer overwatch on TTS
# TODO pasarme a aws con mysql


@loginManager.user_loader
def loadUser(user_id):
    return getPlayerById(user_id)


@jwt.expired_token_loader
def refreshToken(jwt_header, jwt_data):
    response = make_response(redirect(url_for('login')))
    unset_jwt_cookies(response)
    return response


@app.route("/", methods={"GET", "POST"})
def general():
    createDatabase(db)
    gen = getGeneral()
    return render_template('general.html', title="General", user=current_user if not current_user.is_anonymous else None, gen=gen)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    createDatabase(db)
    if request.method == 'POST':
        status, new_user = userSignup(db, request.form)
        if status == 401:
            flash("Your password has tu have 8 characters, 1 uppercase and 1 digit")
            return redirect(url_for('signup'))
        if status == 402:
            flash("The username already exists")
            return redirect(url_for('signup'))
        if status == 200:
            response = redirect(url_for('general'))
            set_access_cookies(response, create_access_token(identity=new_user.publicId, expires_delta=timedelta(days=365)))
            login_user(new_user)
            flash("Registered successfully")
            return response
        if status == 403:
            flash("Password fields must coincide")
            return redirect(url_for('signup'))
    return render_template('signup.html', title="Signup")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        status, user = userLogin(request.form)
        if status == 200:
            flash("Login successful")
            response = redirect(url_for('general'))
            set_access_cookies(response, create_access_token(identity=user.publicId))
            login_user(user)
            return response
        if status == 401:
            flash("Could not verify")
            return make_response(render_template('login.html', title="Login"), 401,
                                 {'Authentication': '"login required"'})
    return render_template('login.html', title="Login")


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    response = redirect(url_for('general'))
    unset_jwt_cookies(response)
    logout_user()
    flash("Logout successfully")
    return response


@app.route("/randomize", methods={"GET", "POST"})
@login_required
@only_admin
def randomize():
    createDatabase(db)
    # if os.path.exists('database.sqlite'):
    #    os.remove('database.sqlite')
    #    pass
    randomize_data(db)
    return redirect(url_for('update'))


@app.route("/update", methods={"GET", "POST"})
@login_required
@only_admin
def update():
    updateFactions(db)
    updateMissions(db)
    updateSecondaries(db)
    updatePlayers(db)
    return redirect(url_for('general'))


@app.route("/addupdate", methods={"GET", "POST"})
@login_required
@only_admin
def addUpdate():
    if request.method == 'POST':
        addNewUpdate(db, request.form)
        return redirect(url_for('update'))
    fct = Faction.query.all()
    return render_template('addupdate.html', title="Update", user=current_user if not current_user.is_anonymous else None, factions=fct)


@app.route("/gamedata", methods={"GET", "POST"})
def data():
    createDatabase(db)
    handleGameData(json.loads(request.data.decode()), db)
    return {'status': 'ok'}, 200


@app.route("/games", methods={"GET", "POST"})
def games():
    gms = getGames()
    return render_template('games.html', title="Games", user=current_user if not current_user.is_anonymous else None, games=gms)


@app.route("/game/<gm>", methods={"GET", "POST"})
def game(gm):
    gm = getGame(gm)
    return render_template('game.html', title="Game", user=current_user if not current_user.is_anonymous else None, game=gm)


@app.route("/players", methods={"GET", "POST"})
def players():
    pls = getPlayers()
    return render_template('players.html', title="Players", user=current_user if not current_user.is_anonymous else None, players=pls)


@app.route("/player/<pl>", methods={"GET", "POST"})
def player(pl):
    pl = getPlayer(pl)
    if pl['sql'] == current_user:
        return render_template('profile.html', title=pl['sql'].username, user=current_user, player=pl)
    if not pl['sql'].allowSharing:
        flash("Player hidden")
        return redirect(url_for('general'))
    return render_template('player.html', title=pl['sql'].username, user=current_user if not current_user.is_anonymous else None, player=pl)


@app.route("/factions", methods={"GET", "POST"})
def factions():
    fct = getFactions()
    return render_template('factions.html', title="Factions", user=current_user if not current_user.is_anonymous else None, factions=fct)


@app.route("/faction/<fact>", methods={"GET", "POST"})
def faction(fact):
    fct = getFaction(fact)
    return render_template('faction.html', title=fct['sql'].name, user=current_user if not current_user.is_anonymous else None, faction=fct)


@app.route("/missions", methods={"GET", "POST"})
def missions():
    mss = getMissions()
    return render_template('missions.html', title="Missions", user=current_user if not current_user.is_anonymous else None, missions=mss)


@app.route("/mission/<ms>", methods={"GET", "POST"})
def mission(ms):
    mss = getMission(ms)
    return render_template('mission.html', title=mss['sql'].name, user=current_user if not current_user.is_anonymous else None, mission=mss)


@app.route("/secondaries", methods={"GET", "POST"})
def secondaries():
    scs = getSecondaries()
    return render_template('secondaries.html', title="Secondaries", user=current_user if not current_user.is_anonymous else None, secondaries=scs)


@app.route("/secondary/<sc>", methods={"GET", "POST"})
def secondary(sc):
    sc = getSecondary(sc)
    return render_template('secondary.html', title=sc['sql'].name, user=current_user if not current_user.is_anonymous else None, secondary=sc)


@app.route("/link/<opt>", methods={"GET", "POST"})
def link(opt):
    if opt == "stop":
        pl = Player.query.filter_by(id=current_user.id).first()
        pl.steamId = 0
        pl.steamLink = False
        db.session.add(pl)
    elif opt == "start":
        if request.method == "POST":
            form = json.loads(request.data.decode())
            pl = Player.query.filter_by(publicId=form['code']).first()
            if pl:
                if not pl.steamLink:
                    pl.steamId = form['name']
                    pl.steamLink = True
                    db.session.add(pl)
                    db.session.commit()
                    updatePlayer(db, pl.id)
                    return make_response(jsonify({'result': "Everything good"}), 200)
                else:
                    return make_response(jsonify({'result': "Already linked"}), 200)
            else:
                return make_response(jsonify({'result': "Something went wrong"}), 200)
        else:  # TODO to delete
            pl = Player.query.filter_by(username='Zakanawaner').first()
            pl.steamId = 1003
            pl.steamLink = True
            db.session.add(pl)
            db.session.commit()
            updatePlayer(db, pl.id)
    db.session.commit()
    flash("Link successfully updated")
    return redirect(url_for('general'))


@app.route("/allowance/<opt>", methods={"GET", "POST"})
@jwt_required()
@login_required
def allowance(opt):
    pl = Player.query.filter_by(publicId=get_jwt_identity()).first()
    if opt == "stop":
        pl.allowSharing = False
    elif opt == "start":
        pl.allowSharing = True
    db.session.add(pl)
    db.session.commit()
    updatePlayer(db, pl.id)
    flash("Selection successfully updated")
    return redirect(url_for('general'))


@app.route("/delete", methods={"GET", "POST"})
@jwt_required()
@login_required
def delete():
    response = redirect(url_for('general'))
    unset_jwt_cookies(response)
    logout_user()
    flash("Deletion successful")
    Player.query.filter_by(publicId=get_jwt_identity()).delete()
    db.session.commit()
    # TODO hacer la cascada de eliminación en la db
    # TODO Actualizar games eliminando el id
    return response


if __name__ == '__main__':
    app.run(port=3000)
