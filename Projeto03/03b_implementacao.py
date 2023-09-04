# importação de bibliotecas
from extra.redefinir_banco import redefinir_banco
from pymongo import MongoClient
from Adafruit_CharLCD import Adafruit_CharLCD
from lirc import init, nextcode
from time import sleep
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
             codigo = lista_com_codigo[0]
             if codigo == "KEY_OK":
                 return cod
             else:
                 cod += (codigo[-1])
        lista_com_codigo = nextcode()
        sleep(0.2)
             
             
             

# criação de componentes

lcd = Adafruit_CharLCD(2, 3, 4, 5, 6, 7, 16, 2)


# loop infinito
init("aula", blocking=False)

apt = ""
libera = False
senha =""
while True:
    apt = coletadados("Digite o apt:")
    if validaAp(apt):
        senha = coletadados("Digite a senha:")
        nome = retornaNome(apt, senha)
        if nome != False:
            lcd.clear()
            lcd.message("Bem-Vindo(a)\n"+nome+"!")
            sleep(2.5)
        else:
            lcd.clear()
            lcd.message("Senha invalida")
            sleep(2.5)
    else:
        lcd.clear()
        lcd.message("apt invalido")
        sleep(2.5)
    
    
        
    
    sleep(0.2)
