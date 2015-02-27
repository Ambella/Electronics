Readme File for Gertboard Test Suite Programs in Python

Python 2.7 version by Alex Eames of http://RasPi.TV 
Latest version available from http://raspi.tv/downloads

Completed the set and released on 14 December 2012, update 04 Feb 2013

All the Python versions are functionally as identical as I could make them to the 
Gertboard test programs by Gert Jan van Loo & Myra VanInwegen

A full walkthrough of the programs is in the official Gertboard manual for
the new revision 2 assembled Gertboard.
http://www.element14.com/community/servlet/JiveServlet/downloadBody/51727-102-1-265829/Gertboard_UM_with_python.pdf

Use at your own risk - I'm pretty sure the code is harmless, but check it yourself.

Quick Usage instructions
========================
Unzip the file in the directory of your choice, on your Raspberry Pi then type:

sudo python leds-rg.py (assuming you chose to run the leds program (RPi.GPIO version)

Then follow the on-screen wiring instructions.
---

Two Versions
============
There are two GPIO systems that work in Python, RPi.GPIO and WiringPi for Python.

It is desirable to have them in two versions, for both RPi.GPIO and WiringPi.
Neither of these systems yet offers a fully finished set of capabilities, but most 
of it is covered between them.

1) RPi.GPIO is included in Raspbian (September 2012 onwards)
If you want to run the RPi.GPIO files you don't need to install anything unless you 
have an older version of Raspbian or other distro.

The RPi.GPIO files are the ones with progname-rg.py
Run these with...
sudo python progname-rg.py

2) WiringPi for Python
If you don't have WiringPi for Python installed already, the best way to install it
is...

sudo apt-get update
sudo apt-get install python-dev python-pip
sudo pip install wiringpi

Once that's done, you can run the WiringPi versions of the programs with...
sudo python progname-wp.py

Analog < > Digital converter programs (NEW 13 December 2012)
=====================================
To make use of atod.py, dtoa.py and dad.py you MUST have SPI enabled 

sudo nano /etc/modprobe.d/raspi-blacklist.conf

make sure there IS a # before blacklist spi-bcm2708, so it looks like this...
#blacklist spi-bcm2708

Adding this # prevents SPI being disabled. If you had to change it, you'll need to 
reboot to activate SPI.

sudo reboot

You will need to install the Python SPI wrapper: (Python 2.7)

cd ~ 
git clone git://github.com/doceme/py-spidev 


If you don’t have git installed, the above command will fail. Install git with...

sudo apt-get update
sudo apt-get install git

When asked  if you want to continue, answer Y
then, after installation, try again
git clone git://github.com/doceme/py-spidev

then it should copy the files into a directory called py-spidev. Go there next

cd py-spidev/ 
If you have already installed WiringPi for Python the next step (python-dev) may not be necessary...

then type
sudo apt-get install python-dev
y (to confirm). 

sudo python setup.py install 
And after that you should be able to use the ADC/DAC programs. No further reboot needed.


Aim
===
The aim is to produce a full set of Gertboard test programs, written in Python, 
true to the functionality of the original Gertboard test suite in C.

In the dad program, column 1 output is slightly different from C version 
because spidev uses denary, not hex. It seems foolish to slavishly follow the
original when it will just be confusing to people looking at the program and trying
to figure out how it works.

I'm not an expert programmer, so I hope these programs are reasonably easy to 
understand without being horribly poor programming style :)

Currently completed programs are:
===================
dad.py - using SPI with spidev 
dtoa.py - using SPI with spidev
atod.py - using SPI with spidev
motor-wp.py - using Hardware PWM and WiringPi
motor-rg.py - using sofware PWM and RPi.GPIO
leds-rg.py - leds program using RPi.GPIO
leds-wp.py - leds program using WiringPi
ocol-rg.py - ocol program using RPi.GPIO - test program for relay switching
ocol-wp.py - ocol program using WiringPi - test program for relay switching
buttons-rg.py - buttons program using RPi.GPIO
butled-rg.py - butled program using RPi.GPIO
buttons-wp.py - buttons program using WiringPi
butled-wp.py - butled program using WiringPi
potmot-wp.py - potmot program using WiringPi & spidev

Youtube Videos of the working programs:
==============
motor-wp.py - http://youtu.be/_6OHEQgn2wo
motor-rg.py - http://youtu.be/90EP20GgyGA
leds-rg.py - http://youtu.be/qp8UCfITSAY
leds-wp.py - http://youtu.be/qp8UCfITSAY
ocol-rg.py - http://youtu.be/mjHjawSTJ-k
ocol-wp.py - http://youtu.be/mjHjawSTJ-k
buttons-rg.py - http://youtu.be/DwlI2Fr1AXg
butled-rg.py - n/a

Blog posts about the programs
=============================
http://raspi.tv/2012/gertboard-software-in-python-2-7-motor-and-leds-programs
http://raspi.tv/2012/gertboard-software-in-python-2-7-part-2-ocol-and-buttons

Forum thread about the programs
===============================
http://www.raspberrypi.org/phpBB3/viewtopic.php?f=42&t=21874


Updates
=======

I will be releasing more as and when they are done.

No doubt, as time goes by and I get feedback, I will make tweaks and improvements.

5th November 2012 18:35 GMT
couple of tweaks to the cleanup in leds-wp & ocol-wp & made it a function
9th November 2012 10:30 GMT
leds-rg & leds-wp updated to include Pi Board Revision checker so the scripts will 
work correctly with all Pi boards
11 November 2012 09:00 GMT
tweaks to leds-rg and leds-wp to tidy up Rev checking code (style change only, function unaffected)
13 November 2012
reverted leds-rg and leds-wp to 9th November versions as the new tweaks broke for some Rev 2 512 Mb boards
13 December 2012
leds-rg now uses a much neater Revision checker built into RPi.GPIO
atod.py released - requires SPI to be enabled and py-spidev to be installed (see above)
dtoa.py released - requires SPI to be enabled and py-spidev to be installed (see above)
14 December 2012 16:44 GMT
dad.py released - requires SPI to be enabled and py-spidev to be installed (see above)
19 December 2012
dad.py improved to be more in line with how the original works
29 December 2012
potmot-wp.py released - requires SPI to be enabled py-spidev & WiringPi to be installed (see above)
25 January 2013
buttons-wp.py released - managed to get pullups working with WiringPi in Python
butled-wp.py released - WP version
27 January 2013
bugfix for atod.py, dtoa.py & dad.py
spi would fail if you previously used the spi ports in the same session in 
normal GPIO mode (e.g. run the leds program then try to run dad/dtoa/atod)
added code to reload the spi drivers to circumvent this.
There is further work ongoing to improve the way spi is handled and make it
more likely to work if you copy and paste code into your own programs.
04 Feb 2013
Improvements made to efficiency of buttons and butled program logic for both GPIO systems
(removing unnecessary str() calls)


Further development
===================
The suite is now complete. There remain a couple of holes due to incomplete implementations
of the Python GPIO systems.

Hardware PWM for RPi.GPIO motor program as and when it becomes available/documented 
for RPi.GPIO

Credits
=======
Hat tip to Alan Johnstone for the dictionary idea for rev_check function in 
leds-wp.py
Hat tip to texy for identifying py-spidev spi/GPIO issue (in a different context)
and Bgreat for the fix - simply reloading the spi drivers
Thanks also to Bgreat for helping me with ongoing general improvements to spi handling

