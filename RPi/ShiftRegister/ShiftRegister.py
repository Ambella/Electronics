#!/usr/bin/env python
import time
import os
import sys
import RPi.GPIO as GPIO
import numpy as np
from random import randint

GPIO.setmode(GPIO.BCM)

def updateLEDsLong(latchpin,clockpin,datapin,value):
  GPIO.output(latchpin, False)   ##Pulls the chips latch low
  time.sleep(0.1)
  for j in range(8):  ##Will repeat 8 times (once for each bit)
    print(j)
    print(bin(value))
    print(bin(128))
    bit = value & 128; ##We use a "bitmask" to select only the eighth 
    print(bin(bit))                           ##bit in our number (the one we are addressing this time through
    value <<= 1;          ##we move our number up one bit value so next time bit 7 willbe
                               ##bit 8 and we will do our math on it
    if bit == 128:
      GPIO.output(datapin, True) ##if bit 8 is set then set our data pin high
      print('data high')
    else:
      GPIO.output(datapin, False)            ##if bit 8 is unset then set the data pin low
      print('data low')
    #time.sleep(0.1)
    GPIO.output(clockpin, True)                ##the next three lines pulse the clock pin
    #time.sleep(0.1)
    
    #print('clock high')
    time.sleep(0.0005)
    GPIO.output(clockpin, False)
    #print('clock low')
    #time.sleep(0.1)

  GPIO.output(latchpin, True)  ##pulls the latch high shifting our data into being displayed
  #print('latch high')
  #time.sleep(0.1)
 
# read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
def readadc(adcnum, clockpin, mosipin, misopin, cspin):
        if ((adcnum > 7) or (adcnum < 0)):
                return -1
        GPIO.output(cspin, True)

        GPIO.output(clockpin, False)  # start clock low
        GPIO.output(cspin, False)     # bring CS low

        commandout = adcnum
        commandout |= 0x18  # start bit + single-ended bit
        commandout <<= 3    # we only need to send 5 bits here
        for i in range(5):
                if (commandout & 0x80):
                        GPIO.output(mosipin, True)
                else:   
                        GPIO.output(mosipin, False)
                commandout <<= 1
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)

        adcout = 0
        # read in one empty bit, one null bit and 10 ADC bits
        for i in range(12):
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)
                adcout <<= 1
                if (GPIO.input(misopin)):
                        adcout |= 0x1

        GPIO.output(cspin, True)

        adcout /= 2       # first bit is 'null' so drop it
        return adcout

# change these as desired - they're the pins connected from the
# SPI port on the ADC to the Cobbler
LATCH= 23
CLOCK = 24
DATA = 25

# set up the SPI interface pins
GPIO.setup(LATCH, GPIO.OUT)
GPIO.setup(CLOCK, GPIO.OUT)
GPIO.setup(DATA, GPIO.OUT)


# temperature sensor connected channel 0 of mcp3008
while True:
    #i=randint(0,255)
  for i in range(255):
    updateLEDsLong(LATCH,CLOCK,DATA,i)
    print(bin(i))

