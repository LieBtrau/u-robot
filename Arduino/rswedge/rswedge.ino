#include "robosapien.h"
#include <DigiCDC.h>

Robosapien robo(0);

void setup()
{
  robo.init();
  SerialUSB.begin();
}

void loop()
{
  robo.update();
  if (SerialUSB.available())
  {
    char c = SerialUSB.read();
    SerialUSB.write(c);
    robo.send((Robosapien::RoboCommand)c);
  }
}
