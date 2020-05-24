from segmentation.UNet import UNetModel
from matplotlib import pyplot as plt
import numpy as np
import torch, os
from torch.nn import CrossEntropyLoss
from torch.optim import Adam
from segmentation.loader_EMG import DataLoader
from torch.utils.tensorboard import SummaryWriter

writer = SummaryWriter()

LEARNING_RATE = 0.001
NUMBER_OF_EPOCH = 60
LOSS_FUNCTION = CrossEntropyLoss()
SIGNAL_LENGTH = 1024

dir = os.path.dirname(os.getcwd())
path_to_data = dir + os.sep + "recordings"
path_saved_data = dir + os.sep + "models"
loaderTrain = DataLoader('EMG_train_data', SIGNAL_LENGTH, path_to_data=path_to_data)
trainLoader = torch.utils.data.DataLoader(loaderTrain, batch_size=1, num_workers=0, shuffle=True,
                                          drop_last=True)

loaderTest = DataLoader('EMG_test_data', SIGNAL_LENGTH, path_to_data=path_to_data)
testLoader = torch.utils.data.DataLoader(loaderTest, batch_size=1, num_workers=0, shuffle=True, drop_last=True)

net = UNetModel().cuda()
OPTIMIZER = Adam(net.parameters(), lr=LEARNING_RATE, weight_decay=1e-6)

train_loss = []
test_loss = []
train_acc = []
test_acc = []
position = []
train_acc_tmp = []
train_loss_tmp = []
test_acc_tmp = []
test_loss_tmp = []
x = np.linspace(0, 1024, 1024)
y = np.ones(1024) * -5

it = -1
for epoch in range(NUMBER_OF_EPOCH):
    print(epoch)
    for k, (test_data, test_lbl, test_name) in enumerate(trainLoader):
        it += 1
        test_data = test_data.cuda()
        test_lbl = test_lbl.cuda()
        OPTIMIZER.zero_grad()  # zero the gradient buffers
        net.train()
        output = net(test_data)
        loss = LOSS_FUNCTION(output, test_lbl)
        loss.backward()
        OPTIMIZER.step()
        prediction = torch.argmax(output, dim=1)
        tresh = output[0, 1, :].detach().cpu().numpy()
        tresh1 = np.where(tresh * 1.2 > -2)
        novy = np.zeros(SIGNAL_LENGTH)
        novy[tresh1] = 1
        quality = np.sum(novy == (test_lbl[0, :].detach().cpu().numpy()))
        acc = torch.mean((prediction == test_lbl).float())
        train_acc_tmp.append(acc.detach().cpu().numpy())
        train_loss_tmp.append(loss.detach().cpu().numpy())

        if it % 10:
            writer.add_scalar('loss', loss, it)
            writer.add_scalar('accuracy', acc, it)
            writer.add_scalar("quality", quality, it)
    if epoch % 10 == 0:
        for kk, (test_data, test_lbl, test_name) in enumerate(testLoader):
            test_data = test_data.cuda()
            test_lbl = test_lbl.cuda()
            OPTIMIZER.zero_grad()  # zero the gradient buffers
            net.eval()
            output = net(test_data)
            # output = F.sigmoid(output)
            loss = LOSS_FUNCTION(output, test_lbl)
            prediction = torch.argmax(output, dim=1)
            clas = torch.argmax(output, dim=1)
            acc = torch.mean((clas == test_lbl).float())
            test_acc_tmp.append(acc.detach().cpu().numpy())
            test_loss_tmp.append(loss.detach().cpu().numpy())
            d = prediction[0, :].detach().cpu().numpy()
            o = test_data[0, :, :].detach().cpu().numpy()
            r = output[0, 1, :].detach().cpu().numpy()
            g = test_lbl[0, :].detach().cpu().numpy()
            plt.plot(o.squeeze(), 'y', label='origin signal')
            plt.plot(d.squeeze() * 50, 'b', label="prediction")
            plt.plot(g * 50, 'g', label="labels")
            plt.legend(loc="upper left")
            plt.title(test_name[0].split("\\")[-1])
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

        current_epoch = str(epoch)
        torch.save(net, path_saved_data + os.sep + "model_epoch_" + current_epoch + ".pth")

