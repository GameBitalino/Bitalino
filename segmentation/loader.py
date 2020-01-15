import numpy as np
import torch
import pandas as pd
import glob
from torch.utils import data


class DataLoader(data.Dataset):
    def __init__(self, dataFolder, path_to_data=r"D:\5. ročník\DP\Bitalino\recordings"):
        self.path = path_to_data + "/" + dataFolder
        # vime ze slozky od 0 do 9
        self.files = []
        self.labels = []
        cvs_files = glob.glob(self.path + '/signal/*.csv')  # list of csv in folder
        self.files = self.files + cvs_files
        cvs_labels = glob.glob(self.path + '/labels/*.csv')
        self.labels = cvs_labels
        self.num_of_signals = len(self.files)

    def __len__(self):
        return self.num_of_signals

    # pocet vzorku do batche X konvolucni vrstvy X velikost obrazku (mxn) - bacth vytvori samo
    def __getitem__(self, index):
        sig = self.files[index]
        sig = pd.read_csv(sig, delimiter=',',
                          decimal=".")
        sig = np.array(sig)[:512]
        sig = torch.from_numpy(np.squeeze(sig))
        label = self.labels[index]
        label = pd.read_csv(label, delimiter=',', decimal=".")
        label = np.array(label)[:512]
        lbl = torch.from_numpy(label.astype(np.float32))
        return sig.unsqueeze(dim=0).float(), lbl.squeeze().long()
