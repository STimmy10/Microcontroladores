import threading
import socket
import subprocess
import time
import cv2 as cv
import numpy as np
import os
import random
class Tello:
    
    cap = None
    frame_lido = None

    def _conectar_tello_win(self):
        a="cp858"
        print("Conectando ao Tello(%s)"%self.TELLO_SSID,end="")
        for _ in range(15):
            print(".",end="")
            netshcmd = subprocess.Popen('netsh wlan connect ssid=%s name=%s'%(self.TELLO_SSID,self.TELLO_SSID), shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE )
            output_1, errors_1 = netshcmd.communicate()
            if errors_1: 
                print("WARNING: ", errors_1.decode(a))
            else:
                netshcmd = subprocess.Popen('netsh wlan show interfaces', shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE )
                output_2, errors_2 = netshcmd.communicate()
                if errors_2: 
                    print("WARNING: ", errors_2.decode(a))
                else:
                    for linha in output_2.decode(a).splitlines():
                        if self.TELLO_SSID in linha:
                            print("\n"+output_1.decode(a),end="")
                            return True
        return False    
        
    def __init__(self, ssid, test_mode=False):
        self.TELLO_SSID = ssid # "TELLO-C7AC08" = Micro 1, "TELLO-D023AE" = Micro 2, "TELLO-AC31C6" = Henrique
        self.test_mode = test_mode
        conectado = True

        self.resposta = None
        self.resposta_estado = None
        
        self.tempo_ultimo_cmd = 0
        self.TEMPO_CMDS_ms = 15  

        self.ip_local = "0.0.0.0"
        self.porta_local = 8889
        self.ip_local_state = "0.0.0.0"
        self.porta_local_state = 8890
        self.ip_local_image = "0.0.0.0"
        self.porta_local_image = 11111

        self.ip_tello = "192.168.10.1"
        self.porta_tello = 8889
        self.tello_addr = (self.ip_tello,self.porta_tello)

        ## servidor de comandos
        print("Iniciando servidor UDP de comandos: %s:%d"%(self.ip_local,self.porta_local))
        
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.ip_local,self.porta_local))

        self.thread_recebido = threading.Thread(target=self._recebido)
        self.thread_recebido.daemon = True
        self.thread_recebido.start()
        print("Servidor de comandos iniciado.")
  
        ## servidor de estados
        print("Iniciando servidor UDP de estado: %s:%d"%(self.ip_local_state,self.porta_local_state))
        
        self.socket_state = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket_state.bind((self.ip_local_state,self.porta_local_state))
        
        self.thread_estado_recebido = threading.Thread(target=self._estado_recebido)
        self.thread_estado_recebido.daemon = True
        self.thread_estado_recebido.start()
        print("Servidor de estados iniciado.")
        
        print("%s conectado e inicializado."%self.TELLO_SSID)
        
        if test_mode:
            self.stream = cv.VideoCapture(0) 
        
    def _recebido(self):
        while True:
            try:
                self.resposta,_ = self.socket.recvfrom(1024)
            except:
                break

    def _estado_recebido(self):
        while True:
            try:
                self.resposta_estado,_ = self.socket_state.recvfrom(2048)
            except:
                break

    def _image_recebido(self):
        while True:
            try:
                self.resposta_image,_ = self.socket_image.recvfrom(2048)
            except:
                break
    
    @property
    def state(self):
        if self.test_mode:
            return {
                "bat": random.randint(1,101),
                "wifi": random.randint(1,101),
                "temp": random.randint(1,101),
                "speed": random.randint(-100,101),
            }

        self.read_tof # keep connection with Tello alive

        while self.resposta_estado is None:
            pass
        resposta = self.resposta_estado.decode("utf-8")
        self.resposta_estado = None
        comandos = resposta.split(";")
        dicionario = {}
        for comando in comandos:
            chave_e_valor = comando.split(":")
            #print(chave_e_valor)
            if len(chave_e_valor) == 2:   
                chave = chave_e_valor[0]
                valor = chave_e_valor[1]
                if chave != "mpry":
                    valor = float(valor)
                dicionario[chave] = valor
                
        return dicionario

    @property
    def get_video_address(self):
        return "udp://@%s:%s?overrun_nonfatal=1&fifo_size=500000"%(self.ip_local_image,self.porta_local_image)
    
    def get_video_cap(self):
        if self.cap is None:
            self.cap = cv.VideoCapture(self.get_video_address,cv.CAP_FFMPEG)

        if not self.cap.isOpened():
            self.cap.open(self.get_video_address())

        return self.cap

    @property
    def current_image(self):
        if self.test_mode:
            if self.stream is None or not self.stream.isOpened():
                height = 480
                width = 640
                dummy_image = np.zeros((height , width , 3), np.uint8)
                dummy_image[:,:,0] = 140
                dummy_image[height//4 : 3*height//4, width//4 : 3*width//4] = (0, 147, 255)
                dummy_image[height//9 : 2*height//9, width//20 : 2*width//20] = (0, 147, 255)
                dummy_image[8*height//10 : 9*height//10, width//5 : 4*width//5] = (0, 147, 255)
                dummy_image[height//9 : 6*height//9, 17*width//20 : 18*width//20] = (0, 0, 255)
                return dummy_image
            else:
                _, image = self.stream.read()
                return image
                
        else:
            return self.get_video_cap().read()[-1]
    
    def the_eye(self):
        while True:
            cv.imshow("Tello vision", self.ler_frame)
            k = cv.waitKey(1) & 0xFF
        pthread_exit(NULL);

    def show_me(self):
        cv.namedWindow("Tello vision",cv.WINDOW_FREERATIO)
        cv.startWindowThread()
        cv.imshow("Tello vision", self.ler_frame)
        self.eye_thread = threading.Thread(target=self.the_eye)
        self.eye_thread.daemon = True
        self.eye_thread.start()
    
    def comando_com_resposta(self,comando):
        diff = time.time() * 1000 - self.tempo_ultimo_cmd
        while diff<self.TEMPO_CMDS_ms:
            diff = time.time() * 1000 - self.tempo_ultimo_cmd
            
        self.socket.sendto(comando.encode("utf-8"),self.tello_addr)

        while self.resposta is None:
            pass

        resposta = self.resposta.decode("utf-8")
        self.tempo_ultimo_cmd = time.time()*1000
        self.resposta = None
        return resposta

    def comando_sem_resposta(self,comando):
        diff = time.time() * 1000 - self.tempo_ultimo_cmd
        while diff<self.TEMPO_CMDS_ms:
            diff = time.time() * 1000 - self.tempo_ultimo_cmd
            
        self.socket.sendto(comando.encode("utf-8"),self.tello_addr)
        self.tempo_ultimo_cmd = time.time()*1000
        # while self.resposta is None:
        #     pass
        
        # resposta = self.resposta.decode("utf-8")
        self.resposta = None
        return None

    def envia_comando(self,comando):
        return self.comando_sem_resposta(comando)

    def envia_comando_de_leitura(self,comando):
        resposta = self.comando_com_resposta(comando)
        try:
            resposta = str(resposta) 
        except:
            pass
        
        if resposta.isdigit():
            return int(resposta)
        else:
            return resposta
        
    def fecha_tudo(self):
        self.envia_comando('land')
        self.socket.close()
        self.socket_state.close()
        cv.destroyAllWindows()
        

    def inicia_cmds(self):
        if not self.test_mode:
            print("Entrando em modo SDK: ",end="")
            resposta = self.envia_comando_de_leitura("command")
            while resposta!="ok":
                pass
            print(resposta)
            print("Iniciando Stream de video: ",end="")
            resposta = self.envia_comando_de_leitura("streamon")
            while resposta!="ok":
                pass
            print(resposta)
        
    @property
    def read_tof(self):
        if self.test_mode:
            return 1
        else:
            return self.envia_comando_de_leitura("tof?")

    @property
    def read_IMU(self):
        return self.envia_comando_de_leitura("attitude?")

    @property
    def read_speeds(self):
        return self.envia_comando_de_leitura("speed?")
    
    @property
    def read_time(self):
        return self.envia_comando_de_leitura("time?")

    @property
    def read_height(self):
        return self.envia_comando_de_leitrua("height?")

    @property
    def read_temperature(self):
        return self.envia_comando_de_leitura("temp?")

    @property
    def read_SNR(self):
        return self.envia_comando_de_leitura("wifi?")
    
    @property
    def sdk(self):
        return self.envia_comando_de_leitura("sdk?")
    
    def _print(self, text):
        print("\x1b[1;37;42m [DRONE TEST MODE] " + text + "\x1b[0m")

    def land(self):
        if self.test_mode:
            self._print("Drone is landing now")
        else:
            return self.envia_comando("land")

    def takeoff(self):
        if self.test_mode:
            self._print("Drone is flying now")
        else:
            return self.envia_comando("takeoff")

    def _anda(self,cmd,qtd):
        return self.envia_comando(cmd+" "+str(qtd))

    def forward(self,qtd):
        return self._anda("forward",qtd)

    def backward(self,qtd):
        return self._anda("back",qtd)

    def left(self,qtd):
        return self._anda("left",qtd)

    def right(self,qtd):
        return self._anda("right",qtd)

    def up(self,qtd):
        return self._anda("up",qtd)

    def down(self,qtd):
        return self._anda("down",qtd)

    def turn_left(self,qtd):
        return self._anda("ccw",qtd)

    def turn_right(self,qtd):
        return self._anda("cw",qtd)

    def rc(self,x,y,z,yaw):
        if self.test_mode:
            self._print("Drone is moving with speeds (%d, %d, %d, %d)" % (x, y, z, yaw))
        else:
            return self.envia_comando("rc %s %s %s %s"%(x,y,z,yaw))

    def goto(self,x,y,z,vel):
        if self.test_mode:
            self._print("Drone is going to (%d, %d, %d) at speed %d" % (x, y, z, vel))
        else:
            return self.envia_comando("go %s %s %s %s"%(x,y,z,vel))
    
    
