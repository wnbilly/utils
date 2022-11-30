import time
import os


import board
import busio

import adafruit_vl6180x # range sensor library
import RPi.GPIO as GPIO

from RPLCD import i2c # LCD library

# Constants to initialise the LCD

lcdmode = 'i2c'
cols = 20
rows = 4
charmap = 'A00'
i2c_expander = 'PCF8574'
address = 0x27 
port = 1 # 0 on an older Raspberry Pi

def LCD_text_init():
    lcd.write_string('   Panier ENSTAR')
    lcd.crlf()
    lcd.crlf()
    lcd.write_string('     0 cerise')

# Constants and variables for the counter
delay = 0.01 # delay to read and print the lux and range
threshold = 50 # in mm
counter = 0 # passes counter
detection = False

# Initialise the LCD
lcd = i2c.CharLCD(i2c_expander, address, port=port, charmap=charmap,
                  cols=cols, rows=rows)
LCD_text_init() # Write the initial text
# Create I2C bus (for range sensor code)
i2c = busio.I2C(board.SCL, board.SDA)

# Create sensor instance.
sensor = adafruit_vl6180x.VL6180X(i2c, offset=0)
# You can add an offset (in mm) to distance measurements here (e.g. calibration)

# SWITCH
reset_pin = 4 # pin for the counter button in BCM mode (15(BCM) = 10(BOARD))
bouncetime = 2000 # time in ms to avoid fake press
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

def counter_reset(channel):
    global counter
    counter = 0
    # print('PUSH on', channel)
    lcd.clear()
    lcd.crlf()
    lcd.write_string('Compteur mis a 0.')
    time.sleep(1)
    lcd.clear()
    LCD_text_init()
    
GPIO.setup(reset_pin, GPIO.IN) # Set pin 10 to be an input pin and set initial value to be pulled low
GPIO.add_event_detect(reset_pin,GPIO.RISING,callback=counter_reset, bouncetime=bouncetime) # Setup event on pin 10 rising edge


# Main loop prints the amount of cherries in the basket
try: # to avoir errors when sensor and LCD not plugged in
    while True:
        # Read the range in millimeters and print it.
        range = sensor.range # in mm
        if range < threshold:
            # print("Range: {0}mm".format(range))
            detection = True
        elif detection == True:
            counter += 1
            detection = False
            lcd.cursor_pos = (2,5)
            lcd.write_string(str(counter)+' cerises')

        # Delay for a (delay) seconds.
        time.sleep(delay)
except:
    GPIO.cleanup()
    os._exit(1)
