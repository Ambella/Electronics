#!/usr/bin/env python2.7
# Python 2.7 version by Alex Eames of http://RasPi.TV 
# functionally equivalent to the Gertboard leds test by 
# Gert Jan van Loo & Myra VanInwegen
# Use at your own risk - I'm pretty sure the code is harmless,
# but check it yourself.

import wiringpi
from time import sleep

def pi_rev_check():      # Function checks which Pi Board revision we have
    # make a dictionary of known Pi board revision IDs
    rev_dict={'0002':1,'0003':1,'0004':2,'0005':2,'0006':2,'000f':2}

    # search the cpuinfo file to get the board revision ID
    revcheck = open('/proc/cpuinfo')
    cpuinfo = revcheck.readlines()
    revcheck.close()

    # put Revision ID line in a variable called matching  
    matching = [s for s in cpuinfo if "Revision" in s]

    # extract the last four useful characters containing Rev ID
    rev_num = str(matching[-1])[-5:-1] 

    # look up rev_num in our dictionary and set board_rev (-1 if not found)
    board_rev = rev_dict.get(rev_num, -1) 
    return board_rev

board_revision = pi_rev_check() # check Pi Revision to set port 21/27 correctly
if board_revision == 1:
    # define ports list Rev 1
    ports = [25, 24, 23, 22, 21, 18, 17, 11, 10, 9, 8, 7]
else:
    # define ports list all others
    ports = [25, 24, 23, 22, 27, 18, 17, 11, 10, 9, 8, 7]

# make a copy of ports list and then reverse it as we need both directions
ports_rev = ports[:]
ports_rev.reverse()

wiringpi.wiringPiSetupGpio()                        # initialise wiringpi

for port_num in ports:
    wiringpi.pinMode(port_num, 1)                   # set up ports for output

def reset_ports():
    for port_num in ports:
        wiringpi.digitalWrite(port_num, 0)          # switches off all LEDs
        wiringpi.pinMode(port_num, 0)               # and reset ports

def led_drive(reps, multiple, direction):           # define function to drive
    for i in range(reps):                      # repetitions, single or multiple
        for port_num in direction:                  # and direction
            wiringpi.digitalWrite(port_num, 1)      # switch on an led
            sleep(0.11)                             # wait for ~0.11 seconds
            if not multiple:                        # if we're not leaving it on
                wiringpi.digitalWrite(port_num, 0)  # switch it off again

# Print Wiring Instructions
print "These are the connections for the LEDs test:"                
print "jumpers in every out location (U3-out-B1, U3-out-B2, etc)"
print "GP25 in J2 --- B1 in J3 \nGP24 in J2 --- B2 in J3"
print "GP23 in J2 --- B3 in J3 \nGP22 in J2 --- B4 in J3"
print "GP21 in J2 --- B5 in J3 \nGP18 in J2 --- B6 in J3"
print "GP17 in J2 --- B7 in J3 \nGP11 in J2 --- B8 in J3"
print "GP10 in J2 --- B9 in J3 \nGP9 in J2 --- B10 in J3"
print "GP8 in J2 --- B11 in J3 \nGP7 in J2 --- B12 in J3"
print "(If you don't have enough straps and jumpers you can install"
print "just a few of them, then run again later with the next batch.)"
raw_input("When ready hit enter.\n")

try:
    # Call the led driver function for each required pattern
    led_drive(3, 0, ports)
    led_drive(1, 0, ports_rev)

    # run this once, switching off each led before next one comes on, forwards
    led_drive(1, 0, ports)

    # run once, switch led off before next one, reverse direction
    led_drive(1, 0, ports_rev)

    # (1, 1, ports) = run once, leaving each led on, forward direction
    led_drive(1, 1, ports)
    led_drive(1, 0, ports)        
    led_drive(1, 1, ports)
    led_drive(1, 0, ports)
except KeyboardInterrupt:           # trap a CTRL+C keyboard interrupt
    reset_ports()                   # reset ports on CTRL-C exit
reset_ports()                       # reset ports on normal exit
