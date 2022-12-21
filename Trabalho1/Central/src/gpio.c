#include <stdio.h>
#include <unistd.h>

#include "gpio.h"
#include "menu.h"
#include "alarm.h"
#include "tcp_client.h"
#include "app.h"

DevicesOut _devOut;
DevicesIn _devIn;

void dataInit() {
  _devOut.l01 = 0;
  _devOut.l02 = 0;
  _devOut.ac = 0;
  _devOut.pr = 0;
  _devOut.alarm = 0;
  _devOut.alarmPlaying = 0;

  
  _devIn.sjan = 0;
  _devIn.spor = 0;
  _devIn.scIn = 0;
  _devIn.scOut = 0;
  _devIn.spres = 0;
  _devIn.sfum = 0;
  _devIn.peopleQuantity = 0;

  Data data = currentData();
  data.devOut = _devOut;
  printData(data);
  printDevicesIn(_devIn);
}

void devicesInHandler(int command) {
  if (command == SPres) {
      if(_devIn.spres) {
        _devIn.spres = 0;
      }
      else {
          _devIn.spres = 1;
      }
  }


  else if (command == SFum) {
    Data data = currentData();

    if (_devIn.sfum == 0) {
      _devIn.sfum = 1;
      _devOut.alarm = 1;
      data.devOut = _devOut;
      printData(data);
    } else {
      _devIn.sfum = 0;
      _devOut.alarm = 0;
      alarmOff();
      alarmHandler();
      data.devOut = _devOut;
      printData(data);
    }
  }

  else if (command == SJan) {
    if(_devIn.sjan) {
        _devIn.sjan = 0;
    }
    else {
        _devIn.sjan = 1;
    }
  }
   else if (command == PR) {
    if(_devOut.pr) {
        _devOut.pr = 0;
    }
    else {
        _devOut.pr = 1;
    }
  }

  else if (command == SPor) {
    if(_devIn.spor){
        _devIn.spor = 0;
    }
    else {
        _devIn.spor = 1;
    }
  }

  else if (command == SC_IN) {
    if (_devIn.peopleQuantity < 100)
      _devIn.peopleQuantity += 1;
  }

  else if (command == SC_OUT) {
    if (_devIn.peopleQuantity > 0)
      _devIn.peopleQuantity -= 1;
  }


  if (_devIn.spres == 1 || _devIn.sfum == 1 || _devIn.sjan == 1 ||
    _devOut.pr == 1 || _devIn.spor == 1 ) {
    alarmHandler();
  }
  else {
    Data data = currentData();
    _devOut.alarmPlaying = 0;
    alarmOff();
    data.devOut = _devOut;
    printData(data);
  }
  
  printDevicesIn(_devIn);
}

void storeDevicesOutUpdate(DevicesOut devOutUpdated) {
  if (devOutUpdated.alarm == 0) {
    devOutUpdated.alarmPlaying = 0;
    alarmOff();
  }

  if (devOutUpdated.alarm == 1 && (
    _devIn.spres == 1 || _devIn.sfum == 1 || _devIn.sjan == 1 ||
    _devOut.pr == 1 || _devIn.spor == 1)) {
    devOutUpdated.alarmPlaying = 1;
  }

  Data data = currentData();
  data.devOut = devOutUpdated;
  printData(data);

  int res = 1;
  if (data.devOut.l01 != _devOut.l01) {
    res = sendCommand(L_01, data.devOut.l01, 0);
  }

  else if (data.devOut.l02 != _devOut.l02) {
    res = sendCommand(L_02, data.devOut.l02, 0);
  }

  else if (data.devOut.ac != _devOut.ac) {
    res = sendCommand(AC, data.devOut.ac, 0);
  }

   else if (data.devOut.pr != _devOut.pr) {
    res = sendCommand(PR, data.devOut.pr, 0);
  }

  if (res == 1) {
    _devOut = devOutUpdated;
  }
}

DevicesOut recoverDevicesOutData() {
  return _devOut;
}