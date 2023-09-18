# importação de bibliotecas
from threading import Timer
from gpiozero import LED, MotionSensor, Button, LightSensor, DistanceSensor
from requests import post

# definição de funções
#Crie um timer recorrente que imprima "olá" a cada 2 segundos.
def imprimir_ola():
    print("olá!")
    timer = Timer(2, imprimir_ola)
    timer.start()
    
# Acenda o LED 2 ao detectar um movimento e apague-o somente se não houver movimento por 8 segundos
def movimento_detectado():
    global timer_led2
    led1.on()
    timer_led2.cancel()
    led2.on()
    
def inercia_detectada():
    global timer_led2
    led1.off()
    timer_led2 = Timer(8, led2.off)
    timer_led2.start()
    
    
def chamar_IFTTT():
    porcentagem = "%.2f" % (sensor_luz.value * 100)
    distancia = "%.2f" % (sensor_distancia.distance * 100)
    dados = {"value1": porcentagem, "value2": distancia}
    resultado = post(url, json=dados)
    print(resultado.text)

# criação de componentes
chave = "itAFKrcDTsfZW5u8sZHrMKKIXuEMBnRiUY4tk-2nMDU"
url = "https://maker.ifttt.com/trigger/docs_event/with/key/" + chave

led1 = LED(21)
led2 = LED(22)

botao1 = Button(11)
botao1.when_pressed = chamar_IFTTT

timer_led2 = Timer(8, led2.off)

# Acenda o LED 1 ao detectar um movimento, e apague-o ao detectar a inércia
sensor = MotionSensor(27)
sensor_luz = LightSensor(8)
sensor_distancia = DistanceSensor(trigger=17, echo=18)

sensor.when_motion = movimento_detectado
sensor.when_no_motion = inercia_detectada

timer = Timer(2, imprimir_ola)
timer.start()
# loop infinito
