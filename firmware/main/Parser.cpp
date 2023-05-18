#include "Arduino.h"
#include "Parser.h"
#include "CNC_movement.h"
//#include <SoftwareSerial.h>

//#define tx_pin 11
//#define rx_pin 10

//SoftwareSerial software_serial (rx_pin, tx_pin);

//#define MAGNET_DIR_PIN_1 12
//#define MAGNET_DIR_PIN_2 13
//#define MAGNET_PWM_PIN 9


CNC_movement CNC;

Parser::Parser(){
  Serial.begin(115200);
  //software_serial.begin(9600);
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

void Parser::parseNext(Servo servo, Servo servo_remover){
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
      CNC.moveXY_end_acc();
      break;
    case 10:
      CNC.setOldCoordinates();
      CNC.next_X = readValue(byteX) - base_X;
      CNC.next_Y = readValue(byteY) - base_Y;
      CNC.moveXY_start_acc();
      break;

    case 11: //move with eject
      CNC.setOldCoordinates();
      final_next_X = readValue(byteX) - base_X;
      final_next_Y = readValue(byteY) - base_Y;
      servo_angle = int(readValue(1));
      CNC.next_X = CNC.current_X + ((final_next_X - CNC.current_X)*6)/10;
      CNC.next_Y = CNC.current_Y + ((final_next_Y - CNC.current_Y)*6)/10;
      CNC.moveXY_start_acc();
      servo.write(servo_angle);
      CNC.setOldCoordinates();
      CNC.next_X = final_next_X;
      CNC.next_Y = final_next_Y;
      CNC.moveXY_no_acc();
      break;
    case 3://delay
      delay(readValue(2));
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
      servo_angle = readValue(1);
      //software_serial.write(servo_angle);
      //software_serial.write(servo_remover_angle);
      servo.write(servo_angle);
      servo_remover.write(servo_angle);
      break;
    case 12://set servo_remover
      //servo_remover_angle = readValue(1);
      //software_serial.write(servo_angle);
      //software_serial.write(servo_remover_angle);
      CNC.move_R();
      break;
  }

  Serial.write(69);
}
  
