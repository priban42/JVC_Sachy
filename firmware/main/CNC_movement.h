#ifndef CNC_movement_h
#define CNC_movement_h
#include <SpeedyStepper.h>
#include <Arduino.h>

#define dirX 5
#define stepX 2

#define dirY 7
#define stepY 4

#define dirR 6
#define stepR 3

#define enableXY 8

#define limit_switch_X 11 
#define limit_switch_Y 10

class CNC_movement{

  public:
    CNC_movement();
    void setOldCoordinates();
    void moveXY();
    void moveXY_start_acc();
    void moveXY_end_acc();
    void moveXY_no_acc();

    void move_R();
    
    void disableMotors();
    void enableMotors();
    void calibrate();
    
    float max_Speed = 140.0; // mm/s
    float acceleration = 1000.0;
    
    float spmm_X = 40.0;//79.8; // 42.4 steps per mm
    float spmm_Y = 40.0;//79.8;
    
    long maxdX = 230*spmm_X;
    long maxdY = 230*spmm_Y;

    long next_X = 0;
    long next_Y = 0;

    long current_X = 0;
    long current_Y = 0;

  private:
    
    SpeedyStepper stepperX;
    SpeedyStepper stepperY;
    
};

#endif
