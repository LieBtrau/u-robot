/*Code based on https://playground.arduino.cc/Main/RoboSapienIR
*/
#ifndef ROBOSAPIEN_H
#define ROBOSAPIEN_H

#include "Arduino.h"

class Robosapien
{
  public:
    // Some but not all RS commands are defined
    typedef enum {
      TurnRight =       0x80,
      RightArmUp =      0x81,
      RightArmOut =     0x82,
      TiltBodyRight =   0x83,
      RightArmDown =    0x84,
      RightArmIn =      0x85,
      WalkForward =     0x86,
      WalkBackward =    0x87,
      TurnLeft =        0x88,
      LeftArmUp =       0x89,
      LeftArmOut =      0x8A,
      TiltBodyLeft =    0x8B,
      LeftArmDown =     0x8C,
      LeftArmIn =       0x8D,
      Stop =            0x8E,
      WakeUp =          0xB1,
      Burp =            0xC2,
      RightHandStrike = 0xC0,
      NoOp =            0xEF
    }RoboCommand;
    Robosapien(byte outputPin);
    void init();
    void send(RoboCommand cmd);
    void update();
  private:
    unsigned long timeout;
    byte irPin;           // Where the echoed command will be sent from
};
#endif
