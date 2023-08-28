# importação de bibliotecas
from gpiozero import LED, Button
from time import sleep
from lirc import init, nextcode
from Adafruit_CharLCD import Adafruit_CharLCD

lcd = Adafruit_CharLCD(2, 3, 4, 5, 6, 7, 16, 2) 
receptor = init("aula", blocking=False)

# definição de funções
def acenderTodos():
    for led in leds:
        led.on()
    return
        
def apagarTodos():
    for led in leds:
        led.off()
    return

def teclaNumero(x):
    lcd.clear()
    global ledSelecionado
    ledSelecionado = x
    lcd.message("LED %d\nselecionado"%ledSelecionado )
    return

def teclaOK():
    global ledSelecionado
    leds[ledSelecionado-1].toggle()
    return

def teclaUP():
    global ledSelecionado
    ledSelecionado = ledSelecionado + 1
    lcd.clear()
    if ledSelecionado > 5:
        ledSelecionado = 1
    lcd.message("LED %d\nselecionado"%ledSelecionado )
    return

def teclaDOWN():
    global ledSelecionado
    ledSelecionado = ledSelecionado - 1
    lcd.clear()
    if ledSelecionado < 1:
        ledSelecionado = 5
    lcd.message("LED %d\nselecionado"%ledSelecionado )
    return

# criação de componentes
leds = [LED(21), LED(22), LED(23), LED(24), LED(25)]
botao1 = Button(11)
botao2= Button(12)
lcd.clear()
global ledSelecionado
ledSelecionado = 1


botao1.when_pressed = acenderTodos
botao2.when_pressed = apagarTodos

# loop infinito
while True:
    lista_com_codigo = nextcode()
    if lista_com_codigo != []:
        codigo = lista_com_codigo[0]
        if codigo == "KEY_1":
            teclaNumero(1)
        elif codigo == "KEY_2":
            teclaNumero(2)
        elif codigo == "KEY_3":
            teclaNumero(3)
        elif codigo == "KEY_4":
            teclaNumero(4)
        elif codigo == "KEY_5":
            teclaNumero(5)
        elif codigo == "KEY_OK":
            teclaOK()
        elif codigo == "KEY_UP":
            teclaUP()
        elif codigo == "KEY_DOWN":
            teclaDOWN()
        else:
            print("Não conheço essa tecla")
    sleep(0.2)