###############
# Math Hammer #
math_operative_melee = db.Table(
    'math_operative_melee',
    db.Column('mathoperative_id', db.Integer, db.ForeignKey('MathOperative.id'), primary_key=True, unique=False),
    db.Column('mathmelee_id', db.Integer, db.ForeignKey('MathMelee.id'), primary_key=True, unique=False)
)
math_operative_ranged = db.Table(
    'math_operative_ranged',
    db.Column('mathoperative_id', db.Integer, db.ForeignKey('MathOperative.id'), primary_key=True, unique=False),
    db.Column('mathranged_id', db.Integer, db.ForeignKey('MathRanged.id'), primary_key=True, unique=False)
)
math_operative_ability = db.Table(
    'math_operative_ability',
    db.Column('mathoperative_id', db.Integer, db.ForeignKey('MathOperative.id'), primary_key=True, unique=False),
    db.Column('mathability_id', db.Integer, db.ForeignKey('MathAbility.id'), primary_key=True, unique=False)
)
math_operative_action = db.Table(
    'math_operative_action',
    db.Column('mathoperative_id', db.Integer, db.ForeignKey('MathOperative.id'), primary_key=True, unique=False),
    db.Column('mathaction_id', db.Integer, db.ForeignKey('MathAction.id'), primary_key=True, unique=False)
)
math_operative_psychic = db.Table(
    'math_operative_psychic',
    db.Column('mathoperative_id', db.Integer, db.ForeignKey('MathOperative.id'), primary_key=True, unique=False),
    db.Column('mathpsychic_id', db.Integer, db.ForeignKey('MathPsychic.id'), primary_key=True, unique=False)
)
math_melee_ability = db.Table(
    'math_melee_ability',
    db.Column('mathmelee_id', db.Integer, db.ForeignKey('MathMelee.id'), primary_key=True, unique=False),
    db.Column('mathweaponability_id', db.Integer, db.ForeignKey('MathWeaponAbility.id'), primary_key=True, unique=False)
)
math_melee_critic = db.Table(
    'math_melee_critic',
    db.Column('mathmelee_id', db.Integer, db.ForeignKey('MathMelee.id'), primary_key=True, unique=False),
    db.Column('mathweaponability_id', db.Integer, db.ForeignKey('MathWeaponAbility.id'), primary_key=True, unique=False)
)
math_ranged_ability = db.Table(
    'math_ranged_ability',
    db.Column('mathranged_id', db.Integer, db.ForeignKey('MathRanged.id'), primary_key=True, unique=False),
    db.Column('mathweaponability_id', db.Integer, db.ForeignKey('MathWeaponAbility.id'), primary_key=True, unique=False)
)
math_ranged_critic = db.Table(
    'math_ranged_critic',
    db.Column('mathranged_id', db.Integer, db.ForeignKey('MathRanged.id'), primary_key=True, unique=False),
    db.Column('mathweaponability_id', db.Integer, db.ForeignKey('MathWeaponAbility.id'), primary_key=True, unique=False)
)


class MathOperative(db.Model):
    __bind_key__ = 'db_uri_2'
    __tablename__ = 'mathoperative'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    M = db.Column(db.Integer)
    APL = db.Column(db.Integer)
    GA = db.Column(db.Integer)
    DF = db.Column(db.Integer)
    SV = db.Column(db.Integer)
    W = db.Column(db.Integer)
    melee = db.relationship("MathMelee", secondary=math_operative_melee)
    ranged = db.relationship("MathRanged", secondary=math_operative_ranged)
    abilities = db.relationship("MathAbility", secondary=math_operative_ability)
    actions = db.relationship("MathAction", secondary=math_operative_action)
    keywords = db.Column(db.String(200))
    psychic = db.relationship("MathPsychic", secondary=math_operative_psychic)


class MathMelee(db.Model):
    __bind_key__ = 'db_uri_2'
    __tablename__ = 'mathmelee'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    A = db.Column(db.Integer)
    BS = db.Column(db.Integer)
    D = db.Column(db.Integer)
    DC = db.Column(db.Integer)
    SP = db.relationship("MathWeaponAbility", secondary=math_melee_ability)
    critic = db.relationship("MathWeaponAbility", secondary=math_melee_critic)
    typ = "⚔"


class MathRanged(db.Model):
    __bind_key__ = 'db_uri_2'
    __tablename__ = 'mathranged'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    A = db.Column(db.Integer)
    BS = db.Column(db.Integer)
    D = db.Column(db.Integer)
    DC = db.Column(db.Integer)
    SP = db.relationship("MathWeaponAbility", secondary=math_ranged_ability)
    critic = db.relationship("MathWeaponAbility", secondary=math_ranged_critic)
    typ = "⌖"


class MathAction(db.Model):
    __bind_key__ = 'db_uri_2'
    __tablename__ = 'mathaction'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    cost = db.Column(db.Integer)
    description = db.Column(db.String(1500))


class MathAbility(db.Model):
    __bind_key__ = 'db_uri_2'
    __tablename__ = 'mathability'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(1500))


class MathPsychic(db.Model):
    __bind_key__ = 'db_uri_2'
    __tablename__ = 'mathpsychic'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(1500))


class MathWeaponAbility(db.Model):
    __bind_key__ = 'db_uri_2'
    __tablename__ = 'mathweaponability'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(1500))


# TODO configurar clases de mathhammer