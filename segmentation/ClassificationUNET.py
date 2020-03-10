import torch
import numpy as np


class ClassificationUNET:
    def __init__(self, frame_lenght=100,
                 path=r"D:\5. ročník\DP\Bitalino\models\model_epoch_50CrossEntropyLoss_Adam_optimizer_1024_05_03_2020.pth"):
        self.model = torch.load(path)
        self.model.eval()
        self.output = []
        self.signal_length = 1024
        self.EMG_record = []
        self.calm_record = []  # 414 samples
        self.EMG_for_NN = []
        self.middle_length = frame_lenght

    def predict_data(self, emg):
        emg = emg - 507
        if len(self.EMG_record) < self.signal_length:
            self.output = np.zeros(self.middle_length)
            self.EMG_record = np.concatenate([self.EMG_record, emg])
            if len(self.EMG_record) > 424:
                self.calm_record = self.EMG_record[:424]
        else:
            self.EMG_for_NN = np.concatenate([self.EMG_record[-500:], emg, self.calm_record])
            self.EMG_for_NN = torch.from_numpy(self.EMG_for_NN).unsqueeze(dim=0)

            output = self.model(self.EMG_for_NN.unsqueeze(dim=1).float().cuda())
            output = output[0, 1, :].detach().cpu().numpy()
            output = output[500:600]
            tresh = np.where(output * 1.2 > - 6)
            self.output = np.zeros(self.middle_length)
            self.output[tresh] = 1
        return self.output
