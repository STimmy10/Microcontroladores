#include <AFMotor.h>

// ESTE É O ARQUIVO DO ARDUINO COM OS MOTORES E OS SENSORES ÓTICOS.
// NÃO TEM BOTÃO, NEM LED E NEM DISPLAY AQUI.

AF_DCMotor motor4(4);
AF_DCMotor motor3(3);

int sensorOtico1 = A11; 
int sensorOtico2 = A12; 

unsigned long instanteAnterior = 0;

void frente(){
  motor3.run(FORWARD);
  motor4.run(FORWARD);
}

void tras(){
  motor3.run(BACKWARD);
  motor4.run(BACKWARD);
}

void esquerda(){
  motor3.run(BACKWARD);
  motor4.run(FORWARD);
}

void direita(){
  motor3.run(FORWARD);
  motor4.run(BACKWARD);
}

void parar(){
  motor3.run(RELEASE);
  motor4.run(RELEASE);
}

void setup() {
    Serial.begin(9600); 
    Serial1.begin(9600); 
    pinMode(sensorOtico1, INPUT);
    pinMode(sensorOtico2, INPUT);
    motor4.setSpeed(160);
    motor3.setSpeed(160);
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
    texto.trim(); // remove quebra de linha
    if (texto.startsWith("frente"))
      {
        frente();
      }
    else if (texto.startsWith("tras"))
      {
        tras();
      }     
    else if (texto.startsWith("esquerda"))
      {
        esquerda();
      }
    else if (texto.startsWith("direita"))
        {
        direita(); 
        }
    else if (texto.startsWith("parar"))
        {
        parar(); 
        }
  }  
}
