import bitalino
import numpy as np
from matplotlib import pyplot as plt
import time
import datetime
from pynput.mouse import Controller

mouse = Controller()
press_time = []

from pynput import mouse


def on_click(x, y, button, pressed):
    press_time.append(datetime.datetime.now())
    # press_time.append(time.time())
    print('{0} at {1}'.format(
        'Pressed' if pressed else 'Released',
        (x, y)))
    if not pressed:
        # Stop listener
        return False


# Collect events until released
with mouse.Listener(
        on_click=on_click
) as listener:
    listener.join()

fvz = 1000
nframes = 100
EMG_record = []
keyboard_press = []
running_time = 10

# connect Bitalino
macAddress = "20:18:06:13:21:59"
device = bitalino.BITalino(macAddress)
time.sleep(1)
print("START")

# ...or, in a non-blocking fashion:
listener = mouse.Listener(
    on_click=on_click)
listener.start()

start = time.time()
device.start(fvz, [0])
# after_start = time.time()
start_time = device.startTime
try:
    while True:
        data = device.read(nframes)  # read nFrames from Bitalino
        EMG = data[:, -1]
        EMG_record = np.concatenate([EMG_record, EMG])
        end = time.time()
        if (end - start) > running_time:
            break
finally:
    device.stop()
    print("STOP")
    device.close()
    plt.plot(EMG_record)
    plt.show()

# output from first time: 252 millisec / from second time: 50 millisec
