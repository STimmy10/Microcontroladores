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

void enviarDecolar(void){
  Serial.println("decolar");
  return;
}

void enviarPousar(void){
  Serial.println("pousar");
  return;
}

void enviarEsquerda(void){
  Serial.println("esquerda");
  return;
}

void enviarFrente(void){
  Serial.println("frente");
  return;
}

void enviarDireita(void){
  Serial.println("direita");
  return;
}

void enviarParar(void){
  Serial.println("parar");
  return;
}

void desenhaRetangulo (int tamX, int tamY, int x, int y) {
  tela.fillRect(x + 20, y + 161, tamX, tamY, TFT_ORANGE);
}

void apagaRetangulo () {
  tela.fillRect(20, 161, 200, 150, TFT_BLACK);
  Serial.println("Apagando");
}


void setup() {
    Serial.begin(9600);
    tela.begin( tela.readID() );
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
  if (Serial.available() > 0) {
    apagaRetangulo();
    String texto = Serial.readStringUntil('\n');
    texto.trim();
    Serial.println(texto);
    if (texto.substring(0, 9) == "retangulo"){   
      String reserva = texto.substring(10, 13);
      int x = reserva.toInt();
      Serial.println(x);

      reserva = texto.substring(14, 17);
      int y = reserva.toInt();
      Serial.println(y);

      reserva = texto.substring(18, 21);
      int tamX = reserva.toInt();
      Serial.println(tamX);

      reserva = texto.substring(22, 25);
      int tamY = reserva.toInt();
      Serial.println(tamY);

      desenhaRetangulo (tamX, tamY, x, y);
    }
}


    
}

