# importação de bibliotecas
from os import system
from time import sleep
from requests import post, get
from gpiozero import Button, LED, Buzzer
from mplayer import Player
from Adafruit_CharLCD import Adafruit_CharLCD
from urllib.request import urlretrieve


# Mata todos os aplicativos "mplayer" e "arecord"
system("killall mplayer")
system("killall arecord")
proximo_id_de_update = 0


# parâmetros iniciais do Telegram
chave = "6616525750:AAEmtYEg5fVzijGhISQg5fQFiWCz_jDU2Pk"
id_da_conversa = "919056018"
endereco_base = "https://api.telegram.org/bot" + chave


# definição de funções
def manda_mensagem(texto):
    endereco = endereco_base + "/sendMessage"
    dados = {"chat_id": id_da_conversa, "text": texto}
    print("mandei -"+texto)
    resposta = post(endereco, json=dados)
    return

def comeca_campainha():
    buzzer.on()
    return

def para_campainha():
    buzzer.off()
    manda_mensagem("Alguem na porta")
    fotografar = "fswebcam " + "visita.jpg"
    system(fotografar)
    endereco = endereco_base + "/sendPhoto"
    dados = {"chat_id": id_da_conversa}
    arquivo = {"photo": open("visita.jpg", "rb")}
    resposta = post(endereco, data= dados, files=arquivo)
    return

def fecha_porta():
    led1.off()
    return

# criação de componentes
lcd = Adafruit_CharLCD(2, 3, 4, 5, 6, 7, 16, 2)
botao1 = Button(11)
botao2 = Button(12)
botao3 = Button(13)
buzzer = Buzzer(16)
led1 = LED(21)

botao1.when_pressed = comeca_campainha
botao1.when_released = para_campainha
botao2.when_pressed = fecha_porta

# loop infinito
while True:
    endereco = endereco_base + "/getUpdates"
    dados = {"offset": proximo_id_de_update} 
    resposta = get(endereco, json=dados)
    dicionario_da_resposta = resposta.json() 
    for resultado in dicionario_da_resposta["result"]: 
        mensagem = resultado["message"] 
        if "text" in mensagem: 
            texto = mensagem["text"]
            if texto == "Soar alarme":
                print("soando alarme")
                buzzer.beep(n=8, on_time = 0.3, off_time = 0.5)
            elif texto == "Abrir":
                led1.on()
        elif "voice" in mensagem: 
            id_do_arquivo = mensagem["voice"]["file_id"] 
    # depois baixa o arquivo e faz algo com ele...
        elif "photo" in mensagem: 
            foto_mais_resolucao = mensagem["photo"][-1] 
            id_do_arquivo = foto_mais_resolucao["file_id"] 
    # depois baixa o arquivo e faz algo com ele...
        proximo_id_de_update = resultado["update_id"] + 1
    sleep(0.2)