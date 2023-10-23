#include <Adafruit_GFX.h>
#include <MCUFRIEND_kbv.h>
#include <TouchScreen.h>
#include <JKSButton.h>

MCUFRIEND_kbv tela;

TouchScreen touch(6, A1, A2, 7, 300);
const int TS_LEFT = 145, TS_RT = 887,TS_TOP = 934, TS_BOT = 158;

JKSButton botao;

void setup() {
  tela.begin( tela.readID() );
  tela.fillScreen(TFT_BLACK);

  botao.init(&tela, &touch, 120, 250, 80, 30, TFT_WHITE, TFT_PURPLE, 
  TFT_BLACK, "Contar", 2);

  botao.setPressHandler(clicouRetangulo);

  tela.fillRect(20, 20, 100, 40, TFT_WHITE);
  tela.drawRect(20, 20, 100, 40, TFT_WHITE);

  tela.fillRect(20, 60, 100, 40, TFT_RED);
  tela.drawRect(20, 60, 100, 40, TFT_RED);

  tela.fillTriangle(20, 20, 20, 100, 60, 60, TFT_BLUE);
  tela.drawTriangle(20, 20, 20, 100, 60, 60, TFT_BLUE);

  int raio = 0;
  for(int i = 0; i < 10; i++){
    raio += 5;
    tela.drawCircle(100, 160, raio, TFT_WHITE);
  }

}

int contagem = 0;

void loop() {
  botao.process();
}

void clicouRetangulo (JKSButton &botaoPressionado) {
  apagar();
  contagem ++;
  tela.setCursor(150, 200);
  tela.setTextColor(TFT_WHITE);
  tela.setTextSize(4);
  tela.print(contagem);
}

void apagar(){
  tela.fillRect(150, 200, 90, 30, TFT_BLACK);
}
