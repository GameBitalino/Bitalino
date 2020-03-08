import numpy as np
import pandas as pd
import torch
from classification.LoadData import LoadData
import matplotlib.pyplot as plt

SIGNAL_LENGTH = 1024
loader = LoadData()
path = r"D:\5. ročník\DP\recordings\EMG_date_24_01_2020_time_17_04_13"

"""
labels[4930:5450] = 1
labels[8954:9465] = 1
labels[13270:13640] = 1
labels[17140:17578] = 1
labels[20773:21202] = 1
labels[24050:24600] = 1
labels[28085:29155] = 1
"""

time, emg = loader.load_record(path + ".csv")
plt.plot(emg)
plt.show()

net = torch.load(r"D:\5. ročník\DP\Bitalino\models\model_epoch_50CrossEntropyLoss_Adam_optimizer_1024_05_03_2020.pth")


part = np.array(emg[17000:18024])
EMG_for_NN = torch.from_numpy(part).unsqueeze(dim=0)
output = net(EMG_for_NN.unsqueeze(dim=1).float().cuda())

t = output[0, 1, :].detach().cpu().numpy()
t1 = np.where(t * 1.2 > -0.2)
t2 = np.where(t * 1.2 > -0.1)
novy = np.zeros(SIGNAL_LENGTH)
novy2 = np.zeros(SIGNAL_LENGTH)
novy[t1] = 50
novy2[t2] = 70

prediction = torch.argmax(output, dim=1)
prediction = prediction[0, :].detach().cpu().numpy() * 70

plt.plot(np.array(part))
plt.plot(novy2, "r", label="pokus")
plt.plot(novy, "g")
# plt.plot(prediction, "r")
plt.show()
