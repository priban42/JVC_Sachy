#include "Parser.h"
#include <Servo.h>

#define SERVO_PIN 10
Servo servo;
Servo servo_remover;


Parser parser;


void setup() {
  servo.attach(SERVO_PIN);
  Parser parser;
}

void loop() {
  parser.parseNext(servo, servo_remover);
}
