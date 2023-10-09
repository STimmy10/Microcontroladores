#include <EEPROM.h>
#include <Servo.h>
#include <GFButton.h>
#include <meArm.h>


int endereco = 0;
int contagem = 0;
int base = 12, ombro = 11, cotovelo = 10, garra = 9;

bool garraFechada = true;
bool modoAbsoluto = true;

int potenciometro = A5;
int valorFinal = 0;
int valorTeste = 0;

int eixoX = A0;
int eixoY = A1;

int mapaX, mapaY;

int X, Y, Z;

  meArm braco(
    180, 0, -pi/2, pi/2, // ângulos da base
    135, 45, pi/4, 3*pi/4, // ângulos do ombro
    180, 90, 0, -pi/2, // ângulos do cotovelo
    30, 0, pi/2, 0 // ângulos da garra
);



GFButton botaoA(2);
GFButton botaoB(3);
GFButton botaoC(4);

void toggleGarra(){
  if (garraFechada){
    garraFechada = false;
    braco.closeGripper();
  }
  else{
    garraFechada = true;
    braco.openGripper();
  }
}

void toggleModo(){
  if (modoAbsoluto){
    modoAbsoluto = false;
    Serial.println("Modo Relativo");
  }
  else {
    modoAbsoluto = true;
    Serial.println("Modo Absoluto");
  }
}

void incremento(){
  X += mapaX;
  Y += mapaY;

  if (X>150){
    X = 150;
  } else if (X < -150){
    X = -150;
  }

  if (Y>150){
    Y = 150;
  } else if (Y<-150){
    Y = -150;
  }
  delay(50);
}

void setup() {
  Serial.begin(9600);
  botaoA.setPressHandler(toggleGarra);
  botaoB.setPressHandler(toggleModo);

  EEPROM.get(endereco, contagem);

  braco.begin(base, ombro, cotovelo, garra);

  pinMode(eixoX, INPUT);
  pinMode(eixoY, INPUT);

  Serial.println("Modo Absoluto");

  braco.gotoPoint(0, 130, 0);
  braco.closeGripper(); 
}

void loop() {
  int valorLido = analogRead(potenciometro);

  if (modoAbsoluto){
    Z = map(valorLido, 0, 1023, -30, 100);
    X = map(analogRead(eixoX), 0, 1023, -150, 150);
    Y = map(analogRead(eixoY), 0, 1023, 100, 200);
    braco.gotoPoint(X, Y, Z);
  } else {
    Z = map(valorLido, 0, 1023, -30, 100);
    mapaX = map(analogRead(eixoX), 0, 1023, -10, 10);
    mapaY = map(analogRead(eixoY), 0, 1023, -10, 10);
    incremento();
    Serial.print(X);
    Serial.print("_");
    Serial.print(Y);
    Serial.print("_");
    Serial.println(Z);
    braco.goDirectlyTo(X, Y, Z);
  }
  
  botaoA.process();
  botaoB.process();
  botaoC.process();
}

