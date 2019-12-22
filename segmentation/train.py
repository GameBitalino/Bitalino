from .UNet import *
from matplotlib import pyplot as plt
import numpy as np
from scipy.io import savemat
import torch
from torch.nn import CrossEntropyLoss
from torch.optim import SGD
from .loader import DataLoader
from tqdm import tqdm  # progressbar


class TrainUNetModel:
    def __init__(self):
        self.model = None
        self.NUM_CLASSES = 2
        self.BATCH_SIZE = 2
        self.STRIDE = 0.2
        self.STRIDE_VAL = 0.2
        self.STRIDE_LIMIT = (1000, 1.)  # THIS PREVENTS DATASET HALTING
        self.NUMBER_OF_EPOCHS = 100
        self.LEARNING_RATE = 1e-3
        self.FOLDER_WITH_IMAGE_DATA = "./recordings/"
        self.MODEL = UNetModel()
        self.OPTIMIZER = SGD(self.MODEL.parameters(), lr=self.LEARNING_RATE, momentum=self.MOMENTUM)
        self.VALIDATION_FREQUENCY = 2  # num epochs
        self.CUDA = True
        self.MOMENTUM = 0.9
        self.loader_train = None
        self.iter = 0
        # load data
        self.dataset = DataLoader("train_data")
        self.trainLoader = torch.utils.data.DataLoader(self.dataset, batch_size=self.BATCH_SIZE, num_workers=0,
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

        for epoch in range(self.NUMBER_OF_EPOCHS):
            for it, (data, lbl) in enumerate(self.trainLoader):
                self.iter += 1
                print(self.iter)

                data = data.cuda()
                lbl = lbl.cuda()
                data.requires_grad = True
                lbl.requires_grad = True

                self.OPTIMIZER.zero_grad()
                prediction = torch.softmax(self.MODEL(data), dim=1)
                loss = CrossEntropyLoss(prediction, lbl)
                loss.backward()
                self.OPTIMIZER.step()
                train_loss.append(loss.detach().cpu().numpy())
                lbl_num = np.argmax(lbl.detach().cpu().numpy(), axis=1)
                predict = np.argmax(prediction.detach().cpu().numpy(), axis = 1)
                acc = np.mean((predict == lbl_num))
                train_acc_tmp.append(acc)
                train_loss_tmp.append(loss.detach().cpu().numpy())

    #def test(self):
