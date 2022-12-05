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
        self.connexion = pigpio.pi() # initialise pigpio instance
        self.pin = pin # GPIO pin to which the ESC is connected
        self.min_width = min_width # max width of the PWM (depends on the ESC or motor)
        self.max_width = max_width # min width of the PWM (depends on the ESC or motor)
        self.speed = (self.min_width + self.max_width)//2 # initial speed set to the middle between min and max
        self.connexion.set_servo_pulsewidth(self.pin, self.speed) # initialise PWM connexion and set the speed to self.speed


    def start(self, init_speed = 1200):
        step = 10 # size of steps from min_width to init_speed, lower to have a smoother start
        delay_btwn_changes = 0.1 # seconds  delay to hold each stop, increase to have more gentle start
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
        self.speed = speed
        if snooze:
            time.sleep(snooze)
        return speed

    def stop(self):
        self.connexion.set_servo_pulsewidth(self.pin, 0)

    # TO DO : CONTINUOUSLY UPDATE self.speed UNTIL stop_kb_commands called
    def start_kb_commands(self, speed_step=20):
        # value is the value to start
        self.commands = arrows(value=self.speed, step=speed_step, min=self.min_width, max=self.max_width)
        self.commands.start_listening()

    def stop_kb_commands(self):
        if self.commands : self.commands.stop_listening()

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
        step = 200  # microseconds
        delay_btwn_changes = 0.5 # seconds

        input("Press Enter to conduct run-up test...")
        print("Increasing...")
        
        for width in range(self.min_width, self.max_width, step):
            self.set_speed(width, delay_btwn_changes)
            print("speed :", width)

        print("Holding 1 sec at max...")
        time.sleep(1)  # Duration test

        print("Decreasing...")
        for width in range(self.max_width, self.min_width, -step):
            self.set_speed(width, delay_btwn_changes)
            print("speed :", width)


if __name__ == "__main__":

    min_width = 1000
    max_width = 2000
    esc = ESC(pin=4, min_width=min_width, max_width=max_width)
    esc2 = ESC(pin=17, min_width=min_width, max_width=max_width)

    speed_step = 20
    init_speed = 1100
    commands = arrows(value=init_speed, step=speed_step, min=min_width, max=max_width)
    commands.start_listening()
    esc.arm()         # Required upon every power-up
    esc2.arm()
    esc.start(init_speed)
    esc2.start(init_speed)
    try:
        # esc.calibrate()  # Recommended when changing "transmitter" or controller
        # esc.arm()         # Required upon every power-up
        # esc.test()        # Run-up test
        while True:
            print((commands.value-min_width)/(max_width-min_width)*100)
            esc.set_speed(commands.value)
            esc2.set_speed(commands.value)
    except KeyboardInterrupt:
        pass
    finally:
        commands.stop_listening()
        esc.quit()
        esc2.quit()
