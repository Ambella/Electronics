#!/usr/bin/env python
import time
import os
import sys
import RPi.GPIO as GPIO
import matplotlib
matplotlib.use('Qt4Agg')
import matplotlib.pylab as plt
import numpy as np


GPIO.setmode(GPIO.BCM)
DEBUG = 0
LOG = 1
VOLT = 0
tel=0
def display(mv,tel):        # function handles the display of #####
    reps=int(mv/50)
    spaces=66-reps
    char='#'
    chars=r'-\\|/-\\|'
    tel+=1
    if tel>6:
      tel=0
    print('\r',chars[tel],'\r')
    print('\r','Current Voltage is ',mv,' millivolt    ','\r', sep='')
    print('\r','[',"{0:04d}".format(mv), ' ', char * reps, ' ' * spaces,']','\r', sep='', end='')
    sys.stdout.write("\033[F"*2) # Cursor up one line
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

if LOG:
  plt.ion()
  plt.subplot(211)
  plt.xlim(0,510)
  plt.ylim(0,35)
  x=[0]
  y=[20]
  y2=[0]
  line, = plt.plot(np.array(x),np.array(y),label='plotname',linewidth=2)
  plt.xlabel('time in seconds')
  plt.ylabel('Temp')
  plt.title('Temperature logger')
  plt.subplot(212)
  line2, = plt.plot(np.array(x),np.array(y2),label='plotname',linewidth=2)
  plt.xlabel('time')
  plt.ylabel('Voltage')
  plt.title('Pot meter')
  plt.xlim(0,100)
  plt.ylim(0,3300)
  i=0

while True:
        # read the analog pin (temperature sensor LM35)
        read_adc0 = readadc(adcnum, SPICLK, SPIMOSI, SPIMISO, SPICS)
        read_adc1 = readadc(1, SPICLK, SPIMOSI, SPIMISO, SPICS)

        # convert analog reading to millivolts = ADC * ( 3300 / 1024 )
        millivolts = read_adc0 * ( 3300.0 / 1024.0)
        millivolts1 = read_adc1 * ( 3300.0 / 1024.0)

        # 10 mv per degree 
        temp_C = ((millivolts - 100.0) / 10.0) - 40.0

        # convert celsius to fahrenheit 
        temp_F = ( temp_C * 9.0 / 5.0 ) + 32

        # remove decimal point from millivolts
        millivolts = "%d" % millivolts

        # show only one decimal place for temprature and voltage readings
        temp_C = "%.1f" % temp_C
        temp_F = "%.1f" % temp_F

        if DEBUG:
                print("read_adc0:\t", read_adc0)
                print("millivolts:\t", millivolts)
                print("temp_C:\t\t", temp_C)
                print("temp_F:\t\t", temp_F)
                print("voltage:\t\t", millivolts1)

        if LOG:
          x.append(i)
          y.append(temp_C)
          y2.append(millivolts1)
          line.set_xdata(np.array(x))
          line.set_ydata(np.array(y))
          line2.set_xdata(np.array(x))
          line2.set_ydata(np.array(y2))
          if (i>500):
            plt.subplot(211)
            plt.xlim(i-500,i+10)
          if (i>100):
            plt.subplot(212)
            plt.xlim(i-100,i+10)
          plt.draw()
          plt.pause(0.005)
          i+=1
        
        if VOLT:
          tel=display(int(millivolts1),tel)
        
        time.sleep(0.05)
