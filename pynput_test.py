from pynput_keyboard import arrows
import time


print("OK")
A = arrows(value = 10)

#A.start_listening()
A.stop_listening()
for i in range(10):
    print(f"value = {A.value}")
    time.sleep(0.5)

#