# microphone.py - read sound from analog and print it
# (c) BotBook.com - Karvinen, Karvinen, Valtokari
import sys
import time
import botbook_mcp3002 as mcp	# <1>
import numpy
from socket import socket, AF_INET, SOCK_DGRAM

SERVER_IP   = '10.0.1.38'
PORT_NUMBER = 5000
SIZE = 10240

def readSound(samples):
	buff = []	# <2>
	for i in range(samples):	# <3>
		buff.append(mcp.readAnalog())	# <4>
	return buff

def fftCalculations(data):
   data2=numpy.array(data)
   fourier=numpy.fft.rfft(data2)
   ffty = numpy.abs(fourier)
   ffty = ffty/256.0
   return  ffty

def main():
   fh=open(sys.argv[1],'w')
   mySocket = socket( AF_INET, SOCK_DGRAM )
   for i in range(1000):
      start = time.clock()
      sound = readSound(1024)	# <5>
                
      print("time:",i,(time.clock() - start)*1000)
      mystr=' '.join([str(j) for j in sound])
      fh.write(mystr)
      fh.write('\n')
      mySocket.sendto(bytes(str(mystr), 'UTF-8'),(SERVER_IP,PORT_NUMBER))
      barData = fftCalculations(sound)
      mystr=' '.join([str(j) for j in barData])
      fh.write(mystr)
      fh.write('\n')
           
      time.sleep(1)	# s
   fh.close()

if __name__ == "__main__":
	main()
