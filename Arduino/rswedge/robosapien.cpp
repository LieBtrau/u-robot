/*Code based on https://playground.arduino.cc/Main/RoboSapienIR
*/
#include "robosapien.h"

Robosapien::Robosapien(byte outputPin):
  irPin(outputPin) {}

void Robosapien::init()
{
  pinMode(irPin, OUTPUT);
  digitalWrite(irPin, HIGH);
  timeout = millis();
}

void Robosapien::send(RoboCommand cmd)
{
  byte cmdByte=cmd;                               // to stop compiler warning
  const int BITTIME = 850;                        // Bit time (Theoretically 833 but 516 works for transmission and is faster)
  digitalWrite(irPin, LOW);
  delayMicroseconds(BITTIME<<3);                  // wait 8x bit time
  for (byte i = 0; i < 8; i++)
  {
    digitalWrite(irPin, HIGH);
    delayMicroseconds(BITTIME);
    if (bitRead(cmdByte, 7))
    {
      delayMicroseconds(BITTIME + (BITTIME<<1));  // wait 3x bit time
    }
    digitalWrite(irPin, LOW);
    delayMicroseconds(BITTIME);
    cmdByte <<=1;
  }
  digitalWrite(irPin, HIGH);
  delay(250); // Give a 1/4 sec before next
}

void Robosapien::update()
{
  if (millis() - timeout > 60000)
  {
    timeout = millis();
    send(NoOp);
  }
}



