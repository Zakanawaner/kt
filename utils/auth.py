import random

from database import Player, Rank
from password_strength import PasswordPolicy
from werkzeug.security import generate_password_hash, check_password_hash


########
# Auth #
def userSignup(db, form):
    if form['username'].isalnum():
        if form['password'] == form['password1']:
            policy = PasswordPolicy.from_names(
                length=8,
                uppercase=1,
                numbers=1
            )
            if policy.test(form['password']):
                return 401, None
            hashed_password = generate_password_hash(form['password'], method='sha256')
            if Player.query.filter_by(username=form['username']).first():
                return 402, None
            ok = False
            while not ok:
                publicId = random.randint(0, 2147483647)
                if not Player.query.filter_by(publicId=publicId).first():
                    ok = True
            new_user = Player(
                publicId=publicId,
                username=form['username'],
                password=hashed_password,
                shortName=form['username'].lower().replace(" ", ""),
                permissions=15 if form['username'] == 'Zakanawaner' else 0,
                steamLink=False,
                allowSharing=True,
                rank=[Rank.query.filter(Rank.score <= 0).first()],
                score=0,
                wins=0,
                ties=0,
                loses=0
            )
            db.session.add(new_user)
            db.session.commit()
            return 200, new_user
        else:
            return 403, None
    return 405, None


def userLogin(form):
    if form['username'].isalnum():
        user = Player.query.filter_by(username=form['username']).first()
        if user:
            if check_password_hash(user.password, form['password']):
                return 200, user
    return 401, None

