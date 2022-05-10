from functools import wraps

from flask_login import current_user


##############
# Decorators #
def only_admin(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.permissions >= 8:
            return func(*args, **kwargs)
    return decorated_view


def only_collaborator(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.permissions >= 7:
            return func(*args, **kwargs)
    return decorated_view


def only_tier6(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.permissions >= 6:
            return func(*args, **kwargs)
    return decorated_view


def only_tier5(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.permissions >= 5:
            return func(*args, **kwargs)
    return decorated_view


def only_tier4(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.permissions >= 4:
            return func(*args, **kwargs)
    return decorated_view


def only_tier3(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.permissions >= 3:
            return func(*args, **kwargs)
    return decorated_view


def only_tier2(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.permissions >= 2:
            return func(*args, **kwargs)
    return decorated_view


def only_tier1(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.permissions >= 1:
            return func(*args, **kwargs)
    return decorated_view
