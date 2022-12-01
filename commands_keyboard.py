from pynput import keyboard
import time

# made for ESC control via keyboard
class arrows:

    def __init__(self, value = 0, step = 0.1, min = 0, max = 1) -> None:
        self.value = value #value controlled by the arrows
        self.init_value = value
        # up or right to increase
        # down or left to decrease
        self.step = step # the amount of wich the value will be increased or decreased 
        self.min = min
        self.max = max

        self.KEYS_INCREASE = [keyboard.Key.up, keyboard.Key.right]
        self.KEYS_DECREASE = [keyboard.Key.down, keyboard.Key.left]
        self.KEYS_RESET = [keyboard.Key.space]
        self.KEYS_STOP = [keyboard.Key.esc]
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)

    def on_press(self, key):
        if key in self.KEYS_INCREASE:
            self.value = min(self.value+self.step, self.max)

        if key in self.KEYS_DECREASE:
            self.value = max(self.value-self.step, self.min)

        if key in self.KEYS_RESET:
            self.value = self.init_value

        if key in self.KEYS_STOP:
            self.value = 0
<<<<<<< HEAD
=======
        print(self.value)
>>>>>>> 68e539804e1f6ff9bf17204d7c5883e664f9af30


    def on_release(self, key):
        pass

    def start_listening(self): # start a thread that will listen to the keyboard
        self.listener.start()

    def stop_listening(self): # stop the created thread
        self.listener.stop()