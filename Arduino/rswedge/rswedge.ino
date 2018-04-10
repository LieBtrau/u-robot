/* Robosapien wedge
 * Interface : virutal serial port 9600 8N1
 * Commands:
 *  audio 0 //audio from audio jack
 *  audio 1 //audio from Robosapien
 *  See robosapien.h for valid actions.
 *  e.g.
 *  action 202  //0xCA : whistle
 */
#include "robosapien.h"
#include <DigiCDC.h>        //Virtual serial port
#include "CommandLine.h"

Robosapien robo(0);
CommandLine commandLine(SerialUSB, "> ");
Command action = Command("action", &doAction);
Command audio = Command("audio", &doAudio);
const byte PIN_AUDIO = 1;

void setup()
{
  robo.init();
  SerialUSB.begin();
  commandLine.add(action);
  commandLine.add(audio);
  pinMode(PIN_AUDIO, OUTPUT);
  digitalWrite(PIN_AUDIO, HIGH);
}

void loop()
{
  robo.update();
  commandLine.update();
}

void doAction(char* tokens)
{
  byte val = parseTokens(tokens);
  robo.send((Robosapien::RoboCommand)val);
}

void doAudio(char* tokens)
{
  byte val = parseTokens(tokens);
  digitalWrite(PIN_AUDIO, val==1 ? HIGH : LOW);
}

byte parseTokens(char* tokens)
{
  char* token = strtok(NULL, " ");

  if (token != NULL) 
  {
    return atoi(token);
  } else 
  {
    return 255;
  }
}


