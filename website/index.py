from flask import *
from random import randint

app = Flask(__name__)

# Page d'acceuil
@app.route('/')
def index():
    return render_template('index.html')

# Donées capteurs :
@app.route("/capteur/tempAndHum")
def tmpAndHum():
    temperature = 0
    humidity = 0

    for i in range(5):
        temperature += randint(0,50)
        humidity += randint(0,100)

    temperature = temperature // 5
    humidity = humidity // 5
    return str(temperature) + "," + str(humidity)

@app.route("/capteur/gaz")
def gaz():
    gaz = 0
    for i in range(5):
        gaz += randint(0,1000)
    gaz = gaz // 5
    return str(gaz)


@app.route("/mouvement/<direction>")
def mouvement(direction):
    return direction


if __name__ == "__main__":
    app.run(debug=True, threaded=True)
    app.config.from_object('config')
