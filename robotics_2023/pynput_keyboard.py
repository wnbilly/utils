from pynput import keyboard
import time

class arrows:

    def __init__(self, value = 0, step = 1) -> None:
        self.value = value #value controlled by the arrows
        self.init_value = value
        # up or right to increase
        # down or left to decrease
        self.step = step # the amount of wich the value will be increased or decreased 

        self.KEYS_INCREASE = [keyboard.Key.up, keyboard.Key.right]
        self.KEYS_DECREASE = [keyboard.Key.down, keyboard.Key.left]
        self.KEYS_RESET = [keyboard.Key.space]
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)

    def on_press(self, key):
        if key in self.KEYS_INCREASE:
            self.value += self.step

        if key in self.KEYS_DECREASE:
            self.value -= self.step

        if key in self.KEYS_RESET:
            self.value = self.init_value

    def on_release(self, key):
        pass

    def start_listening(self): # start a thread that will listen to the keyboard
        self.listener.start()

    def stop_listening(self): # stop the created thread
        self.listener.stop()