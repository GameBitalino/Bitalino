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
        # self.NN_output_debug = []
        # self.NN_whole_output_debug = []
        self.treshold = -2

    def predict_data(self, emg):
        emg = emg - 507
        if len(self.EMG_record) < self.signal_length:
            self.output = np.zeros(self.middle_length)
            self.EMG_record = np.concatenate([self.EMG_record, emg])
            # self.NN_output_debug = np.concatenate([self.NN_output_debug, self.output])
            if len(self.EMG_record) > 424:
                self.calm_record = self.EMG_record[:424]
        else:
            self.EMG_for_NN = np.concatenate([self.EMG_record[-500:], emg, self.calm_record])
            self.EMG_record = np.concatenate([self.EMG_record, emg])
            self.EMG_for_NN = torch.from_numpy(self.EMG_for_NN).unsqueeze(dim=0)
            output_net = self.model(self.EMG_for_NN.unsqueeze(dim=1).float().cuda())
            output = output_net[0, 1, :].detach().cpu().numpy()
            output = output[500:600]
            # NN_whole_output_debug = output_net[0, 0, :].detach().cpu().numpy()
            # NN_whole_output_debug = NN_whole_output_debug[500:600]
            # self.NN_output_debug = np.concatenate([self.NN_output_debug, output])
            # self.NN_whole_output_debug = np.concatenate([self.NN_whole_output_debug, NN_whole_output_debug])
            tresh = np.where(output * 1.2 > self.treshold)
            self.output = np.zeros(self.middle_length)
            self.output[tresh] = 1
        return self.output
