import numpy as np
import pandas as pd
import torch
from compare_algorithm.online_detection_without_bitalino import OnlineProcessing
from classification.LoadData import LoadData
import matplotlib.pyplot as plt

SIGNAL_LENGTH = 1024
loader = LoadData()
path = r"D:\5. ročník\DP\recordings\EMG_date_24_01_2020_time_17_04_13"

time, emg = loader.load_record(path + ".csv")
plt.plot(emg)
plt.show()

emg = emg[:59000]
emg = emg + 507
labels = np.zeros((len(emg)))
labels[1890:2775] = 1
labels[4800:5710] = 1
labels[9120:9785] = 1
labels[12135:13217] = 1
labels[14905:15940] = 1
labels[17455:18630] = 1
labels[21930:22910] = 1
labels[25800:26730] = 1
labels[29550:30520] = 1
labels[33195:34350] = 1
labels[37075:38100] = 1
labels[41725:42760] = 1
labels[46260:47300] = 1
labels[49750:50640] = 1
labels[53750:54700] = 1
labels[58205:] = 1

plt.plot(emg)
plt.plot((labels * 100) + 507)
plt.show()

########################
# processing
signal_max = np.max(emg)
calm_mean = np.mean(emg[:1000])
proc_UNET = OnlineProcessing("UNET", signal_max, calm_mean)
proc_TKEO = OnlineProcessing("TKEO", signal_max, calm_mean)
proc_SVM = OnlineProcessing("SVM", signal_max, calm_mean)

count_iter = int(len(emg) / 100)

for i in range(count_iter):
    part = emg[(i * 100):(i + 1) * 100]
    part = np.array(part)
    unet = proc_UNET.process_data(part)
    tkeo = proc_TKEO.process_data(part)
    svm = proc_SVM.process_data(part)

before_valid_UNET = proc_UNET.emg_record_result
proc_UNET.validation()
proc_SVM.validation()
proc_TKEO.validation()

unet = proc_UNET.emg_record_result
tkeo = proc_TKEO.emg_record_result
svm = proc_SVM.emg_record_result

#### plot TKEO
clas = tkeo  # choose method

# pom = pd.Series(np.array(emg[:20000]))
pom = emg
pom_result = clas
# pom_result = pd.Series(clas[:20000])
plt.plot(pom, label="Původní signál", color=[0.2, 0.2, 0.2])
plt.grid(True, which='major', alpha=0.2, ls='-.', lw=0.15)
plt.plot(pom[np.array(np.where(pom_result == 1))[0]], color=[215 / 255, 60 / 255, 45 / 255],
         label="Detekovaná aktivita")
# plt.plot(pom_result * 100 + 500)
plt.title("EMG signál s detekcí metodou TKEO")
plt.xlabel("Vzorky [-]")
plt.ylabel("Napětí [μV]")
# Show the major grid lines with dark grey lines
plt.grid(b=True, which='major', color='#666666', linestyle='-', alpha=0.5)
plt.legend()
# Show the minor grid lines with very faint and almost transparent grey lines
plt.minorticks_on()
plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.3)
plt.show()

#### plot SVM
clas = svm  # choose method

# pom = pd.Series(np.array(emg[:20000]))
pom = emg
pom_result = clas
# pom_result = pd.Series(clas[:20000])
plt.plot(pom, label="Původní signál", color=[0.2, 0.2, 0.2])
plt.grid(True, which='major', alpha=0.2, ls='-.', lw=0.15)
plt.plot(pom[np.array(np.where(pom_result == 1))[0]], color=[215 / 255, 60 / 255, 45 / 255],
         label="Detekovaná aktivita")
# plt.plot(pom_result * 100 + 500)
plt.title("EMG signál s detekcí metodou SVM")
plt.xlabel("Vzorky [-]")
plt.ylabel("Napětí [μV]")
# Show the major grid lines with dark grey lines
plt.grid(b=True, which='major', color='#666666', linestyle='-', alpha=0.5)
plt.legend()
# Show the minor grid lines with very faint and almost transparent grey lines
plt.minorticks_on()
plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.3)
plt.show()

#### plot UNET
clas = unet  # choose method

# pom = emg
# pom_result = clas
pom = pd.Series(np.array(emg[:20000]))
pom_result = pd.Series(clas[:20000])
plt.plot(pom, label="Původní signál", color=[0.2, 0.2, 0.2])
plt.grid(True, which='major', alpha=0.2, ls='-.', lw=0.15)
plt.plot(pom[np.array(np.where(pom_result == 1))[0]], color=[215 / 255, 60 / 255, 45 / 255],
         label="Detekovaná aktivita")
# plt.plot(pom_result * 100 + 500)
plt.title("EMG signál s detekcí metodou UNET")
plt.xlabel("Vzorky [-]")
plt.ylabel("Napětí [μV]")
# Show the major grid lines with dark grey lines
plt.grid(b=True, which='major', color='#666666', linestyle='-', alpha=0.5)
plt.legend()
# Show the minor grid lines with very faint and almost transparent grey lines
plt.minorticks_on()
plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.3)
plt.show()


def perf_measure(y_actual, y_pred):
    TP = 0
    FP = 0
    TN = 0
    FN = 0

    for i in range(len(y_pred)):
        if y_actual[i] == y_pred[i] == 1:
            TP += 1
        if y_pred[i] == 1 and y_actual[i] != y_pred[i]:
            FP += 1
        if y_actual[i] == y_pred[i] == 0:
            TN += 1
        if y_pred[i] == 0 and y_actual[i] != y_pred[i]:
            FN += 1

    return (TP, FP, TN, FN)


method = unet
TP, FP, TN, FN = perf_measure(method, labels)
sensitive = TP / (TP + FN)
specifity = TN / (TN + FP)
poz_prediction = TP / (TP + FP)
neg_predection = TN / (TN + FN)
accuracy = sum(1 for x, y in zip(method, labels) if x == y) / len(method)
print("METODA: UNET")
print("senzitivita: ", sensitive)
print("specifita: ", specifity)
print(("pozitivní predikce: "), poz_prediction)
print("negativní predikce: ", neg_predection)
print("přesnost: ", accuracy)

method = tkeo
### senzitivita
TP, FP, TN, FN = perf_measure(method, labels)
sensitive = TP / (TP + FN)
specifity = TN / (TN + FP)
poz_prediction = TP / (TP + FP)
neg_predection = TN / (TN + FN)
accuracy = sum(1 for x, y in zip(method, labels) if x == y) / len(method)
print("METODA: TKEO")
print("senzitivita: ", sensitive)
print("specifita: ", specifity)
print(("pozitivní predikce: "), poz_prediction)
print("negativní predikce: ", neg_predection)
print("přesnost: ", accuracy)

method = svm
### senzitivita
TP, FP, TN, FN = perf_measure(method, labels)
sensitive = TP / (TP + FN)
specifity = TN / (TN + FP)
poz_prediction = TP / (TP + FP)
neg_predection = TN / (TN + FN)
accuracy = sum(1 for x, y in zip(method, labels) if x == y) / len(method)
print("METODA: SVM")
print("senzitivita: ", sensitive)
print("specifita: ", specifity)
print(("pozitivní predikce: "), poz_prediction)
print("negativní predikce: ", neg_predection)
print("přesnost: ", accuracy)
