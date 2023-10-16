#include <GFButton.h>
#include <ShiftDisplay.h>

// NÃO COPIE O IMPLEMENTAÇÃO 1 PARA CÁ NÃO!
// ESSE É UM CÓDIGO SEPARADO DA PRIMEIRA PARTE!

// ESTE É O ARQUIVO DO ARDUINO SÓ COM O SHIELD MULTIFUNÇÃO.
// NÃO TEM MOTOR E SENSOR ÓTICO.

int movimento = 0;

GFButton botao1(A1);
GFButton botao2(A2);

int led1 = 13; 
int led2 = 12; 

ShiftDisplay display(4, 7, 8, COMMON_ANODE, 4, true);

void mudaMovimento(){
  movimento += 1;
  if (movimento >= 4){
    movimento = 0;
  }
}

void enviarMovimento(){
  if (movimento == 0){
    Serial1.println("frente");
  } else if (movimento == 1){
    Serial1.println("tras");
  } else if (movimento == 2){
    Serial1.println("esquerda");
  } else if (movimento == 3){
    Serial1.println("direita");
  }
}

void enviarParar(){
  Serial1.println("parar");
}

void setup() {
  Serial.begin(9600);
  Serial1.begin(9600);
  Serial1.setTimeout(10);

  botao1.setPressHandler(mudaMovimento);
  
  botao2.setPressHandler(enviarMovimento); 
  botao2.setReleaseHandler(enviarParar);

  pinMode(led1, OUTPUT);
  pinMode(led2, OUTPUT); 
}

void loop() {
  botao1.process();
  botao2.process();

  if (movimento == 0){
    display.set("frente");
  } else if (movimento == 1){
    display.set("tras");
  } else if (movimento == 2){
    display.set("esquerda");
  } else if (movimento == 3){
    display.set("direita");
  }
  display.update(); 

  if (Serial1.available() > 0) {
    String texto = Serial1.readStringUntil('\n');
    texto.trim(); // remove quebra de linha
    int index = texto.indexOf(",");
    int numero1, numero2;
    numero1 = (texto.substring(0, index)).toInt();
    numero2 = (texto.substring(index+2)).toInt();
    Serial.print(numero1);
    Serial.print(", ");
    Serial.println(numero2);

    if (numero1 > 600){
      digitalWrite(led1, HIGH);
    } else {
      digitalWrite(led1, LOW);
    }
    if (numero2 > 600){
      digitalWrite(led2, HIGH);
    } else {
      digitalWrite(led2, LOW);
    }
}
}
