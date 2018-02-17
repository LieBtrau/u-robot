#include "robosapien.h"

Robosapien robo(0);
unsigned long timeout;

void setup()
{
  robo.init();
  timeout=millis();
}



void loop()
{
  robo.update();
  if (millis() - timeout > 25000)
  {
    timeout = millis();
    robo.send(Robosapien::Burp);
  }
}
