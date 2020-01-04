import pygame, bitalino, time
import matplotlib.pyplot as plt
import numpy as np
import datetime

"""
pygame.init()


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

start = time.time()
device.start(fvz, [0])

# after_start = time.time()
start_time = device.startTime
try:
    while True:
        for event in pygame.event.get():
            if event.type == pygame.K_SPACE:
                print("now")
                keyboard_press.append(datetime.datetime.now())
        print(pygame.key.get_pressed())
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

"""

from pynput import keyboard
import bitalino
from matplotlib import pyplot as plt
import time
import datetime
import numpy as np

press_time = []


def on_press(key):
    press_time.append(datetime.datetime.now())
    print("Detected key press: ", key)
    if key == keyboard.Key.esc:
        # Stop listener
        return False


# Collect events until rele  ased

lis = keyboard.Listener(on_press=on_press)

fvz = 1000
running_time = 10
nframes = fvz * running_time
EMG_record = []

# connect Bitalino
macAddress = "20:18:06:13:21:59"
device = bitalino.BITalino(macAddress)
time.sleep(1)
print("START")

# listener.start()

start = time.time()
device.start(fvz, [0])

lis.start()
lis.join()
# after_start = time.time()
start_time = device.startTime
while True:
    end = time.time()
    if (end - start) > running_time:
        data = device.read(nframes)  # read nFram es from Bitalino
        print("read")
        EMG = data[:, -1]
        EMG_record = np.concatenate([EMG_record, EMG])
        device.stop()
        print("STOP")
        device.close()
        plt.plot(EMG_record)
        plt.show()



