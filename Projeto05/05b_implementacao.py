# importação de bibliotecas
from gpiozero import LED, Button
from pymongo import MongoClient, ASCENDING, DESCENDING
from datetime import datetime, timedelta
from flask import Flask


# criação do servidor


# definição de funções das páginas
def atualiza_led(indice, valor):
    global leds
    vetor_estados = []
    if valor == True:
        leds[indice-1].on()
    else:
        leds[indice-1].off()
    for element in leds:
        vetor_estados+= [element.is_lit]
    dados = {"data": datetime.now(), "estados_dos_leds": vetor_estados}
    colecao.insert(dados)

# criação dos componentes
global leds
leds = [LED(21), LED(22), LED(23), LED(24), LED(25)]
botoes = [Button(11), Button(12), Button(13), Button(14)]

cliente = MongoClient("localhost", 27017)
banco = cliente["estados"]
colecao= banco["leds"]

app = Flask(__name__)

@app.route("/")
def mostrar_inicio():
    return "Bem-vino!"

@app.route("/led/<int:indice>/<string:estado>")
def pagina_led(indice, estado):
    if estado == "on":
        atualiza_led(indice, True)
        return "Led " + str(indice) + " aceso"
    else:
        atualiza_led(indice, False)
        return "Led " + str(indice) + " apagado"
    return "ok"

atualiza_led(3, True)
app.run(port=5000, debug=True)

# rode o servidor
