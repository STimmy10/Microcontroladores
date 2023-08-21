# COMECE COPIANDO AQUI O SEU CÓDIGO DO APERFEIÇOAMENTO

# COMECE COPIANDO AQUI O SEU CÓDIGO DA IMPLEMENTAÇÃO

# importação de bibliotecas
from os import system
from time import sleep
from gpiozero import LED, Button
from mplayer import Player
from Adafruit_CharLCD import Adafruit_CharLCD
import random
lcd = Adafruit_CharLCD(2, 3, 4, 5, 6, 7, 16, 2)



# para de tocar músicas que tenham ficado tocando da vez passada
system("killall mplayer")

player = Player()
# definição de funções
def pause():
    print('troca pause')
    player.pause()
    if (player.paused == False):
        led1.on()
    else:
        led1.off()
        led1.blink(on_time = 0.3, off_time = 0.3)
    return

def voltar_faixa():
    lcd.message(titulo[0:15])
    tempo = player.time_pos
    if (tempo <= 2):
        player.pt_step(-1)
        if (player.paused):
            pause()
    else:
        player.time_pos = 0
        if (player.paused):
            pause()
    return

def pular_faixa():
    lcd.message(titulo[0:15])
    if (player.speed == 2):
        player.speed = 1
    else:
        player.pt_step(1)
        if (player.paused):
            pause()
            
    return

def aumenta_velocidade():
    player.speed = 2
    return

# criação de componentes
arquivoEntrada = open("playlist.txt", "r")
lista = []
arquivoSaida = open("random.txt","w")
for linha in arquivoEntrada:
    lista.append(linha)
    
random.shuffle(lista)
for musica in lista:
    arquivoSaida.write(musica)

arquivoEntrada.close()
arquivoSaida.close()

player.loadlist("random.txt")
botao1 = Button(11)
botao2 = Button(12)
botao3 = Button(13)
led1 = LED(21)
led1.on()

botao1.when_pressed = voltar_faixa
botao2.when_pressed = pause
botao3.when_held = aumenta_velocidade
botao3.when_released = pular_faixa

inicio = 0
fim = 15

# loop infinito
while True:
    lcd.clear()
    
    metadados = player.metadata
    if metadados != None:
        titulo = str(metadados["Title"])

    tam = len(titulo)
    
    posicao = player.time_pos        
    if player.length != None:
        tempo_total = player.length
        minutos_total = tempo_total//60
        segundos_total = tempo_total % 60
    
    lcd.message(titulo[inicio:fim])
    if(fim < tam):
        inicio += 1
        fim += 1
    else:
        inicio = 0
        fim = 15
    
    if posicao != None:
        minutos = posicao // 60
        segundos = posicao % 60
        lcd.message("\n%02d:%02d  de  %02d:%02d "%(minutos, segundos, minutos_total, segundos_total))
        

    sleep(1)



# DEPOIS FAÇA OS NOVOS RECURSOS

