import uuid

from database import Player, Rank
from password_strength import PasswordPolicy
from werkzeug.security import generate_password_hash, check_password_hash


########
# Auth #
def userSignup(db, form):
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
        new_user = Player(
            publicId=str(uuid.uuid4()),
            username=form['username'],
            password=hashed_password,
            shortName=form['username'].lower().replace(" ", ""),
            permissions=8 if form['username'] == 'Zakanawaner' else 0,
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


def userLogin(form):
    user = Player.query.filter_by(username=form['username']).first()
    if user:
        if check_password_hash(user.password, form['password']):
            return 200, user
    return 401, None

