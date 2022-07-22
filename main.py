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
from bpCardGen import cardGenBP
from bpI18n import i18nBP

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
app.register_blueprint(cardGenBP)
app.register_blueprint(i18nBP)

app = createApp(app)
createDatabase(app)


if __name__ == '__main__':
    app.run(host=app.config['HOST'], port=app.config['PORT'])

# TODO TTS:

# TODO WEB
#  - Meter equipos en la base de datos antes de salir publico
#  - Checkear desc de operativos
#  - Hacer el timeline de la partida como me mostró GoodPerson
#  - BackUp de la base de datos regularmente

# TODO Future
#  - Posibilidad de añadir manualmente partidas
#  - Hacer una página informativa de rangos
#  - Añadir torneos a mano
#  - Implementar tiers y ventajas por tier
#  - Número de bichos muertos por player
#  - Numero total de bichos muertos
#  - Integrar en css version movil
#  - Eventualmente pasar a react...?
#  - Hacer un generador de cartas -> En curso
#  - Web Scrapping de BCP para torneos
#  - Hacer sistema de tier list
#  - Hacer un mathhammer -> En curso
