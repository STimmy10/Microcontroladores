#include <AFMotor.h>

// ESTE É O ARQUIVO DO ARDUINO COM OS MOTORES E OS SENSORES ÓTICOS.
// NÃO TEM BOTÃO, NEM LED E NEM DISPLAY AQUI.

AF_DCMotor motor4(4);
AF_DCMotor motor3(3);

int sensorOtico1 = A11;
int sensorOtico2 = A12;

unsigned long instanteAnterior = 0;

bool modoAutomatico = false;

void frente() {
  motor3.run(FORWARD);
  motor4.run(FORWARD);
}

void tras() {
  motor3.run(BACKWARD);
  motor4.run(BACKWARD);
}

void esquerda() {
  motor3.run(BACKWARD);
  motor4.run(FORWARD);
}

void direita() {
  motor3.run(FORWARD);
  motor4.run(BACKWARD);
}

void parar() {
  motor3.run(RELEASE);
  motor4.run(RELEASE);
}

void setup() {
  Serial.begin(9600);
  Serial1.begin(115200);
  //Serial1.begin(9600);
  pinMode(sensorOtico1, INPUT);
  pinMode(sensorOtico2, INPUT);
  motor4.setSpeed(100);
  motor3.setSpeed(100);
}

void loop() {
  int valorAnalogicoSensor1 = analogRead(sensorOtico1);
  int valorAnalogicoSensor2 = analogRead(sensorOtico2);
  if (millis() > instanteAnterior + 100) {
    instanteAnterior = millis();
    Serial1.print(valorAnalogicoSensor1);
    Serial1.print(", ");
    Serial1.println(valorAnalogicoSensor2);
  }
  if (Serial1.available() > 0) {
    String texto = Serial1.readStringUntil('\n');
    texto.trim();  // remove quebra de linha
    Serial.println(texto);
    if (texto.startsWith("frente")) {
      frente();
    } else if (texto.startsWith("tras")) {
      tras();
    } else if (texto.startsWith("esquerda")) {
      esquerda();
    } else if (texto.startsWith("direita")) {
      direita();
    } else if (texto.startsWith("parar")) {
      parar();
      modoAutomatico = false;
    } else if (texto.startsWith("auto")) {
      modoAutomatico = true;
      //dois sensores na faixa preta
    }
  }
  if (modoAutomatico == true) {
    if (valorAnalogicoSensor1 > 600 && valorAnalogicoSensor2 > 600) {
      frente();
    } else
      //sensor esquerdo fora da faixa e sensor direito dentro da faixa preta
      if (valorAnalogicoSensor1 < 600 && valorAnalogicoSensor2 > 600) {
        direita();
      }
      //sensor direito fora da faixa e sensor esquerdo dentro da faixa preta
      else if (valorAnalogicoSensor1 > 600 && valorAnalogicoSensor2 < 600) {
        esquerda();
      }
      //dois sensores fora da faixa
      else if (valorAnalogicoSensor1 < 600 && valorAnalogicoSensor2 < 600) {
        tras();
      }
  }
}
