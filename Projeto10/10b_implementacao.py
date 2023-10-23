from extra.tello import Tello
from time import sleep
from cv2 import *
from traceback import format_exc

    
drone = Tello("TELLO-C7AC08", test_mode=True)
#drone = Tello("TELLO-D023AE", test_mode=True)
drone.inicia_cmds()
print("[INFO] - Drone pronto")



while True:
    
  # A linha abaixo já faz o papel do VideoCapture e do stream.read
    imagem = drone.current_image
  

  # COLOQUE AQUI O CÓDIGO DO OPENCV
    #_, imagem = stream.read()
  
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
