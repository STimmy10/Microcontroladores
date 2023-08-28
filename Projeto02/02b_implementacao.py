# importação de bibliotecas
from gpiozero import LED, Button
from time import sleep
from flask import Flask
from py_irsend.irsend import send_once
from threading import Timer

# criação do servidor
app = Flask(__name__)

# definição de funções das páginas
@app.route("/")
def inicio():
    return "jhajdsh"

@app.route("/mudo")
def mudo():
    send_once("aquario",["KEY_MUTE"])
    return "MUDO"

@app.route("/power")
def power():
    send_once("aquario", ["KEY_POWER"])
    return "liga/desliga"

@app.route("/volumeUP")
def aumentaVolume():
    send_once("aquario", ["KEY_VOLUMEUP"])
    return "VolumeUP"

@app.route("/volumeDOWN")
def diminuiVolume():
    send_once("aquario", ["KEY_VOLUMEDOWN"])
    return "VolumeDOWN"

@app.route("/canal/<string:x>")
def canal(x):
    for letra in x:
        send_once("aquario",["KEY_"+letra])
    send_once("aquario",["KEY_OK"])
    return "canal"+x

@app.route("/power/<int:N>")
def desligaN(N):
    Timer(N,power).start()
    return "desligando em "+str(N)+" segundos"
# rode o servidor

app.run(port = 5000,debug=True)

# definição de funções

# criação de componentes


# loop infinito
while True:
    sleep(0.2)

