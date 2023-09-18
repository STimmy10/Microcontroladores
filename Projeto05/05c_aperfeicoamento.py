# importação de bibliotecas
from gpiozero import LED, Button
from pymongo import MongoClient, ASCENDING, DESCENDING
from datetime import datetime, timedelta
from flask import Flask
from gpiozero import LED, MotionSensor, Button, LightSensor, DistanceSensor
from threading import Timer

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

def movimento_detectado():
    global timer_led1
    atualiza_led(1, True)
    timer_led1.cancel()
    
def inercia_detectada():
    global timer_led1
    timer_led1 = Timer(6, apaga_led1)
    timer_led1.start()

def apaga_led1():
    atualiza_led(1, False)

def acende_led2():
    atualiza_led(2, True)

def apaga_led2():
    atualiza_led(2, False)

# criação dos componentes
global leds
leds = [LED(21), LED(22), LED(23), LED(24), LED(25)]
botoes = [Button(11), Button(12), Button(13), Button(14)]
timer_led1 = Timer(6, apaga_led1)

sensor_movimento = MotionSensor(27)
sensor_movimento.when_motion = movimento_detectado
sensor_movimento.when_no_motion = inercia_detectada

sensor_luz = LightSensor(8)
sensor_luz.threshold = 0.6
sensor_luz.when_dark = acende_led2
sensor_luz.when_light = apaga_led2

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

@app.route("/estados")
def pagina_estados():
    estados = []
    for led in leds:
        estado = "Apagado"
        if led.is_lit:
            estado = "Aceso" 
        estados += [estado]
    html = '''
    <ul style=“list-style-type:square”>

    <li>LED 1: {estados[0]}</li>

    <li>LED 2: {estados[1]}</li>

    <li>LED 3: {estados[2]}</li>

    <li>LED 4: {estados[3]}</li>

    <li>LED 5: {estados[4]}</li>

    </ul>
    '''.format(estados = estados)
    return html

ordenacao = [ ["data", DESCENDING] ]
documentos = list( colecao.find({}, sort=ordenacao) )
estados = documentos[0]["estados_dos_leds"]
if estados != None:
    print(estados)
    for index in range(len(estados)):
        atualiza_led(index + 1, estados[index])

# rode o servidor
app.run(port=5000, debug=False)
