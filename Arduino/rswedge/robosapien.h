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
      // https://inventorsforce.wordpress.com/category/robosapien/
      // Ralf Fickert - Inventors:Force Project  "Hack the Robosapien V1 for Arduino"
      // Date: June 2015
      // Email: rfickert@st3am.comz
      //
      // References/Sources:
      // ===================
      // http://www.aibohack.com/robosap/ir_codes.htm
      // Many thanks to this reference I found the most complete list of Robosapien V1 hex Codes

      //////////////////////////////////////////////////////////////////////
      // Hacking - Robosapien V1 - Comprehensive hex command codes
      //////////////////////////////////////////////////////////////////////

      // LED RED - Just press buttons without using the SELECT - Basic Movement Commands
      //
      //Variable                       HEX-Code    Comment
      //------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
      //
      TurnRight               = 0x80,    // turn right                                   - Send command to turn right on the spot
      RightArmUp              = 0x81,    // right arm up                                 - Send command twice to fully raise arm up
      RightArmOut             = 0x82,    // right arm out                                - Send command twice to fully turn arm outwards
      TiltBodyRight           = 0x83,    // tilt body right
      RightArmDown            = 0x84,    // right arm down                               - Send command twice to fully lower arm down
      RightArmIn              = 0x85,    // right arm in                                 - Send command twice to fully turn arm inwards
      WalkForward             = 0x86,    // walk forward                                 - Send command twice to move forward slowly
      WalkBackward            = 0x87,    // walk backward                                - Send command twice to move backwards slowly
      TurnLeft                = 0x88,    // turn left                                    - Send command to turn left on the spot
      LeftArmUp               = 0x89,    // left arm up                                  - Send command twice to fully raise arm up
      LeftArmOut              = 0x8A,    // left arm out                                 - Send command twice to fully turn arm outwards
      TiltBodyLeft            = 0x8B,    // tilt body left
      LeftArmDown             = 0x8C,    // left arm down                                - Send command twice to fully lower arm down
      LeftArmIn               = 0x8D,    // left arm in                                  - Send command twice to fully turn arm inwards
      Stop                    = 0x8E,    // stop                                         - Send command at any time to end a command

      // Programming Commands (no shift)
      MasterCMDPRG            = 0x90,    //P (Master Command Program)
      //                                              - Send command to set Robosapien into program mode - Robosapien beeps - you can now program up to fourteen steps
      //                                                when 14 steps reached Robosapien will automatically repeat the programmed sequence. If you have less then 14 steps then you need to close
      //                                                the program by sending once the ProgramPlay command. To clear the program and return to the default program send the command MasterCMDPRG
      //                                                followed by the command ProgramPlay. Turning off the Robosapien will clear any previous set program. The sleep (Sleep) mode will
      //                                                keep Robosapiens memory for up to 2 hours. Please keep this in mind when writing the code.

      ProgramPlay             = 0x91,    //P>> (Program Play, the one on the bottom)

      RightSensorPRG          = 0x92,    //R>> (Right sensor program)
      //                                              - Send command to set Robosapien into program mode - Robosapien beeps - you can now program up to six steps
      //                                                when 6 steps reached Robosapien will automatically repeat the programmed sequence. If you have less then 6 steps then you need to close
      //                                                the program by sending once the ProgramPlay command.To trigger the sensor: touch a long finger, or a toe/heel sensor on the right side.
      //                                                Alternative send command ExecuteRightSensorPRG. To clear the program and return to the default program send the command LeftSensorPRG
      //                                                followed by the command ExecuteLeftSensorPRG. Turning off the Robosapien will clear any previous set program. The seep (Sleep) mode will
      //                                                keep Robosapiens memory for up to 2 hours. Please keep this in mind when writing the code.

      LeftSensorPRG           = 0x93,    //L>> (Left sensor program) )
      //                                              - Send command to set Robosapien into program mode - Robosapien beeps - you can now program up to six steps
      //                                                when 6 steps reached Robosapien will automatically repeat the programmed sequence. If you have less then 6 steps then you need to close
      //                                                the program by sending once the ProgramPlay command.To trigger the sensor: touch a long finger, or a toe/heel sensor on the left side
      //                                                Alternative send command ExecuteLeftSensorPRG. To clear the program and return to the default program send the command RightSensorPRG
      //                                                followed by the command ProgramPlay. Turning off the Robosapien will clear any previous set program. The seep (Sleep) mode will
      //                                                keep Robosapiens memory for up to 2 hours. Please keep this in mind when writing the code.


      SonicSensorPRG          = 0x94,    //S>> (Sonic sensor program)
      //                                              - Send command to set Robosapien into program mode - Robosapien beeps - you can now program up to six steps
      //                                                when 6 steps reached Robosapien will automatically repeat the programmed sequence. If you have less then 6 steps then you need to close
      //                                                the program by sending once the ProgramPlay command. To put robosapien into SONIC RESPONSE mode send command Listen. The Robosapien
      //                                                waits now for a sharp sound or tap on his body and then will run through your programmed routine. To clear the program and return to the default
      //                                                program send the command SonicSensorPRG followed by the command ProgramPlay . Turning off the Robosapien will clear any previous set program.
      //                                                The seep (Sleep) mode will keep Robosapiens memory for up to 2 hours. Please keep this in mind when writing the code.

      //LED GREEN - Press SELECT once - Combination Moves
      RightTurnStep           = 0xA0,    // right turn step                              - Send command to turn 45 degrees to the right
      RightHandThump          = 0xA1,    // right hand thump                             - Send command to lift right arm up and press downwards
      RightHandThrow          = 0xA2,    // right hand throw                             - Send command to throw object which is in Robosapiens right hand
      Sleep                   = 0xA3,    // sleep                                        - Send command to send Robosapiens to sleep. All sensors are inactive. Send Stop or WakeUp to wake him up. After 2 hours of
      //                                                                                   uninterrupted sleep the Robosapien will automatically power off.
      RightHandPickUp         = 0xA4,    // right hand pickup                            - Send command to let Robosapien pickup object (bucket) next to his right foot.
      LeanBackward            = 0xA5,    // lean backward                                - Send command to let Robosapien lean backwards and to open his arms
      ForwardStep             = 0xA6,    // forward step                                 - Send command to let Robosapien take two steps forward
      BackwardStep            = 0xA7,    // backward step                                - Send command to let Robosapien take two steps backwards
      LeftTurnStep            = 0xA8,    // left turn step                               - Send command to turn 45 degrees to the left
      LeftHandThump           = 0xA9,    // left hand thump                              - Send command to lift left arm up and press downwards
      LeftHandThrow           = 0xAA,    // left hand throw                              - Send command to throw object which is in Robosapiens left hand
      Listen                  = 0xAB,    // listen                                       - Send command to set Robosapien into listen mode - Robosapien responds to a sound or tap on his body with a default grunt, or a Sonnic Sensor Program
      //                                                                                   sequent as programmed by you.
      LeftHandPickUp          = 0xAC,    // left hand pickup                             - Send command to let Robosapien pickup object (bucket) next to his left foot.
      LeanForward             = 0xAD,    // lean forward                                 - Send command to let Robosapien lean forward and to close his arms
      Reset                   = 0xAE,    // reset                                        - Send command to reset Robosapien to his default positions
      ExecuteMasterPRG        = 0xB0,    // execute master command program               - Send command to play program routine.
      WakeUp                  = 0xB1,    // wakeup                                       - Send command to wakeup Robosapien. Robosapien goes through his wakeup routine.
      ExecuteRightSensorPRG   = 0xB2,    // right sensor program execute                 - Send command to play right sensor routine
      ExecuteLeftSensorPRG    = 0xB3,    // left sensor program execute                  - Send command to play left sensor routine
      ExecuteSonicPRG         = 0xB4,    // sonic sensor program execute                 - Send command to play left sensor routine

      // LED ORANGE Press SELECT twice - Combination Move
      RightHandStrike3        = 0xC0,    // right hand strike 3                          - Send command to perform an outside strike with the right hand
      RightHandSweep          = 0xC1,    // right hand sweep                             - Send command to knock things forward with a sweeping right arm and waist action
      Burp                    = 0xC2,    // burp                                         - Send command to burp ;-)
      RightHandStrike2        = 0xC3,    // right hand strike 2                          - Send command to perform an open right hand strike with a powerful Hoy-hah oOOo
      High5                   = 0xC4,    // high 5                                       - Send command to let Robosapien strech up on the right side for a big high 5 and to say Aaay
      RightHandStrike1        = 0xC5,    // right hand strike 1                          - Send command to perform an inside strike with the right hand with a Hi-yah
      Bulldozer               = 0xC6,    // bulldozer                                    - Send command to push forward 8 steps
      Fart                    = 0xC7,    // oops                                         - Send command to let Robosapien fart ;-)
      LeftHandStrike3         = 0xC8,    // left hand strike 3                           - Send command to perform an outside strike with the left hand
      LeftHandSweep           = 0xC9,    // left hand sweep                              - Send command to knock things forward with a sweeping left arm and waist action
      Whistle                 = 0xCA,    // whistle                                      - Send command to let Robosapien do a wolf whistle ;-)
      LeftHandStrike2         = 0xCB,    // left hand strike 2                           - Send command to perform an open left hand strike with a powerful Hoy-hah oOOo
      TalkBack                = 0xCC,    // talkback                                     - Send command to let Robosapien Grunt and gestures ;-)
      LeftHandStrike1         = 0xCD,    // left hand strike 1                           - Send command to perform an inside strike with the left hand with a Hi-yah
      Roar                    = 0xCE,    // roar                                         - Send command to let Robosapien lift both arms and roar
      AllDemo                 = 0xD0,    // All Demo                                     - Send command to let Robosapien execute all 3 pre-programmed demos (Demo 1, Demo 2 and Dance)
      PowerOff                = 0xD1,    // Power Off                                    - Send command to power off completely the Robosapien.Drop snow-globe and say "Rosebud" - On/Off Button is required to turn him on again.
      Demo1                   = 0xD2,    // Demo 1                                       - Send command to let Robosapien do Karate chopping
      Demo2                   = 0xD3,    // Demo 2                                       - Send command to show off attitude
      Dance                   = 0xD4,    // Dance                                        - Send command to let Robosapien show that he go the moves ;-)
      NoOp                    = 0xEF
    } RoboCommand;
    Robosapien(byte outputPin);
    void init();
    bool send(RoboCommand cmd);      //return false when called to quickly after previous call. Actions need time to complete
    void update();
  private:
    const unsigned long KEEPALIVE_TIMEOUT = 60000;
    const unsigned long ACTION_TIMEOUT = 250;
    unsigned long keepAliveTimeout;
    unsigned long actionTimeout;      //forced pause between two action commands
    byte irPin;                       // Where the echoed command will be sent from
};
#endif
