from json import load
from turtle import *


# Copie as funções que você fez na Implementação aqui embaixo
def desenha_retangulo(x, y, comprimento, altura, cor):
    penup()
    goto(x, y)
    pendown()
    fillcolor(cor)
    begin_fill()
    setheading(0)
    forward(comprimento)
    right(90)
    forward(altura)
    right(90)
    forward(comprimento)
    right(90)
    forward(altura)
    end_fill()
    return
    
    
def desenha_circulo(x, y, raio, cor):
    penup()
    goto(x + raio, y)
    pendown()
    fillcolor(cor)
    begin_fill()
    circle(raio)
    end_fill()
    return
    
    
def desenha_poligono(lista_pontos, cor):
    fillcolor(cor)
    begin_fill()
    penup()
    contaPontos = 0
    goto(lista_pontos[contaPontos]["x"], lista_pontos[contaPontos]["y"])
    pendown()
    while contaPontos <= len(lista_pontos) - 1:
        goto(lista_pontos[contaPontos]["x"], lista_pontos[contaPontos]["y"])
        contaPontos+=1
    goto(lista_pontos[0]["x"], lista_pontos[0]["y"])
    end_fill()   
    return    


# Faça a primeira parte do Aperfeiçoamento aqui

def desenha_bandeira(dicionario_do_pais):
    listaElementos = dicionario_do_pais["elementos"]
    for elemento in listaElementos:
        if (elemento["tipo"]) == "retângulo":
            desenha_retangulo(elemento["x"], elemento["y"], elemento["comprimento"], elemento["altura"], elemento["cor"])
        elif (elemento["tipo"]) == "círculo":
            desenha_circulo(elemento["x"], elemento["y"], elemento["raio"], elemento["cor"])
        elif (elemento["tipo"]) == "polígono":
            desenha_poligono(elemento["pontos"], elemento["cor"])
    return
lista_de_paises = load(open('paises.json', encoding="UTF-8"))


# Faça a segunda parte do Aperfeiçoamento aqui
def onClick(x, y):
    penup()
    goto(x, y)
    pendown()
    pais = textinput("Digite o nome do país", "Pais")
    for element in lista_de_paises:
        if element["nome"] == pais:
            desenha_bandeira(element)
    return


onscreenclick(onClick)



# O desafio deve ser feito diretamente no JSON, não aqui!


# Mantém a janela do Turtle aberta
mainloop()