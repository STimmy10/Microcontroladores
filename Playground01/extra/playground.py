from tkgpio import TkCircuit

from threading import Thread
from os import path, environ, system
from subprocess import Popen, check_output
import sys
from json import load
import platform

def rodar (programa):
    pasta_atual = path.dirname(__file__)
    caminho_das_configuracoes = path.join(pasta_atual, "configuracoes.json")
    with open(caminho_das_configuracoes, encoding="UTF-8") as arquivo:
        configuracoes = load(arquivo)
    
    adicionar_no_path("mplayer")
    
    matar("mplayer")

    circuito = TkCircuit(configuracoes)
    circuito.run(programa)
    
def adicionar_no_path(pasta):
    caminho_atual = path.dirname(__file__)
    
    if platform.system() == "Windows":
        caminho = path.join(caminho_atual, "binarios\\" + pasta + "\\windows")
        environ["PATH"] += ";" + caminho
    elif platform.system() == "Darwin":
        caminho = path.join(caminho_atual, "binarios/" + pasta + "/mac/")
        environ["PATH"] += ":" + caminho
    else:
        return
    
    #print(environ['PATH'])
    
def matar(app):
    if platform.system() == "Windows":
        # POpen() and os.system() sometimes freeze the script when running via Thonny on Windows 
        try:
            check_output(["taskkill", "/F", "/IM", app + ".exe"])
        except:
            pass
    else:
        system("killall " + app + " &>/dev/null")
