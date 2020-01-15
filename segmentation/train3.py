from segmentation.UNet import UNetModel
from matplotlib import pyplot as plt
import numpy as np
import torch
from torch.nn import CrossEntropyLoss
from torch.optim import SGD
import torch.nn.functional as F
from segmentation.loader import DataLoader
from torch.autograd import Variable

BATCH_SIZE = 1
LEARNING_RATE = 0.001
NUMBER_OF_EPOCH = 200
LOSS_FUNCTION = CrossEntropyLoss()

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

        # data = Variable(data, requires_grad=True)
        # lbl = Variable(lbl, requires_grad=True)
        OPTIMIZER.zero_grad()  # zero the gradient buffers
        net.train()
        output = net(data)
        prediction = torch.argmax(output, dim=1)
        # prediction = torch.sigmoid(output)
        # print("after sigmoid")
        loss = LOSS_FUNCTION(output, lbl)
        loss.backward()
        OPTIMIZER.step()
        clas = (output > 0.5).float()
        acc = torch.mean((clas == lbl).float())
        train_acc_tmp.append(acc.detach().cpu().numpy())
        train_loss_tmp.append(loss.detach().cpu().numpy())

        if it % 50 == 0:
            for kk, (data, lbl) in enumerate(testLoader):
                data = data.cuda()
                lbl = lbl.cuda()
                OPTIMIZER.zero_grad()  # zero the gradient buffers
                net.eval()
                output = net(data)
                #output = F.sigmoid(output)
                loss = LOSS_FUNCTION(output, lbl)
                prediction = torch.argmax(output, dim=1)
                clas = (output > 0.5).float()
                acc = torch.mean((clas == lbl).float())
                test_acc_tmp.append(acc.detach().cpu().numpy())
                test_loss_tmp.append(loss.detach().cpu().numpy())

                d = prediction[0,:].detach().cpu().numpy()
                r = output[0, 1, :].detach().cpu().numpy()
                g = lbl[0, :].detach().cpu().numpy()
                plt.plot(d.squeeze(), 'b', label="prediction")
                plt.plot(r, 'r', label="output")
                plt.plot(g, 'g', label="labels")
                plt.legend(loc="upper left")
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
            plt.title('loss')
            plt.show()

            plt.plot(position, train_acc)
            plt.plot(position, test_acc)
            plt.title('accuracy')
            plt.legend(['train', 'test'])
            plt.show()
