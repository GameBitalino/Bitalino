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
nframes = 512
threshold = 5
minutes = 1  # how long you want to measure

running_time = minutes * 60

macAddress = "20:18:06:13:21:59"
device = bitalino.BITalino(macAddress)
time.sleep(1)
device.start(fvz, [0])
print("START")

EMG_record = []
predicted = []
try:
    start = time.time()
    while True:
        data = device.read(nframes)  # read nFrames from Bitalino
        EMG = data[:, -1]

        for i in range(len(EMG)):
            EMG[i] = EMG[i] - 507
        EMG_record = np.concatenate([EMG_record, EMG])
        EMG_for_NN = torch.from_numpy(EMG).unsqueeze(dim=0).float()
        output = model(EMG_for_NN.unsqueeze(dim=1).float().cuda())
        output = torch.argmax(output, dim=1)
        output = output.detach().cpu().numpy().squeeze().tolist()
        predicted = np.concatenate([predicted, output])
        end = time.time()
        if (end - start) > running_time:
            break
finally:
    print("STOP")
    device.stop()
    device.close()
    plt.plot(EMG_record, 'b')
    plt.plot(predicted*100, 'r')
    plt.show()