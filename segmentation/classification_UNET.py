import torch, os
import numpy as np

dir = "./segmentation/unet_model.pth"

class ClassificationUNET:
    def __init__(self, frame_lenght=100,
                 path=dir):
        self.model = torch.load(path)
        self.model.eval()
        self.output = []
        self.signal_length = 512
        self.EMG_record = []
        self.calm_record = []  # 414 samples
        self.EMG_for_NN = []
        self.middle_length = frame_lenght
        self.NN_output_debug = []
        # self.NN_whole_output_debug = []
        self.treshold = -2

    def predict_data(self, emg):
        emg = emg - 507
        if len(self.EMG_record) < self.signal_length:
            self.output = np.zeros(self.middle_length)
            self.EMG_record = np.concatenate([self.EMG_record, emg])
            # self.NN_output_debug = np.concatenate([self.NN_output_debug, self.output])
            if len(self.EMG_record) > 206:
                self.calm_record = self.EMG_record[:206]
        else:
            self.EMG_for_NN = np.concatenate([self.EMG_record[-206:], emg, self.calm_record])
            self.EMG_record = np.concatenate([self.EMG_record, emg])
            self.EMG_for_NN = torch.from_numpy(self.EMG_for_NN).unsqueeze(dim=0)
            output_net = self.model(self.EMG_for_NN.unsqueeze(dim=1).float().cuda())
            """
            output_net[0, 1, :] = output_net[0, 1, :] + 8
            output = torch.argmax(output_net, dim=1)
            output = output[0, :].detach().cpu().numpy()
            self.output = output[206:306]
            """
            output = output_net[0, 1, :].detach().cpu().numpy()
            output = output[206:306]
            # self.NN_output_debug = output_net
            # NN_whole_output_debug = output_net[0, 0, :].detach().cpu().numpy()
            # NN_whole_output_debug = NN_whole_output_debug[500:600]
            # self.NN_output_debug = np.concatenate([self.NN_output_debug, output])
            # self.NN_whole_output_debug = np.concatenate([self.NN_whole_output_debug, NN_whole_output_debug])

            tresh = np.where(output *1.2 > self.treshold)
            self.output = np.zeros(self.middle_length)
            self.output[tresh] = 1
        return self.output
