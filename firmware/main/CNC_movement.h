#ifndef CNC_movement_h
#define CNC_movement_h
#include <SpeedyStepper.h>
#include <Arduino.h>

#define dirX 5
#define stepX 2

#define dirY 6
#define stepY 3

#define enableXY 8

#define limit_switch_X 9 
#define limit_switch_Y 10

class CNC_movement{

  public:
    CNC_movement();
    void setOldCoordinates();
    void moveXY();
    void disableMotors();
    void enableMotors();
    void calibrate();
    
    float max_Speed = 140.0; // mm/s
    float acceleration = 1000.0;
    float accIndex = 1;
    
    float spmm_X = 80.0;//79.8; // 42.4 steps per mm
    float spmm_Y = 80.0;//79.8;
    
    long maxdX = 230*spmm_X;
    long maxdY = 230*spmm_Y;

    long next_X = 0;
    long next_Y = 0;

  private:
    
    SpeedyStepper stepperX;
    SpeedyStepper stepperY;
    
    long current_X = 0;
    long current_Y = 0;

    long distanceToGo_X;
    long distanceToGo_Y;

    int directionX = -1;
    int directionY = -1;

    byte byteX = 2;
    byte byteY = 2;

    long baseX = long(1)<<(8*byteX - 1);
    long baseY = long(1)<<(8*byteY - 1);

    float Base;
    float meziSpeed;
    float meziAcceleration;

    long long_null = -2147483648;
};

#endif
