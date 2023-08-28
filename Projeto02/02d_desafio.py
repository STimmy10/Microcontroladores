# importação de bibliotecas
from gpiozero import LED, Button
from time import sleep
from flask import Flask, render_template, redirect
from py_irsend.irsend import send_once
from threading import Timer
from json import load


# criação do servidor
app = Flask(__name__)
lista_canais = load(open("canais.json",encoding = "UTF-8"))

# definição de funções das páginas
@app.route("/")
def inicio():
    return render_template("index.html",lista = lista_canais)

@app.route("/mudo")
def mudo():
    send_once("aquario",["KEY_MUTE"])
    return redirect("/")

@app.route("/power")
def power():
    send_once("aquario", ["KEY_POWER"])
    return redirect("/")

@app.route("/volumeUP")
def aumentaVolume():
    send_once("aquario", ["KEY_VOLUMEUP"])
    return redirect("/")

@app.route("/volumeDOWN")
def diminuiVolume():
    send_once("aquario", ["KEY_VOLUMEDOWN"])
    return redirect("/")

@app.route("/canal/<string:x>")
def canal(x):
    for letra in x:
        send_once("aquario",["KEY_"+letra])
    send_once("aquario",["KEY_OK"])
    return redirect("/")

@app.route("/power/<int:N>")
def desligaN(N):
    Timer(N,power).start()
    return redirect("/")
# rode o servidor
app.run(port = 5000,debug = True)

# definição de funções

# criação de componentes

# loop infinito
while True:
    sleep(0.2)
