from flask import Blueprint, request, redirect, url_for
from flask_babel import Babel


i18nBP = Blueprint('i18nBlueprint', __name__)
babel = Babel()


@babel.localeselector
def get_locale():
    return 'en' if 'preferred_language' not in request.cookies else request.cookies['preferred_language']


@i18nBP.route("/lang/<loc>", methods={"GET"})
def language(loc):
    response = redirect(request.referrer)
    response.set_cookie("preferred_language", loc)
    return response
