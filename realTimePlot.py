import time

import bitalino
import numpy as np
import pyqtgraph as pg
from matplotlib import pyplot as plt

from saveData import saveEMG
import torch

model = torch.load(r"D:\5. ročník\DP\Bitalino\models\rel_good_model_epoch_20_crossEntropyLoss_Adam_optimizer_1024.pth")
model.eval()

# set parameters
fvz = 1000
nframes = 1024
threshold = 5
minutes = 0.1  # how long you want to measure
num_frames_plot = 10  # every e.g.. tenth sample will be draw in real time graph

# connect Bitalino
macAddress = "20:18:06:13:21:59"
device = bitalino.BITalino(macAddress)
time.sleep(1)
device.start(fvz, [0])
print("START")

# initialize values
EMG_record = []
running_time = 60 * minutes  # in seconds
iteration = 0
x_vec = np.linspace(0, minutes * 60, int(running_time * fvz / num_frames_plot))
y_vec = np.zeros(len(x_vec))  # only for nicer plot
prediction = y_vec

# main loop
try:
    win = pg.GraphicsWindow()
    win.setWindowTitle('DOTS')
    p1 = win.addPlot()
    # set figure for plot
    curve = p1.plot()
    """
    curve.setWindowTitle('EMG')
    curve.setTitle('<font size="5">EMG záznam</font>')
    curve.setLabel(axis='bottom', text='<font size="5">Čas [s]')
    curve.setLabel(axis='left', text='<font size="5">Napětí [μV]')
    curve.setYRange(0, 1000)
    """
    curve2 = p1.plot()
    # start
    start = time.time()
    while True:
        data = device.read(nframes)  # read nFrames from Bitalino
        EMG = data[:, -1]
        EMG_record = np.concatenate([EMG_record, EMG])
        EMG_for_NN = torch.from_numpy(EMG).unsqueeze(dim=0).float()
        output = model(EMG_for_NN.unsqueeze(dim=1).float().cuda())
        output = torch.argmax(output, dim=1)
        output.detach().cpu().numpy()
        # plot real time graph
        float_count_samples = int(nframes / num_frames_plot)
        float_window = 100
        if (np.shape(y_vec[(iteration * float_count_samples):((iteration + 1) * float_count_samples)])[0]) < 10:
            break
        else:
            y_vec[(iteration * float_count_samples):((iteration + 1) * float_count_samples)] = EMG[0::num_frames_plot]
            prediction[(iteration * float_count_samples):((iteration + 1) * float_count_samples)] = output[
                                                                                                    0::num_frames_plot]
        # y_vec[(iteration * float_count_samples):((iteration + 1) * float_count_samples)] = EMG[0::num_frames_plot]

        if iteration <= float_window:  # collect start data
            # curve.plot(x_vec[0:(float_count_samples * float_window)],
            #           y_vec[0:(float_count_samples * float_window)], clear=True, pen="r")
            curve.setData(x_vec[0:(float_count_samples * float_window)],
                          y_vec[0:(float_count_samples * float_window)], clear=True, pen="r")
            curve2.setData(x_vec[0:(float_count_samples * float_window)],
                           prediction[0:(float_count_samples * float_window)], clear=True, pen="g")
        else:
            """
            curve.plot(
                x_vec[((iteration - float_window) * float_count_samples):(iteration * float_count_samples)],
                y_vec[((iteration - float_window) * float_count_samples): (iteration * float_count_samples)],
                clear=True, pen='r')
                """
            curve.setData(
                x_vec[((iteration - float_window) * float_count_samples):(iteration * float_count_samples)],
                y_vec[((iteration - float_window) * float_count_samples): (iteration * float_count_samples)],
                clear=True, pen='r')
            curve2.setData(
                x_vec[((iteration - float_window) * float_count_samples):(iteration * float_count_samples)],
                prediction[((iteration - float_window) * float_count_samples): (iteration * float_count_samples)],
                clear=True, pen='g')
        pg.QtGui.QGuiApplication.processEvents()
        iteration += 1

        # stop recording
        end = time.time()
        if (end - start) > running_time:
            pg.QtGui.QGuiApplication.exec()
            break

finally:
    print("STOP")
    device.stop()
    device.close()

    # subtract mean value
    meanValue = np.mean(EMG_record)
    for i in range(len(EMG_record)):
        EMG_record[i] -= meanValue

    # save current data
    time = np.linspace(0, int(running_time), len(EMG_record))
    saveEMG(time, EMG_record)

    # plot EMG record
    plt.style.use("ggplot")
    plt.plot(time, EMG_record)
    plt.title("EMG")
    plt.xlabel("čas [s]")
    plt.ylabel("napětí [μV]")
    plt.show()
