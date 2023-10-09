#include <EEPROM.h>
#include <Servo.h>
#include <GFButton.h>

int endereco = 0;
int contagem = 0;
int pino = 12;
int potenciometro = A5;
int valorFinal = 0;
int valorTeste = 0;

Servo base;
Servo ombro;

int valorOmbro = 90;

GFButton botaoA(2);
GFButton botaoB(3);
GFButton botaoC(4);

void aumentaContagem(){
  contagem += 1;
  Serial.println(contagem); 
  EEPROM.put(endereco, contagem);
  pinMode(potenciometro, INPUT);
}

void AApertado(){
  if (valorOmbro > 45){
    valorOmbro -= 1;
    delay(30);
  }
  ombro.write(valorOmbro);
}

void CApertado(){
  if (valorOmbro < 135){
    valorOmbro += 1;
    delay(30);
  }
  ombro.write(valorOmbro);
}

void mexeBase(){
  base.write(valorFinal);
}

void setup() {
  base.attach(pino);
  ombro.attach(11);
  Serial.begin(9600);
  botaoA.setPressHandler(aumentaContagem);
  botaoB.setPressHandler(aumentaContagem);
  botaoC.setPressHandler(aumentaContagem);
  EEPROM.get(endereco, contagem);
}

void loop() {
  int valorLido = analogRead(potenciometro);
  valorFinal = map(valorLido, 0, 1023, 0, 180);
  mexeBase();
  botaoA.process();
  botaoB.process();
  botaoC.process();
  if (botaoA.isPressed()){
    AApertado();
  }
  if (botaoC.isPressed()){
    CApertado();
  }
}

