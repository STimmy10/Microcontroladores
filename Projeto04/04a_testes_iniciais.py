# importação de bibliotecas
from time import sleep
from requests import post, get
from gpiozero import Button, LED
from mplayer import Player
from Adafruit_CharLCD import Adafruit_CharLCD
from os import system


# parâmetros iniciais do Telegram
chave = "6616525750:AAEmtYEg5fVzijGhISQg5fQFiWCz_jDU2Pk"
id_da_conversa = "919056018"
endereco_base = "https://api.telegram.org/bot" + chave


# definição de funções
global aplicativo 
aplicativo = None
nome_foto = "0"


def gravando():
    lcd.message("Gravando...")
    system("arecord --duration 5 audio.wav")
    print("Audio gravado")
    lcd.clear()
    return
    
def fotos():
    i = 1
    
    print("tirando fotos")
    while i <= 5 :
        
        nome_foto = "foto_"+str(i)+".jpg"
        fotografar = "fswebcam " + nome_foto
        system(fotografar)
        led1.blink(n=1)
        sleep(2)
        i=i+1
    return

def mensagem(texto):
    endereco = endereco_base + "/sendMessage"
    dados = {"chat_id": id_da_conversa, "text": texto}
    resposta = post(endereco, json=dados)
    return

# criação de componentes
lcd = Adafruit_CharLCD(2, 3, 4, 5, 6, 7, 16, 2)
botao1 = Button(11)
botao2 = Button(12)
botao3 = Button(13)
led1 = LED(21)
botao1.when_pressed = gravando
botao2.when_pressed = fotos
botao3.when_pressed = mensagem


while True:
    sleep(0.2)
