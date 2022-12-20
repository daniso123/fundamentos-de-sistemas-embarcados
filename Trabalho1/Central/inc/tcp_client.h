#include "gpio.h"

#ifndef TCP_CLIENT_H_
#define TCP_CLIENT_H_

int sendCommand(int device, int state, int floor);
DHT22 requestData(int floor);

#endif