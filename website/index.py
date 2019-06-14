from flask import *
from random import randint
import grovepi
import time
import picamera
import threading
import io
from MaCamera import MaCamera
import RPi.GPIO as gpio



capteur_temp = 3 #D3
capteur_gas = 16 #A1

grovepi.pinMode(capteur_gas, "INPUT")

E1 = 21
E2 = 23
M1 = 22
M2 = 24

def init():
    gpio.setmode(gpio.BOARD)
    gpio.setup(E1,gpio.OUT)
    gpio.setup(E2,gpio.OUT)
    gpio.setup(M1,gpio.OUT)
    gpio.setup(M2,gpio.OUT)

def forward(tf):
    init()
    gpio.output(E1, True)
    gpio.output(E2, True)
    gpio.output(M1, True)
    gpio.output(M2, True)
    time.sleep(tf)
    gpio.output(E1, False)
    gpio.output(E2, False)
    gpio.cleanup()

def backward(tf):
    init()
    gpio.output(E1, True)
    gpio.output(E2, True)
    gpio.output(M1, False)
    gpio.output(M2, False)
    time.sleep(tf)
    gpio.output(E1, False)
    gpio.output(E2, False)
    gpio.cleanup()

def left(tf):
    init()
    gpio.output(E1, True)
    gpio.output(E2, True)
    gpio.output(M1, True)
    gpio.output(M2, False)
    time.sleep(tf)
    gpio.output(E1, False)
    gpio.output(E2, False)
    gpio.cleanup()

def right(tf):
    init()
    gpio.output(E1, True)
    gpio.output(E2, True)
    gpio.output(M1, False)
    gpio.output(M2, True)
    time.sleep(tf)
    gpio.output(E1, False)
    gpio.output(E2, False)
    gpio.cleanup()


def generateur(camera):
    """
    Cette fonction représente un générateur d'images
    Il utilise la fonction "get_image" de notre classe "MaCamera"
    """
    while True:
        img = camera.get_image()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n')

app = Flask(__name__)

@app.route('/image_url')
def image_url():
    """
    Route générant le flux d'images

    Doit être appelée depuis l'attribut "src" d'une balise "img"
    """
    return Response(generateur(MaCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')


# Page d'acceuil
@app.route('/')
def index():
    return render_template('index.html')

# Donees capteurs :
@app.route("/capteur/tempAndHum")
def tmpAndHum():
    [ temperature,humidity ] = grovepi.dht(capteur_temp, 0)
    return str(temperature) + "," + str(humidity)

@app.route("/capteur/gaz")
def gaz():
    global capteur_gas
    sensor_value = 0
    for i in range(3):
        sensor_value += grovepi.analogRead(capteur_gas)
    return str(sensor_value // 3)

@app.route("/jet")
def led():
    led = 2
    grovepi.pinMode(led, "OUTPUT")
    grovepi.digitalWrite(led,1)
    time.sleep(2)
    grovepi.digitalWrite(led,0)
    return "ok"

@app.route("/mouvement/<direction>")
def mouvement(direction):
    if direction == "avancer":
        forward()
    elif direction == "reculer":
        backward()
    elif direction == "droite":
        right()
    elif direction == "gauche":
        left()
    return direction


if __name__ == "__main__":
    app.run(debug=True, threaded=True, host="0.0.0.0", port="80")
    app.config.from_object('config')
