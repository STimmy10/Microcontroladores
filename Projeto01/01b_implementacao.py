# importação de bibliotecas
from os import system
from time import sleep
from gpiozero import LED, Button
from mplayer import Player
from Adafruit_CharLCD import Adafruit_CharLCD
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
    player.pt_step(1)
    if (player.paused):
        pause()
    return

# criação de componentes

player.loadlist("playlist.txt")
botao1 = Button(11)
botao2 = Button(12)
botao3 = Button(13)
led1 = LED(21)
led1.on()

botao1.when_pressed = voltar_faixa
botao2.when_pressed = pause
botao3.when_pressed = pular_faixa



# loop infinito
while True:
    lcd.clear()
    metadados = player.metadata
    if metadados != None:
        lcd.message(str(metadados["Title"]))
        

    sleep(0.2)
