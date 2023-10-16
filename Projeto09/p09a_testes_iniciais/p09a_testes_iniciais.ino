#include <AFMotor.h>

AF_DCMotor motorA(1);
AF_DCMotor motor3(3);

int N = 0;

unsigned long instanteAnterior = 0;

int sensorOtico1 = A11; 
int sensorOtico2 = A12; 

int contador = 0;

bool maior800 = false;
void setup() {
    Serial.begin(9600); 

    pinMode(sensorOtico1, INPUT);
    pinMode(sensorOtico2, INPUT);
}

void loop() {
    if (Serial.available() > 0) {
      String texto = Serial.readStringUntil('\n');
      texto.trim(); // remove quebra de linha
      
      // Ao receber o comando "frente N" da Serial, gire o Motor 3 
      //para frente com a velocidade N. Ao receber "tras N", gire 
      //para trás com a velocidade N.
      if (texto.startsWith("frente"))
      {
        N = (texto.substring(7)).toInt();
        Serial.println(N);
        motor3.setSpeed(N); 
        motor3.run(FORWARD); 
      }
      
      if (texto.startsWith("tras"))
      {
        N = (texto.substring(5)).toInt();
        Serial.println(N);
        motor3.setSpeed(N);
        motor3.run(BACKWARD); 
      }     
    } 

    int valorAnalogicoSensor1 = analogRead(sensorOtico1);
    int valorAnalogicoSensor2 = analogRead(sensorOtico2);

    //A cada 500 milissegundos, imprima na Serial as leituras 
    //analógicas dos dois sensores óticos numa mesma linha, 
    //separadas por vírgula (ex: "529, 98")
    if (millis() > instanteAnterior + 500) {
      instanteAnterior = millis();
      Serial1.print(valorAnalogicoSensor1);
      Serial1.print(", ");
      Serial1.println(valorAnalogicoSensor2);

    }

//Aumente 1 vez um contador X cada vez que o valor 
//analógico do sensor ótico 2 ultrapassar o limiar de 800 (ou 
//seja, quando o valor passar de algo menor que 800 para 
//algo maior que 800). Em seguida, envie o texto "contagem 
//X" (com o valor de X) pela Serial
    if (valorAnalogicoSensor2 > 800 && maior800 == false)
    {
      contador = contador + 1;
      maior800 = true;
      Serial.print("contagem ");
      Serial.println(contador);
    }
    else
      if (valorAnalogicoSensor2 < 800 && maior800 == true)
      {
        maior800 = false;    
      }
}  
 


