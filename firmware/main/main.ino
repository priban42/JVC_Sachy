#include "Parser.h"

#define SERVO_PIN 10
Servo servo;


Parser parser;


void setup() {
  Parser parser;
  servo.attach(SERVO_PIN);
  servo.write(50);
}

void loop() {
  parser.parseNext(servo);
}
