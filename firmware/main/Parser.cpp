#include "Arduino.h"
#include "Parser.h"
#include "CNC_movement.h"

CNC_movement CNC;

Parser::Parser(){
  Serial.begin(115200);
  CNC_movement CNC;
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
  
void Parser::parseNext(){
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
  }

  Serial.write(69);
}
  
