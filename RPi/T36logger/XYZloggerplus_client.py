#!/usr/bin/env python
import time
import os
import sys
import RPi.GPIO as GPIO
from socket import socket, AF_INET, SOCK_DGRAM
from time import sleep

SERVER_IP   = '10.0.1.7'
PORT_NUMBER = 5000
SIZE = 1024
mySocket = socket( AF_INET, SOCK_DGRAM )

GPIO.setmode(GPIO.BCM)
DEBUG = 0
LOG = 0
VOLT = 1
tel=0
def display(x,y,z,tel):        # function handles the display of #####
    repsx=int(x/50)
    repsy=int(y/50)
    repsz=int(z/50)
    spacesx=66-repsx
    spacesy=66-repsy
    spacesz=66-repsz
    char='#'
    chars=r'-\\|/-\\|'
    tel+=1
    if tel>6:
      tel=0
    print('\r',chars[tel],'\r')
    print('\r','X: {}, Y: {}, Z:{} '.format(x,y,z),'\r', sep='')
    print('\r','[',"{0:04d}".format(x), ' ', char * repsx, ' ' * spacesx,']','\r', sep='')
    print('\r','[',"{0:04d}".format(y), ' ', char * repsy, ' ' * spacesy,']','\r', sep='')
    print('\r','[',"{0:04d}".format(z), ' ', char * repsz, ' ' * spacesz,']','\r', sep='', end='')
    sys.stdout.write("\033[F"*4) # Cursor up one line
    #sys.stdout.write("\033[K") # Clear to the end of line
    sys.stdout.flush()
    return(tel)

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
SPICLK = 18
SPIMISO = 23
SPIMOSI = 24
SPICS = 25

# set up the SPI interface pins
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)


# temperature sensor connected channel 0 of mcp3008
adcnum = 0

while True:
        # read the analog pin (temperature sensor LM35)
        read_adcx = readadc(2, SPICLK, SPIMOSI, SPIMISO, SPICS)
        read_adcy = readadc(3, SPICLK, SPIMOSI, SPIMISO, SPICS)
        read_adcz = readadc(4, SPICLK, SPIMOSI, SPIMISO, SPICS)

        # convert analog reading to millivolts = ADC * ( 3300 / 1024 )
        millivoltsx = read_adcx * ( 3300.0 / 1024.0)
        millivoltsy = read_adcy * ( 3300.0 / 1024.0)
        millivoltsz = read_adcz * ( 3300.0 / 1024.0)

        mySocket.sendto(bytes(str('{}_{}_{}'.format(millivoltsx,millivoltsy,millivoltsz)), 'UTF-8'),(SERVER_IP,PORT_NUMBER))

        # remove decimal point from millivolts
        #millivolts = "%d" % millivolts

        if VOLT:
          tel=display(int(millivoltsx),int(millivoltsy),int(millivoltsz),tel)
        
        time.sleep(0.001)
