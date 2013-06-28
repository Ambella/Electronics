#!/usr/bin/python

from time import sleep
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate
import socket, subprocess, re
from time import gmtime, strftime

def get_time():
    return strftime("%Y-%m-%d %H:%M:%S", gmtime())

def get_ipv4_address():
    """
    Returns IP address(es) of current machine.
    :return:
    """
    p = subprocess.Popen(["ifconfig"], stdout=subprocess.PIPE)
    ifc_resp = p.communicate()
    patt = re.compile(r'inet\s*\w*\S*:\s*(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
    resp = patt.findall(ifc_resp[0])
    print resp
    return resp


# Initialize the LCD plate.  Should auto-detect correct I2C bus.  If not,
# pass '0' for early 256 MB Model B boards or '1' for all later versions
lcd = Adafruit_CharLCDPlate()

# Clear display and show greeting, pause 1 sec
lcd.clear()
lcd.message("Adafruit RGB LCD\nPlate w/Keypad!")
sleep(1)

lcd.clear()

lcd.message(str(get_ipv4_address()[0]))
sleep(10)
# Cycle through backlight colors
col = (lcd.RED , lcd.YELLOW, lcd.GREEN, lcd.TEAL,
       lcd.BLUE, lcd.VIOLET, lcd.ON   , lcd.OFF)
for c in col:
    lcd.backlight(c)
    sleep(.5)

# Poll buttons, display message & set backlight accordingly
btn = ((lcd.LEFT  ,  get_time()             , lcd.ON),
       (lcd.UP    ,  str(get_ipv4_address()[0])    , lcd.ON),
       (lcd.DOWN  , 'I see fields\nof green'    , lcd.ON),
       (lcd.RIGHT , 'Purple mountain\nmajesties', lcd.ON),
       (lcd.SELECT, ''                          , lcd.OFF))
prev = -1
while True:
    for b in btn:
        if lcd.buttonPressed(b[0]):
            if b is not prev:
                if not lcd.buttonPressed(lcd.LEFT):
                   lcd.clear()
                   lcd.message(b[1])
                   lcd.backlight(b[2])
                   prev = b
                else:
                   lcd.clear()
                   lcd.message(get_time())
                   lcd.backlight(b[2])
            break
