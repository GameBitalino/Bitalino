import numpy as np
import torch
import pandas as pd
import glob
from torch.utils import data


class DataLoader(data.Dataset):
    def __init__(self, dataFolder, signal_length=512, path_to_data=r"D:\5. ročník\DP\Bitalino\recordings"):
        self.signal_length = signal_length
        self.path = path_to_data + "/" + dataFolder
        # vime ze slozky od 0 do 9
        self.files = []
        cvs_files = glob.glob(self.path + '/*.csv')  # list of csv in folder
        self.files = self.files + cvs_files
        self.num_of_signals = len(self.files)

    def __len__(self):
        return self.num_of_signals

    # pocet vzorku do batche X konvolucni vrstvy X velikost signalu - bacth vytvori samo
    def __getitem__(self, index):
        file = self.files[index]
        file = pd.read_csv(file, delimiter=',',
                           decimal=".")
        file = np.array(file)[:self.signal_length]
        sig = file[0, :]
        sig = torch.from_numpy(np.squeeze(sig))
        label = file[1, :]
        lbl = torch.from_numpy(label.astype(np.float32))
        return sig.unsqueeze(dim=0).float(), lbl.squeeze().long()
