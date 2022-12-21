#ifndef GPIO_H_
#define GPIO_H_

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


typedef struct {
  int l01;
  int l02;
  int pr;
  int ac;
  int alarm;
  int alarmPlaying;
} DevicesOut;

typedef struct {
  int spres;
  int sjan;
  int spor;
  int scIn;
  int scOut;
  int sfum;
  int peopleQuantity;
} DevicesIn;

typedef struct {
  float temperature;
  float humidity;
} DHT22;

typedef struct {
  DHT22 dht22Class1;
  DevicesOut devOut;
} Data;

void dataInit();
void devicesInHandler(int command);
void storeDevicesOutUpdate(DevicesOut devOutUpdated);
DevicesOut recoverDevicesOutData();

#endif