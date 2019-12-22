import numpy as np
import torch
import pandas as pd
import matplotlib.pyplot as plt
import glob
from skimage.io import imread
from torch.utils import data


class DataLoader(data.Dataset):
    def __init__(self, dataFolder, path_to_data=r"D:\5. ročník\DP\Bitalino\recordings"):
        self.path = path_to_data + "/" + dataFolder
        # vime ze slozky od 0 do 9
        self.files = []
        self.labels = []
        cvs_files = glob.glob(self.path + '/signal/*.csv')  # vrati list souboru, ktere jsou uvnitr slozky
        self.files = self.files + cvs_files
        cvs_labels = glob.glob(self.path + '/labels/*.csv')
        self.labels = cvs_labels
        self.num_of_signals = len(self.files)

    def __len__(self):
        return self.num_of_signals

    # pocet vzorku do batche X konvolucni vrstvy X velikost obrazku (mxn) - bacth vytvori samo
    def __getitem__(self, index):
        sig = self.files[index]
        print(sig)
        sig = pd.read_csv(sig, delimiter=',',
                          decimal=".")
        sig = np.array(sig)
        print(sig)
        m = sig.shape[0]
        n = sig.shape[1]
        print(m,n)
        sig = sig.reshape((1, m, n))
        sig = sig.astype(np.float32)
        # prevod na tensor
        sig = torch.from_numpy(sig)
        label = self.labels[index]
        label = pd.read_csv(label, delimiter=',', decimal=".")
        label = np.array(label)
        lbl = torch.from_numpy(label.astype(np.float32))
        return sig, lbl


loader = DataLoader("train_data")
trainLoader = data.DataLoader(loader, batch_size=2, num_workers=0, shuffle=True, drop_last=True)
loader.files

for it,(batch,lbls) in enumerate(trainLoader): ### you can iterate over dataset (one epoch)
  print("batch ", batch)
  print("batch size: ", batch.size())
  print("max - the position of label", np.argmax(lbls.detach().cpu().numpy(),axis=1))
  plt.plot(batch[0,0,:,:].detach().cpu().numpy())
  plt.show()
  break
