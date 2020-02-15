import torch
import numpy as np


class ClassificationUNET:
    def __init__(self,
                 path=r"D:\5. ročník\DP\Bitalino\models\rel_good_model_epoch_20_crossEntropyLoss_Adam_optimizer_1024.pth"):
        self.model = torch.load(path)
        self.model.eval()
        self.output = []

    def predict_data(self, emg):
        self.output = self.model(torch.from_numpy(emg).unsqueeze(dim=0).unsqueeze(dim=1).float().cuda())
        self.output = torch.argmax(self.output, dim=1)
        self.output = self.output.detach().cpu().numpy()
        return np.array(self.output)

    """
    def loadModel(path=r"D:\5. ročník\DP\Bitalino\models\rel_good_model_epoch_20_crossEntropyLoss_Adam_optimizer_1024.pth"):
        global model
        model = torch.load(path)
        model.eval()
    
    
    def predict(EMG):
        output = model(torch.from_numpy(EMG).unsqueeze(dim=0).float().unsqueeze(dim=1).float().cuda())
        output = torch.argmax(output, dim=1)
        output = output.detach().cpu().numpy().squeeze().tolist()
        return output
    """
