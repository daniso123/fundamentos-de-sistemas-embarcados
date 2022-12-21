#include <stdio.h>
#include <unistd.h>
#include "gpio.h"
#include "tcp_client.h"

// Private functions signatures
void checkPresence();
void checkSmokeClass1();
void checkWindow1();
void checkDoorClass1();
void checkPeopleQuantityGround_IN();
void checkPeopleQuantityGround_OUT();
void checkpr();

// Main functions

void gpioSetup() {
  wiringPiSetup();
}

void* gpioHandler() {
  pinMode(SPres, OUTPUT);
  wiringPiISR(SPres, INT_EDGE_BOTH, &checkPresence);

  pinMode(SFum, OUTPUT);
  wiringPiISR(SFum, INT_EDGE_BOTH, &checkSmokeClass1);

  pinMode(SJan, OUTPUT);
  wiringPiISR(SJan, INT_EDGE_BOTH, &checkWindow1);


  pinMode(SPor, OUTPUT);
  wiringPiISR(SPor, INT_EDGE_BOTH, &checkDoorClass1);

  pinMode(PR, OUTPUT);
  wiringPiISR(PR, INT_EDGE_BOTH, &checkpr);


  for (;;) {
    sleep(1);
  }
}

void* peopleQuantityHandler() {
  pinMode(SC_IN, OUTPUT);
  wiringPiISR(SC_IN, INT_EDGE_BOTH, &checkPeopleQuantityGround_IN);

  pinMode(SC_OUT, OUTPUT);
  wiringPiISR(SC_OUT, INT_EDGE_BOTH, &checkPeopleQuantityGround_OUT);

  for (;;) {
    sleep(1);
  }
}

void setDeviceState(int device, int state) {
  pinMode(device, OUTPUT);
  digitalWrite(device, state);
}

void turnDevicesOff() {
  setDeviceState(L_01, LOW);
  setDeviceState(L_02, LOW);
  setDeviceState(AC, LOW);
  setDeviceState(PR, LOW);
}

// Private functions to handlers

void checkPresence() {
    printf("Sala 01 - Sensor de Presença Ativado!!!\n");
    sendCommand(SPres);

    int sensorState = digitalRead(SPres);
    int lampState = digitalRead(L_01);

    if (sensorState == 1 && lampState == 0) {
        pinMode(L_01, OUTPUT);
        digitalWrite(L_01, HIGH);
        sendCommand(L_01);

        sleep(10);

        pinMode(L_01, OUTPUT);
        digitalWrite(L_01, LOW);
        sendCommand(L_01);
    }
}

void checkSmokeClass1() {
    printf("Sala 01 - Sensor de Fumaça Ativado!\n");
    sendCommand(SFum);

    int sensorState = digitalRead(SFum);

    if (sensorState == 1) {
        pinMode(AL_BZ, OUTPUT);
        digitalWrite(AL_BZ, HIGH);
        sendCommand(AL_BZ);
    } else {
        pinMode(AL_BZ, OUTPUT);
        digitalWrite(AL_BZ, LOW);
        sendCommand(AL_BZ);
    }
}

void checkWindow1() {
    printf("Sala 01 - Sensor da Janela 1 Ativado!!!\n");
    sendCommand(SJan);
}

void checkDoorClass1() {
    printf("Sala 01 - Sensor da Porta Ativado!!!\n");
    sendCommand(SPor);
}
void checkpr(){
    printf("sala 1- Senso de Projetor Multimídia Ativado!!!\n");

}

void checkPeopleQuantityGround_IN() {
    int sensorState = digitalRead(SC_IN);

    if (sensorState == 1) {
        printf("Sala 01 - Sensor de contagem interno ativado!!!\n");
        sendCommand(SC_IN);
        delay(280);
    }
}

void checkPeopleQuantityGround_OUT() {
    int sensorState = digitalRead(SC_OUT);

    if (sensorState == 1) {
        printf("Sala 01 - Sensor de contagem externo ativado!!!\n");
        sendCommand(SC_OUT);
        delay(280);
    }
}


