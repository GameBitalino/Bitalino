from segmentation.UNet import UNetModel
from matplotlib import pyplot as plt
import numpy as np
import torch
from torch.nn import CrossEntropyLoss
from torch.optim import Adam, SGD
import pandas as pd
from segmentation.loaderEMG import DataLoader
from torch.utils.tensorboard import SummaryWriter

writer = SummaryWriter()

LEARNING_RATE = 0.001
NUMBER_OF_EPOCH = 60
LOSS_FUNCTION = CrossEntropyLoss()
SIGNAL_LENGTH = 1024

loaderTrain = DataLoader('EMG_train_data', SIGNAL_LENGTH)
trainLoader = torch.utils.data.DataLoader(loaderTrain, batch_size=1, num_workers=0, shuffle=True,
                                          drop_last=True)

loaderTest = DataLoader('EMG_test_data', SIGNAL_LENGTH)
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
        tresh1 = np.where(tresh * 1.2 > -5)
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
            data_emg = test_data[0, :, :].detach().cpu().numpy().squeeze()
            vystup_site = output[0, 1, :].detach().cpu().numpy()

            fig = plt.figure(1)
            plt.style.use("ggplot")
            plt.plot(prediction[0, :].detach().cpu().numpy(), color="b", label="prediction")
            plt.plot(test_lbl[0, :].detach().cpu().numpy(), color="g", label="label")
            plt.plot(novy, color="r", label="tresh")
            plt.legend(loc="upper left")
            plt.title("Detekce EMG aktivity")
            plt.xlabel("Vzorky [-]")
            plt.ylabel("Predikce [-]")
            writer.add_figure("train/prediction", fig, it)

            fig2 = plt.figure(2)
            plt.style.use("ggplot")
            plt.plot(vystup_site, color = 'black')
            plt.title("Výstup sítě U-Net")
            plt.xlabel("Vzorky [-]")
            plt.ylabel("Výstup sítě [-]")
            writer.add_figure("Výstup sítě U-Net", fig2, it)

            fig4 = plt.figure(4)
            plt.style.use("ggplot")
            plt.title("Zvýrazněný výstup sítě U-Net s prahem")
            plt.plot(x, y, color='r')
            plt.plot(vystup_site*1.2, color = 'black')
            plt.xlabel("Vzorky [-]")
            plt.ylabel("Výstup sítě [-]")
            writer.add_figure("Zvýrazněný výstup sítě U-Net s prahem", fig4, it)

            fig5 = plt.figure(5)
            plt.style.use("ggplot")
            pom = pd.Series(np.array(data_emg))
            plt.title("Detekovaná EMG aktivita")
            plt.plot(pom + 507, color = 'black')
            plt.plot(pom[np.array(tresh1)[0]] + 507, color=[215 / 255, 60 / 255, 45 / 255], label="Detekovaná aktivita")
            plt.xlabel("Vzorky [-]")
            plt.ylabel("Výstup sítě [-]")
            writer.add_figure("Detekovaná EMG aktivita", fig5, it)

            fig3 = plt.figure(3)
            plt.style.use("ggplot")
            plt.plot(data_emg + 507, color = 'black')
            plt.title("Původní EMG signál")
            plt.xlabel("Vzorky [-]")
            plt.ylabel("Napětí [μV]")
            writer.add_figure("Původní EMG signál", fig3, it)

            fig6 = plt.figure(6)
            plt.style.use("ggplot")
            plt.plot(x, y+3, color='r')
            plt.plot(vystup_site*1.2, color = 'black')
            plt.title("Zvýrazněný výstup sítě U-Net s prahem")
            plt.xlabel("Vzorky [-]")
            plt.ylabel("Výstup sítě [-]")
            writer.add_figure("Zvýrazněný výstup sítě U-Net s prahem", fig6, it)

            fig7= plt.figure(7)
            plt.style.use("ggplot")
            plt.title("Detekovaná EMG aktivita")
            plt.plot(data_emg + 507, 'black')
            tr = np.where(tresh * 1.2 > -2)
            plt.plot(data_emg[tr] +507, color = 'r')
            plt.xlabel("Vzorky [-]")
            plt.ylabel("Výstup sítě [-]")
            writer.add_figure("Detekovaná EMG aktivita", fig7, it)

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
        torch.save(net,
                   r"D:\5. ročník\DP\Bitalino\models\model_epoch_" + current_epoch + "CrossEntropyLoss_Adam_optimizer_1024_05_03_2020.pth")
        """
        plt.plot(position, train_loss)
        plt.plot(position, test_loss)
        plt.title('loss')
        plt.show()

        plt.plot(position, train_acc)
        plt.plot(position, test_acc)
        plt.title('accuracy')
        plt.legend(['train', 'test'])
        plt.show()
        """
