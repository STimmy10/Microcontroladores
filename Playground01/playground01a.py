# Neste Playground 01A, vamos trabalhar com LEDs, botões e LCDs.
# Veja os códigos de exemplo e programe o que está sendo soliticado em LETRAS MAIÚSCULAS.


# Como estamos longe do laboratório, usaremos um simulador gráfico para representar os componentes.
# Para controlar o hardware simulado, basta colocar todo o código dentro da função main abaixo.
# Os comandos são os mesmos da teoria, só que dentro da main.
from extra.playground import rodar

@rodar
def main():
    
    # Começamos importando as bibliotecas – sim, dentro da função main!
    from gpiozero import LED, Button
    from Adafruit_CharLCD import Adafruit_CharLCD
    from time import sleep
    
        
    # Agora podemos iniciar os componente. Vamos começar com os LEDs.
    # O número de cada um se refere ao pino do Raspberry Pi onde ele está conectado.
    led1 = LED(21)
    led2 = LED(22)
    led3 = LED(23)
    led4 = LED(24)
    led5 = LED(25)
    
    # Por padrão, os LEDs começam apagados.
    # Mas posso mandar um LED se acender logo no começo do programa.
    # Rode o código e veja o resultado.
    led1.on()
    
    
    
    # ACENDA O LED 2.
    led2.on()
    
    
    
    # Também posso deixar um LED piscando continuamente.
    # Repare que só precisa chamar o comando uma vez.
    
    # DESCOMENTE A LINHA ABAIXO PARA VER O RESULTADO.
    
    led3.blink()
    
    
    
    # Por padrão, a blink acende durante 1 segundo e apaga durante 1 segundo.
    # Mas você pode mudar esses tempos, ou até pedir para só piscar algumas vezes.
    
    # DESCOMENTE A LINHA ABAIXO PARA VER O RESULTADO.
    
    led4.blink(n=3, on_time=2.0, off_time=2.0)
    
    
    
    # PISQUE O LED 5 RAPIDAMENTE 4 VEZES.
    led5.blink(n=4, on_time=0.2, off_time=0.2)
    
    
    
    # Agora vamos passar para os botões.
    # Assim como os LEDs, a gente inicializa especificando aos pinos onde estão conectados.
    botao1 = Button(11)
    botao2 = Button(12)
    botao3 = Button(13)
    botao4 = Button(14)
    
    
    # Para que o clique no botão faça alguma coisa, a gente primeiro cria uma função.
    # Dentro dela, coloque os comandos que serão executados.
    # Normalmente eu sugiro colocar as funções no começo do código, mas deixei aqui para ser mais didático.
    def acender_ultimos_leds():
        led4.on()
        led5.on()
        
    # Por fim, associe o when_pressed do botão ao nome da função.
    # Estamos passando uma refência da função (tipo um ponteiro), e não chamando ela.
    botao1.when_pressed = acender_ultimos_leds   # SEM PARÊNTESIS NO FINAL!
    
    
    
    # CRIE UMA FUNÇÃO QUE APAGUE OS LEDS 4 E 5, CHAMANDO A .off().
    # EM SEGUIDA, FAÇA O CLIQUE NO BOTÃO 2 CHAMAR ESSA FUNÇÃO.
    def apagar_os_ultimos_leds():
        led5.off()
        led4.off()
    
    botao2.when_pressed = apagar_os_ultimos_leda
    
    
    
    # Para terminar esta primeira parte do Playground, vamos para o display LCD.
    # A inicialização dele pede os seis pinos, o número de colunas e o número de linhas.
    lcd = Adafruit_CharLCD(2, 3, 4, 5, 6, 7, 16, 2)
    
    
    # Para escrever algo nele, é só chamar a função message.
    # ATENÇÃO: ao contrário da print, o parâmetro precisa sempre ser um texto!
    lcd.message("Playground")
    
    
    # Se chamarmos a message de novo, o texto é impresso ao lado do anterior.
    lcd.message(" 01")
    
    
    # O texto não quebra para a linha de baixo automaticamente.
    # Para escrever algo na linha de baixo, use o \n.
    lcd.message("\nRaspberry Pi")
    
        
    # CHAME A FUNÇÃO lcd.clear() PARA APAGAR O TEXTO INICIAL.
    # EM SEGUIDA, ESCREVA O SEU NOME NA LINHA DE CIMA E O SOBRENOME NA LINHA DE BAIXO.
    lcd.clear()
    lcd.message("Lucas")
    lcd.message("\nLucena")    
    
    
    # CRIE OUTROS COMPORTAMENTOS PARA OS DISPOSITIVOS! BRINQUE À VONTADE!
    # Sugestão 1: faça com que o botão 3 pisque 2 vezes os LEDs 4 e 5.
    # Sugestão 2: use o while True abaixo para ir aumentando um contador e mostrá-lo no LCD.
    def piscar_45():
        led4.blink(n=2, on_time=2.0, off_time=2.0)
        led5.blink(n=2, on_time=2.0, off_time=2.0)
    
    botao3.when_pressed = piscar_45

    
    
    # Este while True garante que o nosso código vai continuar rodando direto.
    while True:
        
        
        
        sleep(0.1)
        
        
    # Não escreva nenhum código depois do while True!
    # O loop infinito segura o programa, então nada aqui embaixo vai rodar.