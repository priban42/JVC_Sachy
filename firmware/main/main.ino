#include "Parser.h"

#define SERVO_PIN 10
Servo servo;


Parser parser;


void setup() {
  Parser parser;
  servo.attach(SERVO_PIN);
}

void loop() {
  parser.parseNext(servo);
}
