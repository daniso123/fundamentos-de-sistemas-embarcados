#ifndef GPIO_H
#define GPIO_H

#include <wiringPi.h>

#define L_01 7
#define L_02 0
#define AC 11
#define PR 25
#define AL_BZ 8
#define SPres 7
#define SFum 1
#define SJan 12
#define SPor 16
#define SC_IN 20
#define SC_OUT 21
#define DHT22 04
/*
#define LS_101 3
#define LS_102 6
#define LC_1 10
#define AC_1 26
#define SP_1 1
#define SF_1 5
define SJ_101 21
#define SJ_102 22
*/

void gpioSetup();
void* gpioHandler();
void* peopleQuantityHandler();
void setDeviceState(int device, int state);
void turnDevicesOff();

#endif