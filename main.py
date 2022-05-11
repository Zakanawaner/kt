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
#  - Asegurarme de que se manda gametype en lugar de tournament
#  - Overlap en scouting phase
#  - Añadir equipement chosen en checklist
#  - Cambiar el game type y añadir en algún sitio el torneo
#  - Cambiar el broadcast de final de game para ir al botón del medio en lugar del scoreboard
#  - Texto de inicio que diga abrir el check list
#  - Activated button when tabled
#  - Ver si puedo limpiar el texto que sale en tooltip de overwatch
#  - Hacer algo para evitar doble click en los botones de la máquina de estados

# TODO WEB
#  - Añadir algo de texto en about y tal
#  - Añadir el filtro de game type (hecho para games, pensar en algo para el resto)
#  - Darle una última vuelta a los sched
#  - Para admin, poder gestionar directamente la bd (opcional)
#  - Gestionar las configuraciones en aws y en local