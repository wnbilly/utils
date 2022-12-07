#!/usr/bin/env python3

import time
import pigpio
from commands_keyboard import arrows    
from ESC_class import ESC

if __name__ == "__main__":

    min_width = 1000
    max_width = 2000
    esc = ESC(pin=4, min_width=min_width, max_width=max_width)
    esc2 = ESC(pin=17, min_width=min_width, max_width=max_width)

    init_speed = 1100
    speed_step = 20
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
