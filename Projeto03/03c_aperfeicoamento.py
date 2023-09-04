# importação de bibliotecas
from gpiozero import LED, Button, Buzzer, DistanceSensor
from extra.redefinir_banco import redefinir_banco
from pymongo import MongoClient, DESCENDING
from Adafruit_CharLCD import Adafruit_CharLCD
from lirc import init, nextcode
from time import sleep
from datetime import datetime, timedelta

# a linha abaixo apaga todo o banco e reinsere os moradores
redefinir_banco()

# parâmetros iniciais do banco
cliente = MongoClient("localhost", 27017)
banco = cliente["projeto03"]
colecao = banco["moradores"]


# definição de funções
def validaAp(apt):
    doc = colecao.find_one({"apartamento":apt})
    if doc != None :
        return True
    return False

def retornaNome (numero, valor):
    if validaAp(numero):
        doc = colecao.find_one({"apartamento":numero})
        if valor == doc["senha"]:
            return doc["nome"]
    return False

def coletadados(texto):
    cod = ""
    lista_com_codigo = []
    while True:
        lcd.clear()
        lcd.message(texto+"\n "+len(cod)*"*")
        if lista_com_codigo != []:
             buzzer.beep(n=1, on_time = 0.2)
             codigo = lista_com_codigo[0]
             if codigo == "KEY_OK":
                 return cod
             else:
                 cod += (codigo[-1])
        lista_com_codigo = nextcode()
        sleep(0.2)
             
             
def on_range():
    apt = coletadados("Digite o apt:")
    if validaAp(apt):
        senha = coletadados("Digite a senha:")
        nome = retornaNome(apt, senha)
        horario = datetime.now()
        if nome != False:
            lcd.clear()
            lcd.message("Bem-Vindo(a)\n"+nome+"!")
            dados = {"apt": apt, "horario": horario, "nome": nome}
        else:
            lcd.clear()
            buzzer.beep(n=3, on_time = 0.1, off_time = 0.2)
            lcd.message("Senha invalida")
            dados = {"apt": apt, "horario": horario}
        distancias.insert(dados)
        sleep(2.5)
            
    else:
        lcd.clear()
        buzzer.beep(n=3, on_time = 0.1, off_time = 0.2)
        lcd.message("apt invalido")
        sleep(2.5)
        
    lcd.clear()
    
def mostra_tentativas():
    dado = coletadados("Entre com o apt:")
    print(dado)
    ordenacao = [ ["horario", DESCENDING] ]
    documentos = list( distancias.find({"apt":dado}, sort=ordenacao) )
    for el in documentos:
        texto = el["horario"].strftime("%d/%m (%H:%M)")
        
        if el.get("nome") != None:
            print(texto + " "+ el["nome"]+"\n")
        else:
            print(texto + " SENHA INCORRETA!\n")


# criação de componentes

lcd = Adafruit_CharLCD(2, 3, 4, 5, 6, 7, 16, 2)
buzzer = Buzzer(16)
button = Button(11)
sensor = DistanceSensor(trigger=17, echo=18)
sensor.threshold_distance = 0.1
sensor.when_in_range = on_range
button.when_pressed = mostra_tentativas
cliente = MongoClient("localhost", 27017)

banco = cliente["Acessos"]
distancias = banco["tentativas"]

# loop infinito
init("aula", blocking=False)

apt = ""
libera = False
senha =""
while True:
    
    
        
    
    sleep(0.2)

# COMECE COPIANDO AQUI O SEU CÓDIGO DA IMPLEMENTAÇÃO
# DEPOIS FAÇA OS NOVOS RECURSOS