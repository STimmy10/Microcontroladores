#include <EEPROM.h>
#include <Servo.h>
#include <GFButton.h>
#include <meArm.h>
#include <LinkedList.h>

struct Posicao {
 int x;
 int y;
 int z;
 bool garraFechada;
};

LinkedList<Posicao> listaDeEstruturas;

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
GFButton botaoE(6);

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
  X += mapaX+1;
  Y += mapaY+1;

  if (X>150){
    X = 150;
  } else if (X < -150){
    X = -150;
  }

  if (Y>200){
    Y = 200;
  } else if (Y<100){
    Y = 100;
  }
  delay(50);
}

void salvaPonto(){
  Posicao elemento;
  elemento.x = X;
  elemento.y = Y;
  elemento.z = Z;
  elemento.garraFechada = garraFechada;
  listaDeEstruturas.add(elemento);
  Serial.println("Salvei um ponto");

  EEPROM.put(endereco + sizeof(int) + (contagem * sizeof(Posicao)), elemento);
  contagem +=1;
  EEPROM.put(endereco, contagem);
 
  
}

void executaPontos(){
  Serial.println("Executando os pontos salvos");
  for (int i = 0; i < listaDeEstruturas.size(); i++){
    Posicao elemento = listaDeEstruturas.get(i);
    X = elemento.x;
    Y = elemento.y;
    Z = elemento.z;
    garraFechada = elemento.garraFechada;
    braco.gotoPoint(X, Y, Z);
    if (garraFechada){
      braco.closeGripper();
    } else {
      braco.openGripper();
    }
    delay(500);
  }
}

void remontaLista(){
  Posicao elemento;
  EEPROM.get(endereco, contagem);
  for (int i = 0; i < contagem; i++){
    int tamanho = endereco + sizeof(int) + (i * sizeof(Posicao));
    EEPROM.get(tamanho, elemento);
    listaDeEstruturas.add(elemento);
  }

  Serial.println(contagem);
}

void apagaTudo(){
  listaDeEstruturas.clear();
  contagem = 0;
  EEPROM.put(endereco, contagem);
}

void setup() {
  Serial.begin(9600);
  remontaLista();

  botaoA.setPressHandler(toggleGarra);
  botaoB.setPressHandler(toggleModo);
  botaoC.setPressHandler(salvaPonto);
  botaoD.setPressHandler(executaPontos);
  botaoE.setPressHandler(apagaTudo);

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
    Serial.println(X);
    Serial.println(Y);
    Serial.println(Z);
    braco.goDirectlyTo(X, Y, Z);
  }
  
  botaoA.process();
  botaoB.process();
  botaoC.process();
  botaoD.process();
  botaoE.process();
}

