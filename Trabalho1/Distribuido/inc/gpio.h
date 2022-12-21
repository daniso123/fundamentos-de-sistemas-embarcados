#ifndef GPIO_H
#define GPIO_H

#include <wiringPi.h>

#define L_01 18
#define L_02 23
#define AC 24
#define PR 25
#define AL_BZ 8
#define SPres 7
#define SFum 1
#define SJan 12
#define SPor 16
#define SC_IN 20
#define SC_OUT 21
#define DHT22 04

void gpioSetup();
void* gpioHandler();
void* peopleQuantityHandler();
void setDeviceState(int device, int state);
void turnDevicesOff();

#endif