#include "Arduino.h"
#include "Parser.h"
#include "CNC_movement.h"


//#define MAGNET_DIR_PIN_1 12
//#define MAGNET_DIR_PIN_2 13
//#define MAGNET_PWM_PIN 9


CNC_movement CNC;

Parser::Parser(){
  Serial.begin(115200);
  CNC_movement CNC;
  //pinMode(MAGNET_DIR_PIN_1, OUTPUT);
  //pinMode(MAGNET_DIR_PIN_2, OUTPUT);
  //pinMode(MAGNET_PWM_PIN, OUTPUT);
  CNC.disableMotors();
  
}

byte Parser::readByteSafe(){//waits until a byte arrives to buffer, than returns it
  while (not Serial.available()){}
  return Serial.read();
}

long Parser::readValue(byte bytes){//returns a number composed of several [bytes] in buffer
  long vraceni = 0;
  for (byte x = 0; x < bytes - 1; x++){
    vraceni += readByteSafe();
    vraceni *= 256;
    //vraceni = vraceni << 8;
  }
  vraceni += readByteSafe();
  return vraceni; 
}

void Parser::sendInt(int cislo){
  Serial.write(byte(cislo/256));
  Serial.write(byte(cislo%256));
}
  
void Parser::parseNext(Servo servo){
  byte command = readValue(byteC);
  //Serial.write(42);
  //Serial.println(command);
  switch(command){
    case 1:
      CNC.setOldCoordinates();
      CNC.next_X = readValue(byteX) - base_X;
      CNC.next_Y = readValue(byteY) - base_Y;
      CNC.moveXY();
      break;
    case 9:
      CNC.setOldCoordinates();
      CNC.next_X = readValue(byteX) - base_X;
      CNC.next_Y = readValue(byteY) - base_Y;
      //CNC.moveXY();
      CNC.moveXY_end_acc();
      break;
    case 10:
      CNC.setOldCoordinates();
      CNC.next_X = readValue(byteX) - base_X;
      CNC.next_Y = readValue(byteY) - base_Y;
      //CNC.moveXY();
      CNC.moveXY_start_acc();
      break;
    case 2:
      CNC.calibrate();
      break;
    case 3:
      break;
    case 4:
      CNC.disableMotors();
      break;
    case 5:
      CNC.enableMotors();
      break;
    case 6://set speed
      CNC.max_Speed = float(readValue(byteF));
      //Serial.write(42);
      //Serial.println(CNC.max_Speed);
      break;
    case 7://set acceleration
      CNC.acceleration = float(readValue(byteA));
      break;
    case 8://set servo
      int servo_value = readValue(1);
      servo.write(servo_value);
      break;
  }

  Serial.write(69);
}
  
