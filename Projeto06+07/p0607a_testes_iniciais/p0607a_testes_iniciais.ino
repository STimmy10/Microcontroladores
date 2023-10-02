#include <GFButton.h>
#include <ShiftDisplay.h>
#include <RotaryEncoder.h>

ShiftDisplay display(4, 7, 8, COMMON_ANODE, 4, true);

int campainha = 5;
int terra = A5;

int posicaoAnterior = 0;

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

void acresce(){
  contagem+=1;
}

void tickDoEncoder() {
 encoder.tick();
}

void setup() {
  // put your setup code here, to run once:
  pinMode(led, OUTPUT);
  pinMode(led2, OUTPUT);

  Serial.begin(9600);

  botao.setPressHandler(toggle);

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
  display.set(contagem);
  display.update();


  unsigned long instanteAtual = millis();
  if (instanteAtual > instanteAnterior + 2000) {
    Serial.println(contagem);
    instanteAnterior = instanteAtual;
  }

  int posicao = encoder.getPosition();
  if (posicao != posicaoAnterior) {
    if (posicaoAnterior - posicao > 0){
      tone(campainha, 220, 50);
    }
    else { 
      tone(campainha, 440, 50);
    }
    posicaoAnterior = posicao;
  }
}
