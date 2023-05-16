#include "Arduino.h"
#include "CNC_movement.h"
#include "CNC_stepper.h"
#include <SpeedyStepper.h>

SpeedyStepper stepperX;
SpeedyStepper stepperY;

CNC_stepper CNC_Stepper;

CNC_movement::CNC_movement(){
  
  CNC_stepper CNC_Stepper;
  CNC_Stepper.init();
  
  CNC_Stepper.set_stepsPerMM_X(spmm_X);
  CNC_Stepper.set_stepsPerMM_Y(spmm_Y);
  
  stepperX.connectToPins(stepX, dirX);
  stepperY.connectToPins(stepY, dirY);

  pinMode(enableXY, OUTPUT);

  //pinMode(limit_switch_X, INPUT);
  //pinMode(limit_switch_Y, INPUT);
}

void CNC_movement::disableMotors(){
  digitalWrite(enableXY, HIGH);
}
void CNC_movement::enableMotors(){
  digitalWrite(enableXY, LOW);
}

void CNC_movement::setOldCoordinates(){
  current_X = next_X;
  current_Y = next_Y;
}

float Q_rsqrt(float number){
    long i;
    float x2, y;
    const float threehalfs = 1.5F;
    x2 = number * 0.5F;
    y  = number;
    i  = * ( long * ) &y;    // evil floating point bit level hacking
    i  = 0x5f3759df - ( i >> 1 );               // what the fuck? 
    y  = * ( float * ) &i;
    y  = y * ( threehalfs - ( x2 * y * y ) );   // 1st iteration
    return y;
}

void CNC_movement::moveXY(){
  CNC_Stepper.set_current_X(current_X);
  CNC_Stepper.set_current_Y(current_Y);
  
  CNC_Stepper.set_next_X(next_X);
  CNC_Stepper.set_next_Y(next_Y);
  
  CNC_Stepper.set_speed(max_Speed);
  CNC_Stepper.set_acceleration(acceleration);
  CNC_Stepper.moveXY();
}

void CNC_movement::moveXY_start_acc(){
  CNC_Stepper.set_current_X(current_X);
  CNC_Stepper.set_current_Y(current_Y);
  
  CNC_Stepper.set_next_X(next_X);
  CNC_Stepper.set_next_Y(next_Y);
  
  CNC_Stepper.set_speed(max_Speed);
  CNC_Stepper.set_acceleration(acceleration);
  CNC_Stepper.moveXY_start_acc();
  //CNC_Stepper.moveXY();
}

void CNC_movement::moveXY_end_acc(){
  CNC_Stepper.set_current_X(current_X);
  CNC_Stepper.set_current_Y(current_Y);
  
  CNC_Stepper.set_next_X(next_X);
  CNC_Stepper.set_next_Y(next_Y);
  
  CNC_Stepper.set_speed(max_Speed);
  CNC_Stepper.set_acceleration(acceleration);
  CNC_Stepper.moveXY_end_acc();
  //CNC_Stepper.moveXY();
}

void CNC_movement::calibrate(){
  
  stepperX.setSpeedInStepsPerSecond(80*spmm_X);
  stepperX.setAccelerationInStepsPerSecondPerSecond(4000*spmm_X);
  stepperX.setupRelativeMoveInSteps((maxdX + 20*spmm_X));

  stepperY.setSpeedInStepsPerSecond(80*spmm_Y);
  stepperY.setAccelerationInStepsPerSecondPerSecond(4000*spmm_Y);
  stepperY.setupRelativeMoveInSteps((maxdY + 20*spmm_Y));
  
  while(!stepperX.motionComplete() || !stepperY.motionComplete()){ 
    for (int x = 0; x<20; x++){
      stepperX.processMovement();
      stepperY.processMovement();
    }
    if (digitalRead(limit_switch_X) == 1){
      stepperX.setupStop();
      stepperX.setupRelativeMoveInSteps(0);
    }
    if (digitalRead(limit_switch_Y) == 1){
      stepperY.setupStop();
      stepperY.setupRelativeMoveInSteps(0);
    }
  }

  stepperX.setCurrentPositionInSteps(0);
  stepperY.setCurrentPositionInSteps(0);
  current_X = 0;
  current_Y = 0;
}
    
