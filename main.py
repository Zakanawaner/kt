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
#  - Controlar que solo se añadan bichos con comand node en la estructura del juego
#  - Si da tiempo, guardar tirdas por jugador?

# TODO WEB
#  - Mirar bien los mail y el estilo y tal

# TODO Future
#  - Posibilidad de añadir manualmente partidas
#  - Añadir torneos a mano
#  - Implementar tiers y ventajas por tier
#  - Número de bichos muertos por player
#  - Numero total de bichos muertos
#  - Añadir auto publicaciones de twitter (e Insta?)
#  - Hacer un Discord
#  - Hacer un sistema de subscripción a tornemos
#  - Integrar en css version movil
#  - Eventualmente pasar a react...?
#  - Hacer un generador de cartas
