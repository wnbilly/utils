from pynput import keyboard
import time

class arrows:

    def __init__(self, value = 0, step = 1) -> None:
        self.value = value #value controlled by the arrows 
        # up or right to increase
        # down or left to decrease
        self.step = step # the amount of wich the value will be increased or decreased 

        self.KEYS_INCREASE = [keyboard.Key.up, keyboard.Key.right]
        self.KEYS_DECREASE = [keyboard.Key.down, keyboard.Key.left]

    def on_press(self, key):
        if any([key in self.KEYS_INCREASE]):
            self.value += self.step

        if any([key in self.KEYS_DECREASE]):
            self.value -= self.step

    def on_release(self, key):
        pass

    def start_listening(self):
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()

    def stop_listening(self):
        pass


A = arrows(value = 10)

A.start_listening()

for i in range(100):
    print(i + A.value)
    time.sleep(1)