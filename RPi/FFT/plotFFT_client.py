import matplotlib
matplotlib.use('Qt4Agg')
import matplotlib.pylab as plt
import numpy as np
import time
from socket import socket, gethostbyname, AF_INET, SOCK_DGRAM
import sys
PORT_NUMBER = 5000
SIZE = 10240

hostName = gethostbyname( '0.0.0.0')

mySocket = socket( AF_INET, SOCK_DGRAM )
mySocket.bind( (hostName, PORT_NUMBER) )
def fftCalculations(data):
   data2=np.array(data)
   fourier=np.fft.rfft(data2)
   ffty = np.abs(fourier)
   ffty = ffty/256.0
   return  ffty

plt.ion()
plt.subplot(211)
plt.xlim(0,1024)
plt.ylim(0,1024)
x=[0]
y=[0.5]
y2=[0.5]
line, = plt.plot(np.array(x),np.array(y),label='plotname',linewidth=2)
plt.xlabel('sample')
plt.ylabel('10 bit value')
plt.title('Raw sound sample input')
plt.subplot(212)
line2, = plt.plot(np.array(x),np.array(y2),label='plotname',linewidth=2)
plt.xlabel('value')
plt.ylabel('value')
plt.title('Fast Fourier Transform')
plt.xlim(0,512)
plt.ylim(0,10)
#plt.subplot(222)

while True:
   (data,addr) = mySocket.recvfrom(SIZE)
   data=str(data,'UTF8')
   data=data.split(' ')
   print(data)
   y=[int(i) for i in data]
   y2=fftCalculations(data)[1:]
   x=[i for i in range(len(y))]
   x2=[i for i in range(len(y2))]
   print(len(x),len(y),len(x2),len(y2))
   print(x)
   print(y)

   line.set_xdata(np.array(x))
   line.set_ydata(np.array(y))
   line2.set_xdata(np.array(x2))
   line2.set_ydata(np.array(y2))

   plt.subplot(211)
   plt.ylim(min(y)-100,max(y)+100)
   plt.draw()
   plt.subplot(212)
   plt.ylim(0,max(y2))
   plt.draw()
   plt.pause(0.001)


