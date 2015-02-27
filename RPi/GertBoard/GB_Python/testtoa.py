#!/usr/bin/python2.7
# Python 2.7 version by Alex Eames of http://RasPi.TV 

import spidev
from time import sleep

# reload spi drivers to prevent spi failures
import subprocess
unload_spi = subprocess.Popen('sudo rmmod spi_bcm2708', shell=True, stdout=subprocess.PIPE)
start_spi = subprocess.Popen('sudo modprobe spi_bcm2708', shell=True, stdout=subprocess.PIPE)
sleep(3)

spi = spidev.SpiDev()
spi.open(0,1)        # The Gertboard DAC is on SPI channel 1 (CE1 - aka GPIO7)

print("These are the connections for the digital to analogue test:")
print("jumper connecting GP11 to SCLK")
print("jumper connecting GP10 to MOSI")
print("jumper connecting GP9 to MISO")
print("jumper connecting GP7 to CSnB")
print("Multimeter connections (set your meter to read V DC):")
print("  connect black probe to GND")
#print("  connect red probe to DA%d on J29" % channel)
raw_input("When ready hit enter.\n")
while True:
   for i in range(256):
      hexv=list((str(hex((i << 4)+0b1011000000000000))))
#      print(hexv)
      leftbyte=int('0x'+str(hexv[2])+str(hexv[3]),16)
      rightbyte=int('0x'+str(hexv[4])+str(hexv[5]),16)
#      print("{0:08b} {1:08b}".format(leftbyte,rightbyte))
      r = spi.xfer2([leftbyte,rightbyte])                   #write the two bytes to the DAC
      #sleep(0.0001)
   for i in range(255,-1,-1):
      hexv=list((str(hex((i << 4)+0b1011000000000000))))
      leftbyte=int('0x'+str(hexv[2])+str(hexv[3]),16)
      rightbyte=int('0x'+str(hexv[4])+str(hexv[5]),16)
#      print("{0:08b} {1:08b}".format(leftbyte,rightbyte))
      r = spi.xfer2([leftbyte,rightbyte])
      #sleep(0.0001)

r = spi.xfer2([16,0])  # switch off channel A = 00010000 00000000 [16,0]
r = spi.xfer2([144,0]) # switch off channel B = 10010000 00000000 [144,0]

# The DAC is controlled by writing 2 bytes (16 bits) to it. 
# So we need to write a 16 bit word to DAC
# bit 15 = channel, bit 14 = ignored, bit 13 =gain, bit 12 = shutdown, bits 11-4 data, bits 3-0 ignored
# You feed spidev a decimal number and it converts it to 8 bit binary
# each argument is a byte (8 bits), so we need two arguments, which together make 16 bits.
# that's what spidev sends to the DAC. If you need to delve further, have a look at the datasheet. :)

