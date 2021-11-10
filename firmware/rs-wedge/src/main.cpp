#include "Arduino.h"
/* Robosapien wedge
 * Interface : virtual serial port 9600 8N1
 * Commands:
 *  audio 0 //audio from audio jack
 *  audio 1 //audio from Robosapien
 *  See robosapien.h for valid actions.
 *  e.g.
 *  action 202  //0xCA : whistle
 */
#include "robosapien.h"
#include "CommandLine.h"

#ifdef ARDUINO_TRINKET_M0
#define SerialPort Serial
#elif defined(ARDUINO_AVR_DIGISPARK)
#include <DigiCDC.h>
#define SerialPort SerialUSB
#else
#error "Undefined platform"
#endif

void doAction(char *tokens);
void doAudio(char *tokens);
byte parseTokens(char *tokens);

Robosapien robo(0);
CommandLine commandLine(SerialPort, (char *)"> ");
Command action = Command((char *)"action", &doAction);
Command audio = Command((char *)"audio", &doAudio);
const byte PIN_AUDIO = 1;

void setup()
{
	robo.init();
	SerialPort.begin(9600);
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

void doAction(char *tokens)
{
	byte val = parseTokens(tokens);
	robo.send((Robosapien::RoboCommand)val);
}

void doAudio(char *tokens)
{
	byte val = parseTokens(tokens);
	digitalWrite(PIN_AUDIO, val == 1 ? HIGH : LOW);
}

byte parseTokens(char *tokens)
{
	char *token = strtok(NULL, " ");

	if (token != NULL)
	{
		return atoi(token);
	}
	else
	{
		return 255;
	}
}
