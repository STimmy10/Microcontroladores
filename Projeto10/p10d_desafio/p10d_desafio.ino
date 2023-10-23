#include <Adafruit_GFX.h>
#include <MCUFRIEND_kbv.h>
#include <TouchScreen.h>
#include <JKSButton.h>

MCUFRIEND_kbv tela;
TouchScreen touch(6, A1, A2, 7, 300);
JKSButton botaoDecolar;
JKSButton botaoPousar;
JKSButton botaoEsquerda;
JKSButton botaoFrente;
JKSButton botaoDireita;

int vetorPontosX[20];
int vetorPontosY[20];
int contadorPontos = 0;

bool trajeto = false;

unsigned long instanteAnterior;

const int TS_LEFT = 145, TS_RT = 887, TS_TOP = 934, TS_BOT = 158;



void enviarDecolar(void) {
  Serial.println("decolar");
  return;
}

void enviarPousar(void) {
  Serial.println("pousar");
  return;
}

void enviarEsquerda(void) {
  Serial.println("esquerda");
  return;
}

void enviarFrente(void) {
  Serial.println("frente");
  return;
}

void enviarDireita(void) {
  Serial.println("direita");
  return;
}

void enviarParar(void) {
  Serial.println("parar");
  return;
}

void desenhaRetangulo(int tamX, int tamY, int x, int y) {
  tela.fillRect(x + 20, y + 161, tamX, tamY, TFT_ORANGE);
}

void apagaRetangulo() {
  tela.fillRect(20, 161, 200, 150, TFT_BLACK);
  Serial.println("Apagando");
}


void setup() {
  Serial.begin(9600);
  tela.begin(tela.readID());
  tela.fillScreen(TFT_BLACK);
  botaoDecolar.init(&tela, &touch, 60, 40, 100, 50, TFT_WHITE, TFT_GREEN, TFT_BLACK, "DECOLAR", 2);
  botaoPousar.init(&tela, &touch, 180, 40, 100, 50, TFT_WHITE, TFT_RED, TFT_WHITE, "POUSAR", 2);
  botaoEsquerda.init(&tela, &touch, 40, 100, 60, 50, TFT_WHITE, TFT_LIGHTGREY, TFT_BLACK, "<", 2);
  botaoFrente.init(&tela, &touch, 120, 100, 60, 50, TFT_WHITE, TFT_LIGHTGREY, TFT_BLACK, "^", 2);
  botaoDireita.init(&tela, &touch, 200, 100, 60, 50, TFT_WHITE, TFT_LIGHTGREY, TFT_BLACK, ">", 2);
  botaoDecolar.setPressHandler(enviarDecolar);
  botaoPousar.setPressHandler(enviarPousar);
  botaoEsquerda.setPressHandler(enviarEsquerda);
  botaoFrente.setPressHandler(enviarFrente);
  botaoDireita.setPressHandler(enviarDireita);
  botaoEsquerda.setReleaseHandler(enviarParar);
  botaoFrente.setReleaseHandler(enviarParar);
  botaoDireita.setReleaseHandler(enviarParar);

  tela.drawRect(19, 160, 202, 152, TFT_WHITE);

  tela.setCursor(50, 140);
  tela.setTextColor(TFT_WHITE);
  tela.setTextSize(1);
  tela.print("Objeto Laranja Detectado");
}

void loop() {
  botaoDecolar.process();
  botaoPousar.process();
  botaoEsquerda.process();
  botaoFrente.process();
  botaoDireita.process();

  TSPoint ponto = touch.getPoint();
  pinMode(A1, OUTPUT);
  digitalWrite(A1, HIGH);  // reconfigura pinos
  pinMode(A2, OUTPUT);
  digitalWrite(A2, HIGH);  // para desenho
  int forca = ponto.z;     // força aplicada na tela
  if (forca > 200 && forca < 1000) {
    if (millis() - instanteAnterior > 300) {
      int x = map(ponto.x, TS_LEFT, TS_RT, 0, 240);
      int y = map(ponto.y, TS_TOP, TS_BOT, 0, 320);
      if (x > 19 && x < 221 && y < 354 && y > 156) {
        trajeto = true;
        if ((abs(x - vetorPontosX[0])<20) && (abs(y - vetorPontosY[0])<20)){
          tela.drawLine(vetorPontosX[0], vetorPontosY[0], vetorPontosX[contadorPontos-1], vetorPontosY[contadorPontos-1], TFT_CYAN);
          Serial.print("trajeto ");
          trajeto = false;
          for (int i = 0; i < contadorPontos; i++){
            Serial.print(vetorPontosX[i]);
            Serial.print(" ");
            Serial.print(vetorPontosY[i]);
            Serial.print(" ");
          }
          Serial.println("");
          contadorPontos = 0;
        }
        else {
          if (contadorPontos>0){
            tela.drawLine(vetorPontosX[contadorPontos-1], vetorPontosY[contadorPontos-1], x, y, TFT_CYAN);
          } else {
            apagaRetangulo();
          }
          tela.fillCircle(x, y, 6, TFT_CYAN);
          vetorPontosX[contadorPontos] = x;
          vetorPontosY[contadorPontos] = y;
          contadorPontos++;
        }
      }
      instanteAnterior = millis();
    }
  }
  if ((Serial.available() > 0)){
    
    String texto = Serial.readStringUntil('\n');
    texto.trim();
    Serial.println(texto);
    if (texto.substring(0, 9) == "retangulo"&&(trajeto == false)){
      apagaRetangulo();
      String reserva = texto.substring(10, 13);
      int x = reserva.toInt();

      reserva = texto.substring(14, 17);
      int y = reserva.toInt();

      reserva = texto.substring(18, 21);
      int tamX = reserva.toInt();

      reserva = texto.substring(22, 25);
      int tamY = reserva.toInt();

      desenhaRetangulo(tamX, tamY, x, y);
    }
  }
}
