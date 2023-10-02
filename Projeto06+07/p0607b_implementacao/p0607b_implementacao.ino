#include <GFButton.h>
#include <ShiftDisplay.h>
#include <RotaryEncoder.h>

ShiftDisplay display(4, 7, 8, COMMON_ANODE, 4, true);

int campainha = 5;
int terra = A5;

int posicaoAnterior = 0;

bool emAndamento = false;

unsigned long instanteAnterior = 0;

int led = 13;
int led2 = 12;
GFButton botao(A1);
GFButton botao3(A3);

int contagem = 0;

RotaryEncoder encoder(20, 21);
int origem1 = digitalPinToInterrupt(20);
int origem2 = digitalPinToInterrupt(21);


void toggle(){
  int val;
  val = digitalRead(led2);
  if (val == HIGH) {
    digitalWrite(led2, LOW);
  } else {
    digitalWrite(led2, HIGH);
  }
}

void comecaAndamento(){
  emAndamento = true;
  instanteAnterior = millis();
}

void acresce(){
  contagem+=1;
}

void contagemAdiciona(){
  contagem = contagem + 15;
}

void contagemSubtrai(){
  contagem = contagem - 15;
  if (contagem < 0) {
    contagem = 0;
  }
}

void tickDoEncoder() {
 encoder.tick();
}

void setup() {
  // put your setup code here, to run once:
  pinMode(led, OUTPUT);
  pinMode(led2, OUTPUT);

  Serial.begin(9600);

  botao.setPressHandler(comecaAndamento);

  digitalWrite(led, LOW);

  botao3.setPressHandler(acresce);

  attachInterrupt(origem1, tickDoEncoder, CHANGE);
  attachInterrupt(origem2, tickDoEncoder, CHANGE);
  
  pinMode(terra, OUTPUT);
  digitalWrite(terra, LOW);
  pinMode(campainha, OUTPUT);
}



void loop() {
  // put your main code here, to run repeatedly:
  
  botao.process();
  botao3.process();
  int contagemMinutos = contagem/60;
  int contagemSegundos = contagem%60;
  float total = 0;

  total = contagemSegundos / 100.0;

  total += contagemMinutos;
  display.set(total, 2, true);

  display.update();


  unsigned long instanteAtual = millis();
  if (instanteAtual > instanteAnterior + 1000) {
    if (emAndamento == true){
      contagem = contagem - 1;
      if (contagem == 0) {
        emAndamento = false;
        tone(campainha, 3000, 800);
      }
    }
    instanteAnterior = instanteAtual;
  }

  int posicao = encoder.getPosition();
  if (posicao != posicaoAnterior) {
    if (posicaoAnterior - posicao > 0){
      contagemSubtrai();
      tone(campainha, 220, 50);
    }
    else { 
      contagemAdiciona();
      tone(campainha, 440, 50);
    }
    posicaoAnterior = posicao;
  }
}
