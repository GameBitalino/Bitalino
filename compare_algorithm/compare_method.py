import numpy as np
from compare_algorithm.count_parameters import Count
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
# EMG_date_24_01_2020_time_17_04_13
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
