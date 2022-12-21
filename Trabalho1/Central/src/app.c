#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#include "menu.h"
#include "tcp_client.h"
#include "gpio.h"
#include "app.h"

#define SLEEP_TIME 1000000

Data appData;

void appInit() {
  DHT22 dht22;
  dht22.temperature = 0.0;
  dht22.humidity = 0.0;
  appData.dht22Class1 = dht22;
  
}

Data currentData() {
  return appData;
}

void* appHandler() {
  while (1) {
    DHT22 dht22Class1 = requestData(0);
    DHT22 dht22FirstFloor = requestData(1);

    if (dht22Class1.temperature > 0 && dht22Class1.humidity > 0) {
      appData.dht22Class1 = dht22Class1;
    }

    DevicesOut devOut;
    devOut = recoverDevicesOutData();
    appData.devOut = devOut;

    printData(appData);
    usleep(SLEEP_TIME);
  }

  return NULL;
}