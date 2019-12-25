from segmentation.UNet import UNetModel
from matplotlib import pyplot as plt
import numpy as np
from scipy.io import savemat
import torch
from torch.nn import CrossEntropyLoss
from torch.optim import SGD
import torch.nn.functional as F
from segmentation.loader import DataLoader
from torch.autograd import Variable

BATCH_SIZE = 1
LEARNING_RATE = 0.001
NUMBER_OF_EPOCH = 20
LOSS_FUNCTION = CrossEntropyLoss()

#def LOSS_FUNCTION(out, labels):
#    return -torch.mean(labels * torch.log(out))

loaderTrain = DataLoader('train_data')
trainLoader = torch.utils.data.DataLoader(loaderTrain, batch_size=BATCH_SIZE, num_workers=0, shuffle=True,
                                          drop_last=True)

loaderTest = DataLoader('test_data')
testLoader = torch.utils.data.DataLoader(loaderTest, batch_size=BATCH_SIZE, num_workers=0, shuffle=True, drop_last=True)

net = UNetModel().cuda()
OPTIMIZER = SGD(net.parameters(), lr=LEARNING_RATE, weight_decay=1e-8)

print("after load data")
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
for epoch in range(NUMBER_OF_EPOCH):
    for k, (data, lbl) in enumerate(trainLoader):
        it += 1
        print(it)

        data = data.cuda()
        lbl = lbl.cuda()

        data.requires_grad = True
        lbl.requires_grad = True
        data = Variable(data, requires_grad=True)
        lbl = Variable(lbl, requires_grad=True)
        OPTIMIZER.zero_grad()  # zero the gradient buffers
        net.train()
        print("after train")
        data = data.reshape((1, 1, 512))
        lbl = lbl.reshape((1, 1, 512))
        output = net(data)
        print("after output")
        prediction = torch.argmax(output, dim=1)
        # output = torch.sigmoid(output)
        # print("after sigmoid")
        loss = LOSS_FUNCTION(output, lbl)
        loss.backward()
        OPTIMIZER.step()
        clas = (output > 0.5).float()
        acc = torch.mean((clas == lbl).float())
        train_acc_tmp.append(acc.detach().cpu().numpy())
        train_loss_tmp.append(loss.detach().cpu().numpy())

        if it % 5 == 0:
            d = data[0, :, :].detach().cpu().numpy()
            r = output[0, :, :].detach().cpu().numpy()
            g = lbl[0, :, :].detach().cpu().numpy()
            plt.plot(d, 'b')
            plt.plot(r, 'r')
            plt.plot(g, 'g')
            plt.show()

            for kk, (data, lbl) in enumerate(testLoader):
                data = data.cuda()
                lbl = lbl.cuda()

                data.requires_grad = True
                lbl.requires_grad = True

                OPTIMIZER.zero_grad()  # zero the gradient buffers

                net.eval()

                output = net(data)
                output = F.sigmoid(output)

                loss = CrossEntropyLoss(output, lbl)

                clas = (output > 0.5).float()

                acc = torch.mean((clas == lbl).float())

                test_acc_tmp.append(acc.detach().cpu().numpy())
                test_loss_tmp.append(loss.detach().cpu().numpy())

                d = data[0, 0, :, :].detach().cpu().numpy()
                r = output[0, 0, :, :].detach().cpu().numpy()
                g = lbl[0, 0, :, :].detach().cpu().numpy()
                plt.plot(d, 'b')
                plt.plot(r, 'r')
                plt.plot(g, 'g')
                plt.show()

            train_loss.append(np.mean(train_loss_tmp))
            test_loss.append(np.mean(test_loss_tmp))
            train_acc.append(np.mean(train_acc_tmp))
            test_acc.append(np.mean(test_acc_tmp))
            position.append(it)

            train_acc_tmp = []
            train_loss_tmp = []
            test_acc_tmp = []
            test_loss_tmp = []

            plt.plot(position, train_loss)
            plt.plot(position, test_loss)
            plt.show()

            plt.plot(position, train_acc)
            plt.plot(position, test_acc)
            plt.show()
