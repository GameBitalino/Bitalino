import time
import bitalino
import numpy as np
import pyqtgraph as pg
from matplotlib import pyplot as plt
from saveData import saveEMG
import torch
from BITalino import BITalino

model = torch.load(r"D:\5. ročník\DP\Bitalino\models\rel_good_model_epoch_20_crossEntropyLoss_Adam_optimizer_1024.pth")
model.eval()

minutes = 1  # how long you want to measure
device = BITalino(minutes * 60, 512)
device.start_recording()
predicted = []

try:
    start = time.time()
    while True:
        EMG = device.read_data()  # read nFrames from Bitalino
        for i in range(len(EMG)):
            EMG[i] = EMG[i] - 507
        EMG_for_NN = torch.from_numpy(EMG).unsqueeze(dim=0).float()
        output = model(EMG_for_NN.unsqueeze(dim=1).float().cuda())
        output = torch.argmax(output, dim=1)
        output = output.detach().cpu().numpy().squeeze().tolist()
        predicted = np.concatenate([predicted, output])
        end = time.time()
        if (end - start) > device.running_time:
            break
finally:
    device.stop_recording()
    plt.plot(device.emg_full_record, 'b')
    plt.plot(predicted * 100, 'r')
    plt.show()
