# Neste Playground 00 A, vamos começar com os tipos básicos de variáveis em Python.
# Veja os códigos de exemplo e programe o que está sendo soliticado em LETRAS MAIÚSCULAS.


# Para declarar variáveis, não precisa de ponto-e-vírgula no final.
numero = 42
lista = [10, 20, 30, 40, 50]
dicionario = {"nome": "", }
texto = "Jan K. S."   # tanto faz usar aspas simples ou duplas


# Usamos o print para imprimir mensagens e variáveis ali embaixo no Shell.
# Clique em "Run current script" (botão verde de Play) para ver o resultado.
print("IMPRIMINDO COISAS AQUI NO SHELL")
print(numero)
print(lista)



# IMPRIMA O SEU NOME NO SHELL E CLIQUE EM RUN PARA TESTAR




# Listas podem guardar vários tipos de elementos, incluindo outras listas:
lista_de_numeros = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55];
lista_de_sobremesas = ["Pudim", "Brownie", "Cheesecake", "Bolo Arco-Íris", "Pavlova"]
lista_misturada = [1, 2, 3, "a", "b", "c", [0, True], None]



# CRIE UMA VARIÁVEL DE LISTA COM SEU NOME, ANO, MÊS E DIA DE NASCIMENTO.
# EM SEGUIDA, IMPRIMA ESSA LISTA NO SHELL.




# Para acessar elementos da lista, usamos o colchetes com o índice desejado.
# Lembrando que o índice começa em zero!
primeira_sobremesa = lista_de_sobremesas[0]  # índice 0 = 1º elemento
segunda_sobremesa = lista_de_sobremesas[1]   # índice 1 = 2º elemento


# Índices negativos (começando em -1) pegam elementos de trás para frente.
última_sobremesa = lista_de_sobremesas[-1]
penúltima_sobremesa = lista_de_sobremesas[-2]


# Dá até para usar o dois pontos para pegar vários elementos (sub-lista).
# ATENÇÃO: perceba que o Python vai do índice inicial até o anterior do final.
duas_primeiras_sobremesas = lista_de_sobremesas[0:2] # índices 0 e 1, sem o 2!



# ACESSE O 7º ELEMENTO DA LISTA DE NÚMERO E IMPRIMA-O (CUIDADO COM O ÍNDICE).
# DEPOIS ACESSE DE UMA VEZ SÓ O 3º, 4º, 5º E 6º ELEMENTO DA LISTA MISTURADA, E IMPRIMA.




# Passando para os textos (strings), usamos aspas duplas ou simples.
nome = "Jan"
sobrenome = 'K. S.'


# O acesso aos caracteres é o mesmo esquema do acesso a elementos de listas.
primeira_letra = nome[0]
primeiro_sobrenome = sobrenome[0:2]


# Podemos juntar textos usando o mais.
nome_completo = nome + " " + sobrenome


# Mas se quiser colocar um número dentro do texto, precisa converter para string primeiro.
duracao = 2021 - 1993
historico = "A carreira do Daft Punk durou " + str(duracao)  + " anos."


# Uma alternativa ao str() é usar o %, que permite configurar os dígitos.
# A ideia é bem parecida com a sprintf de outras linguagens.
# Obs: existem outras alternativas em Python (.format, f"", etc).
fahrenheit = 83
celsius = (fahrenheit - 32) * 5 / 9
meteorologia = "A temperatura atual é %d˚F / %.1f˚C" % (fahrenheit, celsius) # inteiro e decimal com 1 dígito



# CRIE UMA VARIÁVEL distancia QUE FAÇA A MULTIPLICAÇÃO DE 1280.4 POR 1.60934
# EM SEGUIDA, IMPRIMA ESSE VARIÁVEL COM 2 CASAS DECIMAIS NO TEXTO "A distância entre NY e Miami é de ____.__ km"




# E para converter um texto para número, usamos o int ou o float.
numero_inteiro = int("123")
numero_decimal = float("1.23")


# Para finalizar esta primeira parte do Playground, vamos falar de dicionários.
# Dicionários servem para organizar vários tipos de dados num só lugar.
# Cada elemento está associado a uma chave, e não a um índice/posição.
pais1 = {"nome": "Brasil",          "capital": "Brasília",       populacao:  211755692,  democracia: True}
pais2 = {"nome": "Estados Unidos",  "capital": "Washington DC",  populacao:  328239523,  democracia: True}
pais3 = {"nome": "China",           "capital": "Pequim",         populacao: 1400050000,  democracia: False}


# Para acessar o valor de uma chave, usamos colchetes novamente, só que com o nome em vez do índice.
capital_do_Brasil = pais1["capital"]


# Eu posso criar uma lista com esses dicionários.
lista_de_paises = [pais1, pais2, pais3]



# CRIE UM QUARTO PAÍS COM AS MESMAS CHAVES DOS ANTERIORES
# EM SEGUIDA, ACRESCENTE ESSE PAÍS NA LISTA COM A FUNÇÃO APPEND




# FAÇA UM FOR QUE PERCORRA TODOS OS PAÍSES.
# PARA CADA UM, IMPRIMA OS DADOS NO FORMATO "____ é um país com ___ habitantes cujo governo [é] / [não é] uma democracia".



