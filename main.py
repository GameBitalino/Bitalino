import time
from BITalino import BITalino
import matplotlib.pyplot as plt
import numpy
import pyqtgraph as pg
import numpy as np

# set parameters

minutes = 0.1  # how long you want to measure
num_frames_plot = 10  # every e.g.. tenth sample will be draw in real time graph

# connect Bitalino
device = BITalino(time=minutes)
device.start_recording()
float_count_samples = int(device.nframes / num_frames_plot)

# initialize values
running_time = 60 * minutes  # in seconds
iteration = 0
x_vec = numpy.linspace(0, minutes * 60, int(running_time * device.fvz / num_frames_plot))
y_vec = numpy.zeros(len(x_vec))  # only for nicer plot

# main loop
try:
    # set figure for plot
    curve = pg.plot()
    curve.setWindowTitle('EMG')
    curve.setTitle('<font size="5">EMG záznam</font>')
    curve.setLabel(axis='bottom', text='<font size="5">Čas [s]')
    curve.setLabel(axis='left', text='<font size="5">Napětí [μV]')
    curve.setYRange(0, 1000)
    # start
    start = time.time()
    while True:
        EMG = device.read_data()  # read nFrames from Bitalino
        EMG_record = device.get_recording()

        # plot real time graph

        float_window = 100
        if (np.shape(y_vec[(iteration * float_count_samples):((iteration + 1) * float_count_samples)])[0]) < 10:
            break
        else:
            y_vec[(iteration * float_count_samples):((iteration + 1) * float_count_samples)] = EMG[0::num_frames_plot]
        if iteration <= float_window:  # collect start data
            curve.plot(x_vec[0:(float_count_samples * float_window)],
                       y_vec[0:(float_count_samples * float_window)], clear=True, pen="r")
        else:
            curve.plot(
                x_vec[((iteration - float_window) * float_count_samples):(iteration * float_count_samples)],
                y_vec[((iteration - float_window) * float_count_samples): (iteration * float_count_samples)],
                clear=True, pen='r')
        pg.QtGui.QGuiApplication.processEvents()
        iteration += 1

        # stop recording
        end = time.time()
        if (end - start) > running_time:
            pg.QtGui.QGuiApplication.exec()
            break

finally:
    device.stop_recording()
    device.save_data()
