#ifndef CNC_stepper_h
#define CNC_stepper_h
#include <Arduino.h>
#include <digitalWriteFast.h>


#define pin_dirX 5
#define pin_stepX 2

#define pin_dirY 6
#define pin_stepY 3

class CNC_stepper{
  public:
    CNC_stepper();
    void moveXY();
    
    void init();

    void set_next_X(long coordinate);
    void set_next_Y(long coordinate);

    void set_current_X(long coordinate);
    void set_current_Y(long coordinate);

    void set_stepsPerMM_X(float stepsPerMM);
    void set_stepsPerMM_Y(float stepsPerMM);

    void set_speed(float Speed);
    void set_acceleration(float Acceleration);

  private:

    void setDirectionsXY();
    
    float Q_rsqrt(float number);
    
    float max_Speed = 50.0;
    float acceleration = 100.0;

    float steps_per_mm_X = 80.0;
    float steps_per_mm_Y = 80.0;

    long directionX = -1; //1 or -1
    long directionY = -1;

    long current_X = 0;
    long current_Y = 0;

    long next_X = 0;
    long next_Y = 0;

    long stepsToGo_X;
    long stepsToGo_Y;

    long int acc_resolution;
    unsigned int acc_resolution_index = 40;//80

    float Base;
    float Base_speed;
    float Base_acceleration;

    boolean done_X;
    boolean done_Y;

    unsigned long first_step;

    unsigned long step_count;
    
    unsigned long acceleration_distance_X;
    unsigned long speed_distance_X;
    float speed_X;
    float acceleration_X;
    float speed_part_X;
    float speed_sum_X;
    float distance_acc_sum_X;
    float distance_acc_sum_sum_X;
    unsigned long Distance_X;
    float distance_part_X;
    unsigned long step_count_X;
    float mezera_X;
    float mezera_sum_X;

    unsigned long acceleration_distance_Y;
    unsigned long speed_distance_Y;
    float speed_Y;
    float acceleration_Y;
    float speed_part_Y;
    float speed_sum_Y;
    float distance_acc_sum_Y;
    float distance_acc_sum_sum_Y;
    unsigned long Distance_Y;
    float distance_part_Y;
    unsigned long step_count_Y;
    float mezera_Y;
    float mezera_sum_Y;
};
#endif
