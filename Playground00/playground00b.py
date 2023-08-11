# Neste Playground 00 B, vamos trabalhar com controles de fluxo no código.
# Veja os códigos de exemplo e programe o que está sendo soliticado em LETRAS MAIÚSCULAS.


# Vamos pedir para o usuário (no caso, você mesmo) digitar um número ali embaixo no Shell.
numero = int( input("Digite um número inteiro e aperte Enter: ") )


# Podemos executar comandos diferentes dependendo do número digitado.
# Para isso, podemos usar o if com alguma comparação.
# Lembre-se que Python usa a indentação em vez de chaves para definir o conteúdo dos blocos.
# ATENÇÃO: não esqueça do dois pontos no final!
if numero >= 10:
    print("O número digitado é maior ou igual a 10.")
 
 
# Eu posso testar encadear várias verificações com if/elif/else
if numero > 0:
    print("O número digitado é positivo.")
elif numero < 0:
    print("O número digitado é negativo.")
else:
    print("O número digitado é nulo.")
    
    
# Para colocar várias verificações num if, use and/or
if numero > 20 and numero < 30:
    print("O número digitado é maior que 20 e menor que 30.")
    
if numero < 0 or numero > 100:
    print("O número digitado é menor que 0 ou maior que 100.")
    
    
    
# USANDO UM ÚNICO IF, VERIFIQUE SE O NÚMERO ESTÁ ENTRE 0 E 21 OU ENTRE 60 E 122
# IMPRIMA "paga meia" SE FOR VERDADEIRO, E "paga inteira / é espírito" CASO CONTRÁRIO




# Outro tipo de controle de fluxo é o for.
# Ele é usado para repetir certos comandos para um conjunto de valores.
# Vocês devem estar mais acostumados a usá-lo com uma sequência numérica.
# Veja que o range abaixo gera valores de 1 até 5, e não 6!
print("\nSequência de 1 até 5:")
    
for numero in range(1, 6):
    print(numero)


# Daria para usar o range para gerar os índices de uma lista, para percorrê-la.
# Mas, em vez disso, eu recomendo usar o "in".
lista = [-3, 0, 10, 7]

print("\nNúmeros da lista:")

for elemento in lista:
    print(elemento)
    
    
    
# CRIE UMA LISTA COM 6 NÚMEROS REPRESENTANDO NOTAS NUMA DISCIPLINA
# USE O FOR PARA PERCORRER CADA VALOR
# SE FOR MAIOR OU IGUAL A 5, IMPRIMA O VALOR COM 1 CASA DECIMAL SEGUIDO DE ": Aprovado"
# CASO CONTRÁRIO, IMPRIMA O VALOR COM 1 CASA DECIMAL SEGUIDO DE ": Reprovado"




# Agora, vamos falar um pouco mais de funções.
# Em Python, a maioria dos comandos está em bibliotecas.
# Para usar um deles, eu preciso primeiro importar da biblioteca.
# Por exemplo, posso importar a função cos (cosseno) da biblioteca math.
# Também dá para importar constantes, como o pi.
# Geralmente a gente escreve os imports no começo do código, mas coloquei aqui para fins didáticos.
# E existem outras maneiras de fazer isso, mas eu costumo usar assim.
from math import cos, pi


# Agora eu posso chamar a cosseno.
cosseno_de_pi = cos(pi)


# Se o Python não tiver uma certa função, dá para criar você mesmo.
# Para isso, usamos "def" seguido do nome da sua escolha, da seguinte forma.
def imprime_mantra():
    print("Na vida, tudo é passageiro (exceto o motorista).")
    

# Depois de definir a função, você pode chamá-la quantas vezes quiser.

# DESCOMENTE AS LINHAS ABAIXO PARA VER O RESULTADO NO SHELL

#imprime_mantra()
#for i in range(1, 10):
#    imprime_mantra()



# A sua função pode receber parâmetros e retornar valores
def cos_em_graus(angulo):
    angulo_em_radianos = angulo * pi / 180
    
    return cos(angulo_em_radianos)



# CHAME A FUNÇÃO PASSANDO O VALOR 45 ENTRE PARÊNTESIS, E IMPRIMA O RESULTADO




# Para finalizar, vamos falar de variáveis globais.
# Elas são bem úteis para guardarem valores ao longo do programa.
# Normalmente, as funções podem acessar as variáveis de fora.
x = 123
def imprime_x():
    print(x)    # Acessa o valor x de cima.


# O problema é quando você quer que a função modifique essa variável de fora.
# Essa função não vai mudar o x ali em cima. Ela esta criando um novo x interno.
def muda_x():
    x = 0       # Cria um novo x em vez de mudar o x de cima. =(
    


# DESCOMENTE AS LINHAS ABAIXO PARA VER O RESULTADO NO SHELL

#print("\nTentando mudar o x na função:")
#imprime_x()
#muda_x()
#imprime_x()



# Para corrigir isso, usaremos o marcador global.
# ATENÇÃO, são duas linhas separadas: uma para o "global" e outra para o valor!
global y
y = 456


# Como a função abaixo não vai mudar o y, não preciso usar global.
def imprime_y():
    print(y)      # Acessa o valor y de cima.


# Já essa função aqui vai mudar o y, então eu preciso usar global.
def muda_y():
    global y      # "Ei, Python, o y aqui vai ser o mesmo de cima!"
    y = 0         # Agora sim, mude o y lá de cima.
    


# DESCOMENTE AS LINHAS ABAIXO PARA VER O RESULTADO NO SHELL

#print("\nTentando mudar o y na função:")
#imprime_y()
#muda_y()
#imprime_y()



# CRIE UMA VARIÁVEL GLOBAL contagem COMEÇANDO EM 1
# CRIE UMA FUNÇÃO QUE MODIFIQUE ESSA VARIÁVEL, MULTIPLICANDO-A POR 2



# Importando a função sleep.
from time import sleep

# Roda para sempre até você parar o programa (botão vermelho Stop).
while True:  
    
    
    # CHAME A FUNÇÃO ANTERIOR E DEPOIS IMPRIMA O NOVO VALOR DA CONTAGEM AQUI DENTRO.
    
    
    
    
    # Use sempre um sleep dentro do while True, para não sobrecarregar o programa.
    sleep(0.5)
    