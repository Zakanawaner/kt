from database import Operative


def getOperatives():
    return Operative.query.all()
