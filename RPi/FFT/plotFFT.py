import matplotlib
matplotlib.use('Qt4Agg')
import matplotlib.pylab as plt
import numpy as np
import time

def fftCalculations(data):
   data2=numpy.array(data)
   fourier=numpy.fft.rfft(data2)
   ffty = numpy.abs(fourier)
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
fh=open('testout.txt','r')

l1=fh.readline()
while l1:
   print(l1)
   l2=fh.readline()
   y=l1.rstrip().split(' ')[1:]
   y=[int(i) for i in y]
   y2=l2.rstrip().split(' ')[1:]
   y2=[float(i) for i in y2]
   x=[i for i in range(len(y))]
   x2=[i for i in range(len(y2))]
   print(len(x),len(y),len(x2),len(y2))
   print(x)
   print(y)

   line.set_xdata(np.array(x))
   line.set_ydata(np.array(y))
   line2.set_xdata(np.array(x2))
   line2.set_ydata(np.array(y2))

   plt.subplot(212)
   plt.ylim(0,max(y2))
   plt.draw()
   plt.pause(0.001)
   time.sleep(1)  
   l1=fh.readline()


