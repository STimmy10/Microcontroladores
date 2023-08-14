from turtle import *

def retangulo(x, y, lado, colado):
    penup()
    goto(x - lado/2, y + colado/2)
    pendown()
    setheading(0)
    forward(lado)
    right(90)
    forward(colado)
    right(90)
    forward(lado)
    right(90)
    forward(colado)
    
def triangulo(x, y, lado):
    penup()
    goto(x, y)
    setheading(60)
    pendown()
    forward(lado)
    right(120)
    forward(lado)
    right(120)
    forward(lado)
    
def circulo(x, y, raio):
    penup()
    goto(x, y)
    pendown()
    circle(raio)
    
def espiral(x, y, voltas):
    penup()
    goto(x, y)
    pendown()
    crescimento = 0
    while crescimento <= voltas*5:    
        circle(3 * crescimento, 60)
        crescimento+=1
    
def cliqueTela(x, y):
    penup()
    goto(x, y)
    texto = "x = " + str(x) +  ", y = " + str(y)
    write(texto)
    
# Desenhe o que foi solicitado no enunciado do PDF aqui embaixo
retangulo(0, 200, 100, 50)
triangulo(160, -52, 80)
circulo(0, -200, 45)
espiral(-160, -52, 4)
onscreenclick(cliqueTela)






# Mantém a janela do Turtle aberta
mainloop()
