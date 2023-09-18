# importação de bibliotecas
from gpiozero import LED, Button
from pymongo import MongoClient, ASCENDING, DESCENDING
from datetime import datetime, timedelta
from flask import Flask
from gpiozero import LED, MotionSensor, Button, LightSensor, DistanceSensor
from threading import Timer
from requests import post

chave = "itAFKrcDTsfZW5u8sZHrMKKIXuEMBnRiUY4tk-2nMDU"
url = "https://maker.ifttt.com/trigger/tempo_leds/with/key/" + chave

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

def calcula_aceso(indice, inicio):
    busca = {"data": {"$gt": inicio}}
    ordenacao = [ ["data", DESCENDING] ]
    documentos = list( colecao.find(busca, sort=ordenacao))
    data_anterior = datetime.now()
    tempo_aceso = 0
    for dicionario in documentos:
        data = dicionario["data"]
        if dicionario["estados_dos_leds"][indice-1] == True:
            deltatime = data_anterior - data
            tempo_aceso += deltatime.total_seconds()
        data_anterior = data
    busca = {"data": {"$lt": inicio}}
    caso_especial = colecao.find_one(busca, sort=ordenacao)
    if caso_especial != None and caso_especial["estados_dos_leds"][indice-1] == True:
        deltatime = data_anterior - inicio
        tempo_aceso+= deltatime.total_seconds()
    return tempo_aceso


def tempo_leds():
    comeco = timedelta(minutes = 1)
    comeco = datetime.now() - comeco
    tempo_led1 = calcula_aceso(1, comeco)
    tempo_led2 = calcula_aceso(2, comeco)
    tempo_led3 = calcula_aceso(3, comeco)
    tempo_led4 = calcula_aceso(4, comeco)
    tempo_led5 = calcula_aceso(5, comeco)
    texto = comeco.strftime("%d/%m/%Y at %H:%M")
    final = texto + "|||" + str(tempo_led1) + "|||" + str(tempo_led2) + "|||" + str(tempo_led3) + "|||" + str(tempo_led4) + "|||" + str(tempo_led5)
    #dados = {"value1": texto, "value2": tempo_led1, "value3": tempo_led2, "value4": tempo_led3, "value5": tempo_led4, "value6": tempo_led5}
    dados = {"value1" : final}
    resultado = post(url, json=dados)
    print(resultado)
    trinta_segundos()
    
def trinta_segundos():
    timer = Timer(30, tempo_leds)
    timer.start()

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
    for index in range(len(estados)):
        atualiza_led(index + 1, estados[index])

ordenacao = [ ["data", DESCENDING] ]
documentos = list( colecao.find({}, sort=ordenacao) )
segundos = calcula_aceso(3, documentos[20]["data"])

tempo_leds()
# rode o servidor
app.run(port=5000, debug=False)
