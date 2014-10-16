/*
 Robotics with the BOE Shield – Chapter 2, Project 1
 Generate a servo full speed counterclockwise signal with pin 13 and
 full speed clockwise signal with pin 12.
 */

#include <Servo.h>                    // Include servo library
 
Servo servoLeft;                      // Declare left servo signal
Servo servoRight;                     // Declare right servo signal

void setup()                          // Built in initialization block
{
  servoLeft.attach(13);               // Attach left signal to pin 13
  servoRight.attach(12);              // Attach right signal to pin 12

  servoLeft.writeMicroseconds(1700);  // Pin 13 counterclockwise
  servoRight.writeMicroseconds(1300); // Pin 12 clockwise
  delay(3000);                        // ..for 3 seconds
  servoLeft.detach();                 // Stop servo signal to pin 13
  servoRight.detach();                // Stop servo signal to pin 12
}  
 
void loop()                           // Main loop auto-repeats
{                                     // Empty, nothing needs repeating
}
