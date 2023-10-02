#include <GFButton.h>
#include <ShiftDisplay.h>
#include <RotaryEncoder.h>

ShiftDisplay display(4, 7, 8, COMMON_ANODE, 4, true);

// 7 notas
int frequenciasDasNotas[7] = { 659.26, 659.26, 659.26, 523.26, 659.26, 784.00, 392.00 };
int intervalosEntreNotas[7] = { 100, 200, 200, 100, 200, 400, 200 };

unsigned long instanteMusica = millis();

bool musica = false;

int campainha = 5;
int terra = A5;

int m = 1;

int indiceContagem = 0;

int posicaoAnterior = 0;

bool emAndamento[] = { false, false, false, false };

unsigned long instanteAnterior[] = { 0, 0, 0, 0 };

int led[] = { 13, 12, 11, 10 };

GFButton botao(A1);
GFButton botao2(A2);
GFButton botao3(A3);

int contagem[] = { 0, 0, 0, 0 };

RotaryEncoder encoder(20, 21);
int origem1 = digitalPinToInterrupt(20);
int origem2 = digitalPinToInterrupt(21);

void tocaMusica() {
  m = 1;
  instanteMusica = millis();
  musica = true;
}

void avancaLed() {
  if (indiceContagem == 0) {
    digitalWrite(led[0], LOW);
    digitalWrite(led[3], HIGH);
  } else {
    digitalWrite(led[indiceContagem], LOW);
    digitalWrite(led[indiceContagem - 1], HIGH);
  }
}

void comecaAndamento() {
  emAndamento[indiceContagem] = true;
  instanteAnterior[indiceContagem] = millis();
}

void acresce() {
  contagem[indiceContagem] += 1;
}

void contagemAdiciona() {
  contagem[indiceContagem] = contagem[indiceContagem] + 15;
}

void contagemSubtrai() {
  contagem[indiceContagem] = contagem[indiceContagem] - 15;
  if (contagem[indiceContagem] < 0) {
    contagem[indiceContagem] = 0;
  }
}

void mudaIndice() {
  indiceContagem += 1;
  tone(campainha, 500, 100);
  if (indiceContagem == 4) {
    indiceContagem = 0;
  }
  avancaLed();
}

void tickDoEncoder() {
  encoder.tick();
}

void setup() {
  // put your setup code here, to run once:
  for (int i = 0; i < 4; i++) {
    pinMode(led[i], OUTPUT);
    digitalWrite(led[i], HIGH);
  }
  digitalWrite(led[0], LOW);


  Serial.begin(9600);

  botao.setPressHandler(comecaAndamento);



  botao2.setPressHandler(mudaIndice);
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
  botao2.process();
  botao3.process();
  int contagemMinutos = contagem[indiceContagem] / 60;
  int contagemSegundos = contagem[indiceContagem] % 60;
  float total = 0;

  total = contagemSegundos / 100.0;

  total += contagemMinutos;
  display.set(total, 2, true);

  display.update();


  unsigned long instanteAtual = millis();
  for (int j = 0; j < 4; j++) {
    if (instanteAtual > instanteAnterior[j] + 1000) {
      if (emAndamento[j] == true) {
        contagem[j] = contagem[j] - 1;
        if (contagem[j] <= 0) {
          emAndamento[j] = false;
          contagem[j] = 0;
          tone(campainha, frequenciasDasNotas[0], 100);
          tocaMusica();
        }
      }
      instanteAnterior[j] = instanteAtual;
    }
  }

  if (musica == true) {

    unsigned long instanteAtualMusica = millis();
    if (instanteAtualMusica > instanteMusica + intervalosEntreNotas[m - 1]) {
      tone(campainha, frequenciasDasNotas[m], intervalosEntreNotas[m]);
      instanteMusica = millis();
      m++;
    }
    if (m == 7) {
      musica = false;
    }
  }


  int posicao = encoder.getPosition();
  if (posicao != posicaoAnterior) {
    if (posicaoAnterior - posicao > 0) {
      contagemSubtrai();
      tone(campainha, 220, 50);
    } else {
      contagemAdiciona();
      tone(campainha, 440, 50);
    }
    posicaoAnterior = posicao;
  }
}