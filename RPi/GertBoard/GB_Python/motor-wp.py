#!/usr/bin/env python2.7
# Python 2.7 version by Alex Eames of http://RasPi.TV 
# functionally similar to the Gertboard motor test by Gert Jan van Loo & Myra VanInwegen
# Use at your own risk - I'm pretty sure the code is harmless, but check it yourself.
# This is the WiringPi for Python version which uses the as yet undocumented hardware PWM

from __future__ import print_function               # all print statements in this prog must now be in python 3 format
import wiringpi, sys
from time import sleep

wiringpi.wiringPiSetupGpio()                        # Initialise wiringpi GPIO
wiringpi.pinMode(18,2)                              # Set up GPIO 18 to PWM mode
wiringpi.pinMode(17,1)                              # GPIO 17 to output
wiringpi.digitalWrite(17, 0)                        # port 17 off for rotation one way
wiringpi.pwmWrite(18,0)                             # set pwm to zero initially

print ("\nThese are the connections for the motor test:")            # Print wiring instructions
print ("GP17 in J2 --- MOTB (just above GP1)")
print ("GP18 in J2 --- MOTA (just above GP4)")
print ("+ of external power source --- MOT+ in J19")
print ("ground of external power source --- GND (any)")
print ("one wire for your motor in MOTA in J19")
print ("the other wire for your motor in MOTB in J19")
command = raw_input("When ready hit enter.\n>")

def display(printchar):                         # this function handles the display of >>> <<< + and -
    print (printchar, sep='', end='')           # using Python 3 print function to prevent line breaks
    sys.stdout.flush()

def reset_ports():                              # resets the ports for a safe exit
    wiringpi.pwmWrite(18,0)                     # set pwm to zero
    wiringpi.digitalWrite(18, 0)                # ports 17 & 18 off
    wiringpi.digitalWrite(17, 0)
    wiringpi.pinMode(17,0)                      # set ports back to input mode
    wiringpi.pinMode(18,0)

def loop(start_pwm, stop_pwm, step, printchar): # defines the main loop that we run in four different ways
    for x in range(start_pwm, stop_pwm, step):  # controlled by the function arguments
        wiringpi.pwmWrite(18,x)
        if x % (19) == 0:                       # if x is an exact multiple of 19 i.e. x/19 has remainder 0
            display(printchar)                  # print the + or - character
        sleep(rest)

rest = 0.013                        # vary "sleep" time for testing purposes ~ 0.013 is about right in use

try:
    display('>>> ')

    loop(140, 1024, 1, '+')         # the arguments for loop are (start_pwm, stop_pwm, step, printchar)
    loop(994, 110, -1, '-')         # 140 is enough to spin up my motor, 70 is about right to stop it

    wiringpi.digitalWrite(17, 1)                    # port 17 ON for opposite rotation
    display('\n<<< ')

    loop(954, 89, -1, '+')
    loop(121, 1024, 1, '-')
    display('\n')

except KeyboardInterrupt:                           # trap a CTRL+C keyboard interrupt
    reset_ports()                                   # reset ports on interrupt 

reset_ports()       # reset ports on normal exit

