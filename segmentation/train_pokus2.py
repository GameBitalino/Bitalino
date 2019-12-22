from segmentation.UNet import UNetModel
from matplotlib import pyplot as plt
import numpy as np
from scipy.io import savemat
import torch
from torch.nn import CrossEntropyLoss
from torch.optim import SGD
from segmentation.loader import DataLoader
from tqdm import tqdm  # progressbar
from torch.autograd import Variable


class TrainUNetModel:
    def __init__(self):
        self.model = UNetModel()
        self.model.cuda()
        self.loss = CrossEntropyLoss()
        self.optimizer = SGD(self.MODEL.parameters(), lr=self.LEARNING_RATE, momentum=self.MOMENTUM)

        self.loader_val = None
        self.loader_train = None

        self.NUM_CLASSES = 2
        self.BATCH_SIZE = 2
        self.NUMBER_OF_EPOCHS = 100
        self.LEARNING_RATE = 1e-3
        self.MOMENTUM = 0.9
        self.loader_train = None
        self.iter = 0
        # load data
        self.dataset = DataLoader("train_data")
        self.trainLoader = torch.utils.data.DataLoader(self.dataset, batch_size=self.BATCH_SIZE, num_workers=0,
                                                       shuffle=True,
                                                       drop_last=True)
        self.dataset = DataLoader("test_data")
        self.testLoader = torch.utils.data.DataLoader(self.dataset, batch_size=self.BATCH_SIZE, num_workers=0,
                                                      shuffle=True,
                                                      drop_last=True)

    def train(self):
        self.model.train()
        train_loss = []
        test_loss = []
        train_acc = []
        test_acc = []
        position = []
        train_acc_tmp = []
        train_loss_tmp = []
        test_acc_tmp = []
        test_loss_tmp = []

        it = -1
        for epoch in range(self.NUMBER_OF_EPOCHS):
            tqdm_loader = tqdm(self.loader_train)
            for data in tqdm_loader:
                it += 1
                signal, labels, indices, img_path, mask_path = data
                self.optimizer.zero_grad()
                signal = Variable(signal, requires_grad=True)
                labels = Variable(labels, requires_grad=True)
                signal = signal.cuda()
                labels = labels.cuda()

                output = self.model(signal)
                prediction = torch.argmax(output, dim=1)
                loss = self.loss(output, labels)
                loss.backward()
                self.optimizer.step()
                clas = (output > 0.5).float()

                acc = torch.mean((clas == labels).float())

                train_acc_tmp.append(acc.detach().cpu().numpy())
                train_loss_tmp.append(loss.detach().cpu().numpy())
                if it % 50 == 0:
                    for kk, (data, lbl) in enumerate(self.testLoader):
                        data = data.cuda()
                        lbl = lbl.cuda()

                        data.requires_grad = True
                        lbl.requires_grad = True
                        self.optimizer.zero_grad()
                        output = self.model(data)
                        loss = self.loss(output, lbl)
                        clas = (output > 0.5).float()
                        acc = torch.mean((clas == lbl).float())
                        test_acc_tmp.append(acc.detach().cpu().numpy())
                        test_loss_tmp.append(loss.detach().cpu().numpy())

                        d = data[0, 0, :, :].detach().cpu().numpy()
                        r = output[0, 0, :, :].detach().cpu().numpy()
                        g = lbl[0, 0, :, :].detach().cpu().numpy()
                        plt.plot(np.concatenate((d, r, g), axis=1), cmap='gray', vmin=0, vmax=1)
                        plt.show()


if __name__ == "__main__":
    TrainUNetModel()