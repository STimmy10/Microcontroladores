from serial import Serial
from threading import Thread, Timer
from extra.tello import Tello
from time import sleep
from cv2 import *
from traceback import format_exc


global variacaoX
global variacaoY
imagem = None

def serial():
  while True:
    if meu_serial != None:
      texto_recebido = meu_serial.readline().decode().strip()
      if texto_recebido != "":
        print(texto_recebido)

        # ESCREVA AQUI O SEU CÓDIGO DA SERIAL!

        if texto_recebido == "decolar":
            drone.takeoff()
        if texto_recebido == "pousar":
            drone.land()
        if texto_recebido == "esquerda":
            drone.rc(40, 0, 0, 0)
        if texto_recebido == "frente":
            drone.rc(0, 40, 0, 0)
        if texto_recebido == "direita":
            drone.rc(-40, 0, 0, 0)
        if texto_recebido == "parar":
            drone.rc(0, 0, 0, 0)

            
    sleep(0.1)
    

# CASO A SERIAL NÃO FUNCIONE, COMENTE A LINHA ABAIXO E DESCOMENTE A SEGUINTE

meu_serial = Serial("COM28", baudrate=9600, timeout=0.1)
#meu_serial = None

print("[INFO] Serial: ok")

thread = Thread(target=serial)
thread.daemon = True
thread.start()  

#drone = Tello("TELLO-C7AC08", test_mode=True)
drone = Tello("TELLO-D023AE", test_mode=False)
drone.inicia_cmds()
print("[INFO] Drone pronto")



def imprime_e_envia_coordenadas():
  timer = Timer(2, imprime_e_envia_coordenadas)
  timer.start() 
  # ESCREVA AQUI O CÓDIGO DO TIMER RECORRENTE
  if imagem is None:
      return
  alturaCV = imagem.shape[0]
  comprimentoCV = imagem.shape[1]
 
  xMap = (xMaior * 200)/comprimentoCV
  yMap = (yMaior * 150)/alturaCV

  comprimentoMap = (comprimentoMaior * 200)/comprimentoCV
  alturaMap = (larguraMaior * 150)/alturaCV
  
  texto = "retangulo %03d %03d %03d %03d\n"%(xMap, yMap, comprimentoMap, alturaMap)
  print(texto)
  meu_serial.write(texto.encode("UTF-8"))
  
  
   
   
imprime_e_envia_coordenadas()

while True:

  # COLOQUE AQUI O CÓDIGO DO WHILE DA IMPLEMENTACAO
     # A linha abaixo já faz o papel do VideoCapture e do stream.read

    imagem = drone.current_image
  

  # COLOQUE AQUI O CÓDIGO DO OPENCV
  
    imagem_hsv = cvtColor(imagem, COLOR_BGR2HSV)
    laranja1 = (0, 60, 100)
    laranja2= (20, 255, 255)
    mascara = inRange(imagem_hsv, laranja1, laranja2)
    
    xMaior = 0
    yMaior = 0
    comprimentoMaior = 0
    larguraMaior = 0
    areaMaior = 0
    
    contornos,_ = findContours(mascara, RETR_TREE, CHAIN_APPROX_SIMPLE)
    for contorno in contornos:
        x, y, comprimento, altura = boundingRect(contorno)
        area = comprimento * altura
        if(area > 2000 and area > areaMaior):
            xMaior = x
            yMaior = y
            comprimentoMaior = comprimento
            larguraMaior = altura
            areaMaior = area
        #ret = rectangle(imagem, pt1=(x,y), pt2=(x + comprimento, y + altura), color=(34,139,34),thickness=10)
    #print(xMaior)
    
    rectangle(imagem, pt1=(xMaior,yMaior), pt2=(xMaior + comprimentoMaior, yMaior + larguraMaior), color=(34,139,34),thickness=3)

    
    #imagem2 = bitwise_and(imagem, imagem, mask=mascara)
    imshow("Minha Janela", imagem)
 
    if waitKey(1) & 0xFF == ord("q"):
        break
    
stream.release()
destroyAllWindows() 


    
   