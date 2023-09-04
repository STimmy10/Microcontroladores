# importação de bibliotecas
from gpiozero import LED, Button, Buzzer, DistanceSensor
from time import sleep
from Adafruit_CharLCD import Adafruit_CharLCD
from pymongo import MongoClient, ASCENDING, DESCENDING
from datetime import datetime, timedelta


# definição de funções
def campainha():
    buzzer.beep(n = 1, on_time = 0.5, off_time = 2)
    return

def isNear():
    led1.blink(n=2, on_time = 0.5, off_time = 0.5)
    return

def dist():
    distancia = sensor.distance *100
    lcd.clear()
    lcd.message("%.1f cm"%distancia)
    horario = datetime.now()
    #print("salvei")
    dados = {"distancia": distancia, "horario": horario}
    distancias.insert(dados)
    #print("Inseri")
    
    return

# criação de componentes
botao1 = Button(11)
botao2 = Button(12)
buzzer = Buzzer(16)
led1 = LED(21)
lcd = Adafruit_CharLCD(2, 3, 4, 5, 6, 7, 16, 2)
sensor = DistanceSensor(trigger=17, echo=18)

cliente = MongoClient("localhost", 27017)

banco = cliente["frutas"]
distancias = banco["frutas"]

botao1.when_pressed = campainha
botao2.when_pressed = dist
sensor.threshold_distance = 0.1
sensor.when_in_range = isNear
sensor.when_out_of_range = isNear

while True:
    sleep(0.2)