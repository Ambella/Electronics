#!/usr/bin/python2.7
# Python 2.7 version by Alex Eames of http://RasPi.TV 

import spidev
from time import sleep
import sys

# reload spi drivers to prevent spi failures
import subprocess
unload_spi = subprocess.Popen('sudo rmmod spi_bcm2708', shell=True, stdout=subprocess.PIPE)
start_spi = subprocess.Popen('sudo modprobe spi_bcm2708', shell=True, stdout=subprocess.PIPE)
sleep(3)

char = '#'

def get_adc(channel,spi):                    # read SPI data from MCP3002 chip
   if ((channel > 1) or (channel < 0)): # Only 2 channels 0 and 1 else return -1
      return -1
   r = spi.xfer2([1,(2+channel)<<6,0])  # these two lines are explained in more detail at the bottom
   #print(r)
   ret = ((r[1]&31) << 6) + (r[2] >> 2)
   return ret

def get_adc_2bytes(channel,spi):                    # read SPI data from MCP3002 chip
   if ((channel > 1) or (channel < 0)): # Only 2 channels 0 and 1 else return -1
      return -1
   leftbyte=(6+channel)<<4
   r = spi.xfer2([leftbyte,0]) 
   #print(r)
   ret = ((r[0]) << 8) + (r[1])
   return ret


def display(char, adc_value): # function handles the display of ##### 
   reps = int(adc_value / 16)
   spaces = 64 - reps
   print('\r',"{0:04d}".format(adc_value), ' ', char * reps, ' ' * spaces,'\r', sep="", end='')
   sys.stdout.flush()

def get_adc_and_display(channel,char,spi):
   adc_value = (get_adc(channel,spi))
   adc_value_2bytes = (get_adc_2bytes(channel,spi))
   #print(adc_value,adc_value_2bytes)
   #print(adc_value)
   #display(char, adc_value)

def set_dtoa(iteration,spi):
   hexv=list((str(hex((iteration << 4)+0b1011000000000000))))
   leftbyte=int('0x'+str(hexv[2])+str(hexv[3]),16)
   rightbyte=int('0x'+str(hexv[4])+str(hexv[5]),16)
#  print("{0:08b} {1:08b}".format(leftbyte,rightbyte))
   r = spi.xfer2([leftbyte,rightbyte])

spi2 = spidev.SpiDev()
spi2.open(0,0)          # The Gertboard ADC is on SPI channel 0 (CE0 - aka GPIO8)

spi = spidev.SpiDev()
spi.open(0,1)        # The Gertboard DAC is on SPI channel 1 (CE1 - aka GPIO7)

sleepsecs=0.00001
channel=1

print("These are the connections for the digital to analogue test:")
print("jumper connecting GP11 to SCLK")
print("jumper connecting GP10 to MOSI")
print("jumper connecting GP9 to MISO")
print("jumper connecting GP7 to CSnB")
print("Multimeter connections (set your meter to read V DC):")
print("  connect black probe to GND")
#print("  connect red probe to DA%d on J29" % channel)
#raw_input("When ready hit enter.\n")
while True:
   for i in range(256):
      set_dtoa(i,spi)
      sleep(sleepsecs)
      get_adc_and_display(channel,char,spi2)
   for i in range(255,-1,-1):
      set_dtoa(i,spi)
      sleep(sleepsecs)
      get_adc_and_display(channel,char,spi2)

r = spi.xfer2([16,0])  # switch off channel A = 00010000 00000000 [16,0]
r = spi.xfer2([144,0]) # switch off channel B = 10010000 00000000 [144,0]

# The DAC is controlled by writing 2 bytes (16 bits) to it. 
# So we need to write a 16 bit word to DAC
# bit 15 = channel, bit 14 = ignored, bit 13 =gain, bit 12 = shutdown, bits 11-4 data, bits 3-0 ignored
# You feed spidev a decimal number and it converts it to 8 bit binary
# each argument is a byte (8 bits), so we need two arguments, which together make 16 bits.
# that's what spidev sends to the DAC. If you need to delve further, have a look at the datasheet. :)

