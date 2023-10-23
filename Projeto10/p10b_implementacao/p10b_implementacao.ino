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

    
}

