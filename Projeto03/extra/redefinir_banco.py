from pymongo import MongoClient
from json import load
import os

def redefinir_banco():
    cliente = MongoClient("localhost", 27017)
    cliente.drop_database("projeto03")
    banco = cliente["projeto03"]

    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    moradores = banco["moradores"]
    dados = load(open(diretorio_atual + "/moradores.json"))
    moradores.insert(dados)
