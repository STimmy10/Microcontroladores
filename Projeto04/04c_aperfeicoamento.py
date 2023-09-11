# importação de bibliotecas
from os import system
from subprocess import Popen
from time import sleep
from datetime import datetime, timedelta
from requests import post, get
from gpiozero import Button, LED, Buzzer, DistanceSensor
from mplayer import Player
from Adafruit_CharLCD import Adafruit_CharLCD
from urllib.request import urlretrieve


# Mata todos os aplicativos "mplayer" e "arecord"
system("killall mplayer")
system("killall arecord")

#Outros
global aplicativo
aplicativo = None
proximo_id_de_update = 0
global aproximacao
aproximacao = 0


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

def chegouAlguem():
    global aproximacao
    aproximacao = datetime.now()
    print("Alguem na porta")

def alguemAi():
    global aproximacao
    print("alguem saiu da frente da porta")
    intervalo = datetime.now() - aproximacao
    if intervalo.total_seconds() > 10:
        manda_mensagem("Pessoa saiu")
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

def comeca_gravar():
    global aplicativo
    gravacao = ["arecord", "--duration", "30", "chegou.wav"]
    aplicativo = Popen(gravacao)
    return
    
def para_gravar():
    global aplicativo
    if aplicativo != None:
        aplicativo.terminate()
        aplicativo = None
    system("opusenc chegou.wav chegou.ogg")
    endereco = endereco_base + "/sendVoice"
    dados = {"chat_id": id_da_conversa}
    arquivo = {"voice": open("chegou.ogg", "rb")}
    resposta = post(endereco, data = dados, files = arquivo)
    return

def recebi_arquivo(id_do_arquivo, tipo):
    endereco = endereco_base + "/getFile"
    dados = {"file_id": id_do_arquivo}
    resposta = get(endereco, json = dados)
    dicionario = resposta.json()
    final_do_link = dicionario["result"]["file_path"]
    link_do_arquivo = "https://api.telegram.org/file/bot" + chave + "/" + final_do_link
    if tipo == "audio":
        arquivo_de_destino = "recebido.ogg"
        urlretrieve(link_do_arquivo, arquivo_de_destino)
    elif tipo == "imagem":
        arquivo_de_destino = "recebido.jpg"
        urlretrieve(link_do_arquivo, arquivo_de_destino)
    return
        

# criação de componentes
lcd = Adafruit_CharLCD(2, 3, 4, 5, 6, 7, 16, 2)
botao1 = Button(11)
botao2 = Button(12)
botao3 = Button(13)
buzzer = Buzzer(16)
led1 = LED(21)
sensor = DistanceSensor(trigger=17, echo=18)
player = Player()


botao1.when_pressed = comeca_campainha
botao1.when_released = para_campainha
botao2.when_pressed = fecha_porta
botao3.when_pressed = comeca_gravar
botao3.when_released = para_gravar

sensor.when_in_range = chegouAlguem
sensor.when_out_of_range = alguemAi

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
            recebi_arquivo(id_do_arquivo, "audio")
            player.loadfile("recebido.ogg")
    # depois baixa o arquivo e faz algo com ele...
        elif "photo" in mensagem: 
            foto_mais_resolucao = mensagem["photo"][-1] 
            id_do_arquivo = foto_mais_resolucao["file_id"]
            recebi_arquivo(id_do_arquivo, "imagem")
    # depois baixa o arquivo e faz algo com ele...
        proximo_id_de_update = resultado["update_id"] + 1
    sleep(0.2)
# COMECE COPIANDO AQUI O SEU CÓDIGO DA IMPLEMENTAÇÃO
# DEPOIS FAÇA OS NOVOS RECURSOS