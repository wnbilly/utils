#!/usr/bin/env python3

import time
import pigpio
from commands_keyboard import arrows


class ESC:
    """
    .
    Tested with:
    - Turnigy Electonic Speed controller Plush 30 A (min_width,max_width)=(650,2500)
    - 
    """

    # Note that some batteries, 12 volt PSUs, etc. might only be capable of far less than this (e.g. 1350)
    # However, the controllers range should still be set to max for finest full-scale resolution.

    def __init__(self, pin, min_width = 1000, max_width = 2000):
        self.connexion = pigpio.pi()
        self.pin = pin
        self.min_width = min_width
        self.max_width = max_width
        init_speed = (self.min_width + self.max_width)//2
        self.connexion.set_servo_pulsewidth(self.pin, init_speed)


    def start(self, init_speed = 1200):
        step = 10
        delay_btwn_changes = 0.1 # seconds
        for speed in range(self.min_width, init_speed, step):
            self.set_speed(speed, delay_btwn_changes)

    def set_speed(self, speed, snooze: int = 0):
        """
        Convenience wrapper around pigpio's set_servo_pulsewidth.
        width: The servo pulsewidth in microseconds. 0 switches pulses off.
        snooze: seconds before returning.
        """
        # values must be between 500 and 2500 for set_servo_pulsewidth
        # print("pulse width to", speed, "µseconds for", snooze, "seconds.")
        self.connexion.set_servo_pulsewidth(self.pin, speed)
        if snooze:
            time.sleep(snooze)
        return speed

    def stop(self):
        self.connexion.set_servo_pulsewidth(self.pin, 0)

    def calibrate(self):
        """
        This trains the ESC on the full scale (max - min range) of the controller / pulse generator.
        This only needs to be done when changing controllers, transmitters, etc. not upon every power-on.
        NB: if already calibrated, full throttle will be applied (briefly)!  Disconnect propellers, etc.
        """
        print("Calibrating...")
        self.set_speed(self.max_width)
        input("Connect power and press Enter to calibrate...") 
        self.set_speed(self.max_width, 2) # Official docs: "about 2 seconds".  
        self.set_speed(self.min_width, 4)# Time enough for the cell count, etc. beeps to play.
        print("Finished calibration.")

    # arms the ESC. Required upon every power cycle.
    def arm(self):
        
        print("Arming...", end='')
        self.set_speed(speed=self.min_width, snooze=4)  # Time enough for the cell count, etc. beeps to play.
        print("Done.")


    # switch off the GPIO, and un-arm the ESC.
    # ensure this runs, even on unclean shutdown.
    def quit(self):
        self.set_speed(0)
        self.connexion.stop()
        print("ESC Stopped.")

    # test with a triangularish wave.
    def test(self): 

        # change those values to determine min and max of your ESC
        max_width = self.max_width  # microseconds
        min_width = self.min_width  # microseconds
        step = 200  # microseconds

        delay_btwn_changes = 0.5 # seconds

        input("Press Enter to conduct run-up test...")
        print("Increasing...")
        for width in range(self.min_width, self.max_width, step):
            self.set_speed(width, delay_btwn_changes)

        print("Holding 1 sec at max...")
        time.sleep(1)  # Duration test

        print("Decreasing...")
        for width in range(self.max_width, self.min_width, -step):
            self.set_speed(width, delay_btwn_changes)
            print("speed :", width)