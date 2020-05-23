import numpy as np
from compare_algorithm.count_parameters import Count
from compare_algorithm.online_detection_without_bitalino import OnlineProcessing
from classification.load_data import LoadData
import matplotlib.pyplot as plt
import os

SIGNAL_LENGTH = 1024
loader = LoadData()
dir = os.path.dirname(os.getcwd())
path = dir + os.sep + "recordings\EMG_date_24_01_2020_time_16_13_44"


time, emg = loader.load_record(path + ".csv")
plt.plot(emg)
plt.show()

emg = emg[:59000]
emg = emg + 507
labels = np.zeros((len(emg)))
# EMG_date_24_01_2020_time_17_04_13
"""
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
"""

# EMG_date_24_01_2020_time_16_13_44
labels[952:1695] = 1
labels[3440:4045] = 1
labels[5875:6330] = 1
labels[7640:8105] = 1
labels[9845:10313] = 1
labels[11885:12512] = 1
labels[13750:14280] = 1
labels[15500:16065] = 1
labels[17680:18300] = 1
labels[20028:20735] = 1
labels[22225:22900] = 1
labels[24300:25000] = 1
labels[26260:27165] = 1
labels[28670:29400] = 1
labels[31800:32700] = 1
labels[35348:35950] = 1
labels[37900:38610] = 1
labels[41120:41920] = 1
labels[44230:45035] = 1
labels[47982:48762] = 1
labels[51330:52050] = 1
labels[54820:55700] = 1
labels[57090:57718] = 1
labels[59175:59945] = 1

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

proc_UNET.validation()
proc_SVM.validation()
proc_TKEO.validation()

unet = proc_UNET.emg_record_result
tkeo = proc_TKEO.emg_record_result
svm = proc_SVM.emg_record_result

count_UNET = Count(emg=emg, method_output=unet, labels=labels, name_of_method="UNET")
count_TKEO = Count(emg=emg, method_output=tkeo, labels=labels, name_of_method="TKEO")
count_SVM = Count(emg=emg, method_output=svm, labels=labels, name_of_method="SVM")

count_UNET.plot_detected_signal(len(unet))
count_TKEO.plot_detected_signal(len(tkeo))
count_SVM.plot_detected_signal(len(svm))

count_UNET.count_accuracy_parameters()
count_TKEO.count_accuracy_parameters()
count_SVM.count_accuracy_parameters()

latency_UNET = count_UNET.count_latency()
latency_SVM = count_SVM.count_latency()
latency_TKEO = count_TKEO.count_latency()

print("UNET: ", np.mean(latency_UNET))
print("SVM: ", np.mean(latency_SVM))
print("TKEO: ", np.mean(latency_TKEO))

import pandas as pd
od = 22150
do = 22350
U = count_UNET.method_output
S = count_SVM.method_output
T = count_TKEO.method_output
fig, (ax0, ax1, ax2,ax3) = plt.subplots(4, sharex=True)
fig.suptitle('Detekce počátku aktivity různými metodami', y= 0.95, fontsize= 14)
#unet
vyska_lab = 120
pom = pd.Series(np.array(count_TKEO.emg[od:do]))
ax0.plot(pom, label="Původní signál", color=[0.2, 0.2, 0.2])
ax0.plot(labels[od:do] * vyska_lab + 507, color = 'r')
ax0.set_title("Manuální anotace dat")
pom_result = pd.Series(U[od:do])
ax1.plot(pom, label="Původní signál", color=[0.2, 0.2, 0.2])
ax1.plot(pom_result* vyska_lab + 507,  color = 'r')
ax1.set_title("Detekce aktivity metodou U-Net")
#svm
pom_result = pd.Series(S[od:do])
ax2.plot(pom, label="Původní signál", color=[0.2, 0.2, 0.2])
ax2.plot(pom_result* vyska_lab + 507,  color = 'r')
ax2.set_title("Detekce aktivity metodou SVM")
#tkeo
pom = pd.Series(np.array(count_TKEO.emg[od:do]))
pom_result = pd.Series(T[od:do])
ax3.plot(pom, label="Původní signál", color=[0.2, 0.2, 0.2])
ax3.plot(pom_result* vyska_lab + 507,  color = 'r')
ax3.set_title("Detekce aktivity metodou TKEO")
#fig.text(1.5, 0.04, 'Vzroky [-]', ha='center')
#fig.text(0.04, 0.5, 'Napětí [μV]', va='center', rotation='vertical')
fig.tight_layout()
fig.subplots_adjust(top=0.85)
plt.savefig("novy_onset.png", dpi=150)
plt.show()

# porovnani cekove detekce
od = 22100
do = 23100
U = count_UNET.method_output
S = count_SVM.method_output
T = count_TKEO.method_output
fig, (ax1, ax2,ax3) = plt.subplots(3, sharex=True)
fig.suptitle('Detekce aktivity v EMG signálu různými metodami', y= 0.95, fontsize= 14)
#unet
pom = pd.Series(np.array(count_TKEO.emg[od:do]))
pom_result = pd.Series(U[od:do])
ax1.plot(pom, label="Původní signál", color=[0.2, 0.2, 0.2])
ax1.plot(pom[np.array(np.where(pom_result == 1))[0]], color=[215 / 255, 60 / 255, 45 / 255],
                 label="Detekovaná aktivita")
ax1.set_title("Detekce aktivity metodou U-Net")
#svm
pom_result = pd.Series(S[od:do])
ax2.plot(pom, label="Původní signál", color=[0.2, 0.2, 0.2])
ax2.plot(pom[np.array(np.where(pom_result == 1))[0]], color=[215 / 255, 60 / 255, 45 / 255],
                 label="Detekovaná aktivita")
ax2.set_title("Detekce aktivity metodou SVM")
#tkeo
pom = pd.Series(np.array(count_TKEO.emg[od:do]))
pom_result = pd.Series(T[od:do])
ax3.plot(pom, label="Původní signál", color=[0.2, 0.2, 0.2])
ax3.plot(pom[np.array(np.where(pom_result == 1))[0]], color=[215 / 255, 60 / 255, 45 / 255],
                 label="Detekovaná aktivita")
ax3.set_title("Detekce aktivity metodou TKEO")
#fig.text(1.5, 0.04, 'Vzroky [-]', ha='center')
#fig.text(0.04, 0.5, 'Napětí [μV]', va='center', rotation='vertical')
fig.tight_layout()
fig.subplots_adjust(top=0.85)
plt.savefig("novy_onset.png", dpi=150)
plt.show()