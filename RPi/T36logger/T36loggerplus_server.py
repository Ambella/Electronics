#!/usr/bin/env python
import time
import os
import sys
import matplotlib
matplotlib.use('Qt4Agg')
import matplotlib.pylab as plt
import numpy as np
from socket import socket, gethostbyname, AF_INET, SOCK_DGRAM
import sys
PORT_NUMBER = 5000
SIZE = 1024

hostName = gethostbyname( '0.0.0.0')

mySocket = socket( AF_INET, SOCK_DGRAM )
mySocket.bind( (hostName, PORT_NUMBER) )

DEBUG = 0
LOG = 1
VOLT = 1
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

mv1=0
mv0=0
while True:
        # read the analog pin (temperature sensor LM35)
        (data,addr) = mySocket.recvfrom(SIZE)
        data=str(data,'UTF8')
        data=data.split('_')
        if data[1] == 'volt':
          mv1=float(data[0])
        else:
          mv0=float(data[0])
        (data,addr) = mySocket.recvfrom(SIZE)
        data=str(data,'UTF8')
        data=data.split('_')
        if data[1] == 'volt':
          mv1=float(data[0])
        else:
          mv0=float(data[0])
        millivolts=mv0;
        millivolts1=mv1;

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
          plt.pause(0.001)
          i+=1
        
        if VOLT:
          tel=display(int(millivolts1),tel)
