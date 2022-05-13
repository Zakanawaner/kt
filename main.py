from flask import Flask
from utils import createApp, createDatabase

from bpAuth import authBP
from bpSched import schedulerBP
from bpGeneric import genericBP
from bpPlayer import playerBP
from bpMission import missionBP
from bpFaction import factionBP
from bpSec import secondaryBP
from bpGame import gameBP
from bpAdmin import adminBP
from bpMail import mailBP

app = Flask(__name__)

app.register_blueprint(authBP)
app.register_blueprint(schedulerBP)
app.register_blueprint(genericBP)
app.register_blueprint(playerBP)
app.register_blueprint(missionBP)
app.register_blueprint(factionBP)
app.register_blueprint(secondaryBP)
app.register_blueprint(gameBP)
app.register_blueprint(adminBP)
app.register_blueprint(mailBP)

app = createApp(app)
createDatabase(app)


if __name__ == '__main__':
    app.run(host=app.config['HOST'], port=app.config['PORT'])

# TODO TTS:
#  - Texto de inicio que diga abrir el check list

# TODO WEB
#  - Añadir algo de texto en about y tal
#  - Mirar bien los mail y el estilo y tal
#  - Comprobar player con gametype -> Player bien pero profile no...?????

# TODO Future
#  - Posibilidad de añadir manualmente partidas
#  - Implementar tiers y ventajas por tier
#  - Número de bichos muertos por player
#  - Numero total de bichos muertos
