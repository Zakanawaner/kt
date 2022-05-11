import json

from flask import Blueprint, make_response, redirect, url_for, request, flash, render_template, current_app, jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager, set_access_cookies, unset_jwt_cookies
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from utils.player import getPlayerById, updatePlayer
from utils.auth import *
from utils.mail import unSubscribeUser
from datetime import timedelta


authBP = Blueprint('authBluePrint', __name__)

loginManager = LoginManager()
jwt = JWTManager()


@loginManager.user_loader
def loadUser(user_id):
    return getPlayerById(user_id)


@jwt.expired_token_loader
def refreshToken(jwt_header, jwt_data):
    response = make_response(redirect(url_for('authBluePrint.login')))
    unset_jwt_cookies(response)
    return response


@authBP.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        status, new_user = userSignup(current_app.config['database'], request.form)
        if status == 401:
            flash("Your password has tu have 8 characters, 1 uppercase and 1 digit")
            return redirect(url_for('authBluePrint.signup'))
        if status == 402:
            flash("The username already exists")
            return redirect(url_for('authBluePrint.signup'))
        if status == 200:
            response = redirect(url_for('genericBluePrint.general'))
            set_access_cookies(response, create_access_token(identity=new_user.publicId, expires_delta=timedelta(days=365)))
            response.set_cookie("preferred_update", "0")
            response.set_cookie("preferred_gameType", "0")
            login_user(new_user)
            flash("Registered successfully")
            return response
        if status == 403:
            flash("Password fields must coincide")
            return redirect(url_for('authBluePrint.signup'))
    return render_template('signup.html', title="Signup")


@authBP.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        status, user = userLogin(request.form)
        if status == 200:
            flash("Login successful")
            response = redirect(url_for('genericBluePrint.general'))
            set_access_cookies(response, create_access_token(identity=user.publicId))
            response.set_cookie("preferred_update", "0")
            response.set_cookie("preferred_gameType", "0")
            login_user(user)
            return response
        if status == 401:
            flash("Could not verify")
            return make_response(render_template('login.html', title="Login"), 401,
                                 {'Authentication': '"login required"'})
    return render_template('login.html', title="Login")


@authBP.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    response = redirect(url_for('genericBluePrint.general'))
    unset_jwt_cookies(response)
    logout_user()
    flash("Logout successfully")
    return response


@authBP.route("/link/<opt>", methods={"GET", "POST"})
def link(opt):
    if opt == "stop":
        pl = Player.query.filter_by(id=current_user.id).first()
        pl.steamId = 0
        pl.steamLink = False
        current_app.config['database'].session.add(pl)
    elif opt == "start":
        if request.method == "POST":
            form = json.loads(request.data.decode())
            pl = Player.query.filter_by(publicId=form['code']).first()
            if pl:
                if not pl.steamLink:
                    pl.steamId = form['steamId']
                    pl.steamLink = True
                    current_app.config['database'].session.add(pl)
                    current_app.config['database'].session.commit()
                    updatePlayer(current_app.config['database'], pl.id)
                    return make_response(jsonify({'result': "Everything good"}), 200)
                else:
                    return make_response(jsonify({'result': "Already linked"}), 200)
            else:
                return make_response(jsonify({'result': "Something went wrong"}), 200)
    current_app.config['database'].session.commit()
    flash("Link successfully updated")
    return redirect(url_for('genericBluePrint.general'))


@authBP.route("/allowance/<opt>", methods={"GET", "POST"})
@jwt_required()
@login_required
def allowance(opt):
    pl = Player.query.filter_by(publicId=get_jwt_identity()).first()
    if opt == "stop":
        pl.allowSharing = False
        unSubscribeUser(pl)
    elif opt == "start":
        pl.allowSharing = True
    current_app.config['database'].session.add(pl)
    current_app.config['database'].session.commit()
    updatePlayer(current_app.config['database'], pl.id)
    flash("Selection successfully updated")
    return redirect(url_for('genericBluePrint.general'))


@authBP.route("/delete", methods={"GET", "POST"})
@jwt_required()
@login_required
def delete():
    response = redirect(url_for('genericBluePrint.general'))
    unset_jwt_cookies(response)
    logout_user()
    flash("Deletion successful")
    pl = Player.query.filter_by(publicId=get_jwt_identity()).first()
    current_app.config['database'].session.delete(pl)
    current_app.config['database'].session.commit()
    return response
