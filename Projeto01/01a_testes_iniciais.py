# importação de bibliotecas
from gpiozero import LED, Button
from time import sleep
from Adafruit_CharLCD import Adafruit_CharLCD
lcd = Adafruit_CharLCD(2, 3, 4, 5, 6, 7, 16, 2)

contagem = 0
lcd.message("0")
# definição de funções
def pisca3 ():
    
    global contagem
    contagem +=1
    
    led3.blink(n=4)
    lcd.clear()
    lcd.message(str(contagem))
    return

# criação de componentes
led1 = LED(21)
led2 = LED(22)
led3 = LED(23)
led5 = LED(25)

botao1 = Button(11)
botao2 = Button(12)
botao3 = Button(13)


led1.blink(on_time=1, off_time=3)
botao2.when_pressed = led2.toggle
botao3.when_pressed = pisca3



# loop infinito
while True:
    if (led1.is_lit and botao1.is_pressed):
        led5.on()
    else:
        led5.off()

    sleep(0.2)