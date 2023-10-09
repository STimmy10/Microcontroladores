#include <EEPROM.h>
#include <Servo.h>
#include <GFButton.h>
#include <meArm.h>


int endereco = 0;
int contagem = 0;
int base = 12, ombro = 11, cotovelo = 10, garra = 9;

int pontosSalvos[4][4];
int quantPontos = 0;

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
GFButton botaoD(5);

void toggleGarra(){
  if (garraFechada == false){
    garraFechada = true;
    braco.closeGripper();
  }
  else{
    garraFechada = false;
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

void salvaPonto(){
  if (quantPontos < 4){
    Serial.println("Salvei um ponto");
    pontosSalvos[quantPontos][0] = X;
    pontosSalvos[quantPontos][1] = Y;
    pontosSalvos[quantPontos][2] = Z;
    pontosSalvos[quantPontos][3] = garraFechada;
  }
  quantPontos += 1;
  EEPROM.put(endereco, pontosSalvos);
}

void executaPontos(){
  Serial.println("Executando os pontos salvos");
  for (int i = 0; i < 4; i++){
    X = pontosSalvos[i][0];
    Y = pontosSalvos[i][1];
    Z = pontosSalvos[i][2];
    garraFechada = pontosSalvos[i][3];
    braco.gotoPoint(X, Y, Z);
    if (garraFechada){
      braco.closeGripper();
    } else {
      braco.openGripper();
    }
    delay(500);
  }
}

void setup() {
  Serial.begin(9600);

  EEPROM.get(endereco, pontosSalvos);

  botaoA.setPressHandler(toggleGarra);
  botaoB.setPressHandler(toggleModo);
  botaoC.setPressHandler(salvaPonto);
  botaoD.setPressHandler(executaPontos);

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
    braco.goDirectlyTo(X, Y, Z);
  }
  
  botaoA.process();
  botaoB.process();
  botaoC.process();
  botaoD.process();
}

