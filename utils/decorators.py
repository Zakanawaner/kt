from functools import wraps

from flask_login import current_user

####################
# TIER INFORMATION #
####################

# Plasteel #
############
#   Models killed (Global)
#   Tier list
#   Internal rank
#   Card generator
#   Tournament data

# Ceramite #
############
#   Models killed (Player)
#   MathHammer

# Diamantite #
##############
#   Operative data

# Adamantium #
##############
#   Manual game adding

# Collaborator #
###############
#   Tournament result adding
#   Add update

# Left hand #
#############
#   Update information

# Right hand #
##############
#   Change permissions


##############
# Decorators #
def only_admin(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.permissions >= 8:
            return func(*args, **kwargs)
    return decorated_view


def only_right_hand(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.permissions >= 7:
            return func(*args, **kwargs)
    return decorated_view


def only_left_hand(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.permissions >= 6:
            return func(*args, **kwargs)
    return decorated_view


def only_collaborator(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.permissions >= 5:
            return func(*args, **kwargs)
    return decorated_view


def only_adamantium(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.permissions >= 4:
            return func(*args, **kwargs)
    return decorated_view


def only_diamantite(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.permissions >= 3:
            return func(*args, **kwargs)
    return decorated_view


def only_ceramite(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.permissions >= 2:
            return func(*args, **kwargs)
    return decorated_view


def only_plasteel(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.permissions >= 1:
            return func(*args, **kwargs)
    return decorated_view
