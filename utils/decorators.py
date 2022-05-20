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


# Exclusive data
# Tournament data
# Operative data
# Personal data
# Manual adding
# Tournament adding
# Update
# Add update
# Change permissions
def only_right_hand(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.permissions >= 7:
            return func(*args, **kwargs)
    return decorated_view


# Exclusive data
# Tournament data
# Personal data
# Operative data
# Manual adding
# Tournament adding
# Update
# Add update
def only_left_hand(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.permissions >= 6:
            return func(*args, **kwargs)
    return decorated_view


# Exclusive data
# Tournament data
# Personal data
# Operative data
# Manual adding
# Tournament adding
# Add update
def only_collaborator(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.permissions >= 5:
            return func(*args, **kwargs)
    return decorated_view


# Exclusive data
# Tournament data
# Personal data
# Operative data
# Manual adding
def only_adamantium(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.permissions >= 4:
            return func(*args, **kwargs)
    return decorated_view


# Exclusive data
# Tournament data
# Personal data
# Operative data
def only_diamantite(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.permissions >= 3:
            return func(*args, **kwargs)
    return decorated_view


# Exclusive data
# Tournament data
# Personal data
def only_ceramite(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.permissions >= 2:
            return func(*args, **kwargs)
    return decorated_view


# Exclusive data
# Tournament data
def only_plasteel(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.permissions >= 1:
            return func(*args, **kwargs)
    return decorated_view
