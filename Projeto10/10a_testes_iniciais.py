from cv2 import *

stream = VideoCapture(0)
while True:
    _, imagem = stream.read()
    imagem_hsv = cvtColor(imagem, COLOR_BGR2HSV)
    laranja1 = (0, 60, 100)
    laranja2= (20, 255, 255)
    mascara = inRange(imagem_hsv, laranja1, laranja2)
    imagem2 = bitwise_and(imagem, imagem, mask=mascara)
    imshow("Só laranja", imagem2)
    
    imagem3 = cvtColor(imagem, COLOR_BGR2GRAY)
    imagem3 = cvtColor(imagem3, COLOR_GRAY2BGR)
    mascara2 = bitwise_not(mascara)
    imagem3 = bitwise_and(imagem3, imagem3, mask=mascara2)
    imshow("Laranja is the new black", imagem3)
    
    imagem4 = imagem2 + imagem3
    putText(imagem4, "Ado", (50, 50), color=(0, 140, 255), thickness=2, fontFace=FONT_HERSHEY_SIMPLEX, fontScale=2)
    imshow("Soma", imagem4)
    
 # mostra a imagem durante 1 milissegundo
 # e interrompe loop quando tecla q for pressionada
    if waitKey(1) & 0xFF == ord("q"):
        break
stream.release()
destroyAllWindows()