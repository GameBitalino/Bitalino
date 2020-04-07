import os
import numpy as np
from compare_algorithm.count_parameters import Count
from compare_algorithm.online_detection_without_bitalino import OnlineProcessing
from classification.load_data import LoadData
import matplotlib.pyplot as plt

path = os.path.dirname(os.path.dirname(os.getcwd())) + os.sep + r"recordings\test_accuracy_algorithm"
entries = os.listdir(path)

SIGNAL_LENGTH = 1024
loader = LoadData()
specificity_SVM = []
sensitivity_SVM = []
accuracy_SVM = []
poz_prediction_SVM = []
neg_prediction_SVM = []

specificity_TKEO = []
sensitivity_TKEO = []
accuracy_TKEO = []
poz_prediction_TKEO = []
neg_prediction_TKEO = []

specificity_UNET = []
sensitivity_UNET = []
accuracy_UNET = []
poz_prediction_UNET = []
neg_prediction_UNET = []

proc_UNET = []
proc_TKEO = []
proc_SVM = []

latency_UNET = []
latency_SVM = []
latency_TKEO = []

variance_TKEO = []
variance_SVM = []
variance_UNET = []

for signal in entries:
    time, emg = loader.load_record(path + os.sep + signal)
    emg = emg + 507
    labels = np.zeros((len(emg)))
    # emg, clas = loader.load_record(path + os.sep + signal)
    # labels = clas
    file = signal[:-4]
    print(file)

    if file == "EMG_date_24_01_2020_time_17_04_13":
        # EMG_date_24_01_2020_time_17_04_13
        emg = emg[:59000]
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

    elif file == "EMG_date_24_01_2020_time_17_08_26":
        # EMG_date_24_01_2020_time_17_08_26
        labels[7855:8970] = 1
        labels[10230:11340] = 1
        labels[13575:14690] = 1
        labels[16620:17755] = 1
        labels[20400:21450] = 1
        labels[26900:27850] = 1
        labels[36200:37310] = 1
        labels[43710:44730] = 1
        labels[48340:49360] = 1
        labels[53480:54740] = 1

    elif file == "EMG_date_24_01_2020_time_17_12_06":
        # EMG_date_24_01_2020_time_17_12_06
        labels[1490:2450] = 1
        labels[4425:5550] = 1
        labels[8690:9840] = 1
        labels[11600:12770] = 1
        labels[17823:18847] = 1

    elif file == "EMG_date_24_01_2020_time_16_17_46":
        # EMG_date_24_01_2020_time_16_17_46
        labels[1060:1830] = 1
        labels[3248:4000] = 1
        labels[5475:6190] = 1
        labels[8115:8860] = 1
        labels[10468:11230] = 1  # according to tkeo_algorithm
        labels[13800:14647] = 1
        labels[16650:17475] = 1
        labels[18960:19820] = 1
        labels[22545:23480] = 1
        labels[25488:26352] = 1
        labels[28875:29750] = 1
        labels[31350:32120] = 1
        labels[33475:34150] = 1
        labels[35175:35900] = 1
        labels[39000:39850] = 1
        labels[41935:42900] = 1
        labels[45975:47070] = 1
        labels[50520:51280] = 1
        labels[53880:55000] = 1
        labels[58250:59260] = 1

    elif file == "EMG_date_24_01_2020_time_16_16_26":
        # EMG_date_24_01_2020_time_16_16_26
        labels[7958:8560] = 1
        labels[11035:11690] = 1
        labels[14260:14905] = 1
        labels[16995:17590] = 1
        labels[20400:21222] = 1
        labels[22725:23295] = 1
        labels[24700:25160] = 1
        labels[26550:26970] = 1
        labels[28620:29100] = 1
        labels[30890:31400] = 1
        labels[34000:34485] = 1
        labels[36474:36940] = 1
        labels[38350:38860] = 1
        labels[41040:41545] = 1
        labels[44980:45550] = 1
        labels[47730:48315] = 1
        labels[50620:51142] = 1
        labels[54450:55050] = 1
        labels[56430:56900] = 1
        labels[58248:58675] = 1

    elif file == "EMG_date_24_01_2020_time_16_13_44":
        # EMG_date_24_01_2020_time_16_13_44 - hnusny signal
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

    elif file == "EMG_date_24_01_2020_time_16_10_18":
        # EMG_date_24_01_2020_time_16_10_18
        labels[3319:4055] = 1
        labels[5194:5969] = 1
        labels[7880:8425] = 1
        labels[10566:11300] = 1
        labels[12850:13501] = 1
        labels[14200:14850] = 1
        labels[15750:16384] = 1
        labels[17175:17800] = 1
        labels[19130:19950] = 1
        labels[22012:22785] = 1
        labels[24488:25275] = 1
        labels[26576:27275] = 1
        labels[28175:28960] = 1
        labels[30172:31000] = 1
        labels[32550:33527] = 1
        labels[35270:36070] = 1
        labels[37145:37850] = 1
        labels[39260:40111] = 1
        labels[41470:42400] = 1
        labels[43886:44650] = 1
        labels[45918: 46860] = 1
        labels[48483:49252] = 1
        labels[51340:52010] = 1
        labels[54472:55318] = 1
        labels[56780:57565] = 1
        labels[58945:59800] = 1

    elif file == "EMG_date_10_15_2019_time_18_01_51":
        # EMG_date_10_15_2019_time_18_01_51: 1.:
        # 658-1478, 2: 2723-3476, 3: 4684 - 5481
        labels[658:1478] = 1
        labels[2723:3476] = 1
        labels[4684:5481] = 1

    elif file == "EMG_date_25_12_2019_time_20_57_23":
        # velky sum
        # EMG_date_25_12_2019_time_20_57_23:
        labels[4930:5450] = 1
        labels[8954:9465] = 1
        labels[13270:13640] = 1
        labels[17140:17578] = 1
        labels[20773:21202] = 1
        labels[24050:24600] = 1
        labels[28085:29155] = 1

    elif file == "EMG_date_25_12_2019_time_21_00_07":
        # EMG_date_25_12_2019_time_21_00_07
        labels[887:1200] = 1
        labels[2800:3090] = 1
        labels[4500:4768] = 1
        labels[7684:8150] = 1
        labels[10562:10800] = 1
        labels[12602:12752] = 1
        labels[16540:16730] = 1
        labels[20347:20610] = 1
        labels[23190:23440] = 1
        labels[27410:27960] = 1

    elif file == "EMG_date_25_12_2019_time_21_00_55":
        # EMG_date_25_12_2019_time_21_00_55
        labels = np.zeros((len(emg)))
        labels[2025:2370] = 1
        labels[4402:4605] = 1
        labels[6350:6652] = 1
        labels[9675:9850] = 1
        labels[14262:14432] = 1
        labels[19950:20115] = 1
        labels[25830:26024] = 1
        labels[27720:29000] = 1

    elif file == "EMG_date_25_12_2019_time_21_04_45":
        # EMG_date_25_12_2019_time_21_04_45
        labels = np.zeros((len(emg)))
        labels[1025:1252] = 1
        labels[3566:3800] = 1
        labels[5928:6219] = 1
        labels[7620:8280] = 1  # ??
        labels[12547:12960] = 1
        labels[16204:16560] = 1
        labels[18350:18680] = 1
        labels[21966:22300] = 1
        labels[22360:22620] = 1
        labels[24466:25250] = 1
        labels[28889:30000] = 1

    elif file == "EMG_date_25_12_2019_time_21_06_41":
        # EMG_date_25_12_2019_time_21_06_41
        labels = np.zeros((len(emg)))
        labels[1083:1500] = 1
        labels[4458:4900] = 1
        labels[4945:5180] = 1
        labels[7943:8750] = 1
        labels[11975:12650] = 1
        labels[15360:15845] = 1
        labels[15900:16010] = 1
        labels[19850:20480] = 1
        labels[24562:25025] = 1
        labels[27786:28620] = 1

    elif file == "EMG_date_25_12_2019_time_21_07_59":
        # EMG_date_25_12_2019_time_21_07_59
        labels = np.zeros((len(emg)))
        labels[1288:2030] = 1
        labels[4132:4975] = 1
        labels[7088:7670] = 1  # ? :7970?
        labels[9276:10400] = 1
        labels[13490:14314] = 1
        labels[22325:23210] = 1
        labels[25610:26510] = 1
        labels[27268:27478] = 1
        labels[28767:29262] = 1

    elif file == "EMG_date_25_12_2019_time_21_10_07":
        # EMG_date_25_12_2019_time_21_10_07
        labels = np.zeros((len(emg)))
        labels[3110:3780] = 1
        labels[4908:5150] = 1
        labels[6895:7120] = 1
        labels[8975:9430] = 1
        labels[13100:13510] = 1
        labels[16175:16430] = 1
        labels[17600:17825] = 1
        labels[19732:19885] = 1
        labels[22150:22424] = 1
        labels[24470:24721] = 1
        labels[26624:26831] = 1
        labels[29880:] = 1

    elif file == "EMG_date_25_12_2019_time_21_11_38":
        # EMG_date_25_12_2019_time_21_11_38
        labels = np.zeros((len(emg)))
        labels[1096:1470] = 1
        labels[3548:3835] = 1
        labels[6350:6700] = 1
        labels[8920:9300] = 1
        labels[12170:12490] = 1
        labels[16944:17235] = 1
        labels[21900:22200] = 1
        labels[27180:27480] = 1
        labels[29570:29870] = 1

    elif file == "EMG_date_25_12_2019_time_21_12_26":
        # EMG_date_25_12_2019_time_21_12_26
        labels = np.zeros((len(emg)))
        labels[1807:2110] = 1
        labels[4763:5300] = 1
        labels[7600:8130] = 1
        labels[14804:15250] = 1
        labels[17466:17800] = 1
        labels[20055:20400] = 1
        labels[22600:23015] = 1
        labels[25036:25500] = 1  # ? :25790
        labels[27760:28105] = 1

    elif file == "EMG_date_25_12_2019_time_21_16_16":
        # EMG_date_25_12_2019_time_21_16_16
        labels = np.zeros((len(emg)))
        labels[1100:1449] = 1
        labels[5090:5480] = 1
        labels[8600:9020] = 1
        labels[11398:11700] = 1
        labels[14450:14750] = 1
        labels[17775:18110] = 1
        labels[21960:22400] = 1
        labels[26090:26378] = 1
        labels[26886:27220] = 1
        labels[27790:28040] = 1
        labels[29680:29905] = 1

    signal_max = np.max(emg)
    calm_mean = np.mean(emg[:1500])
    proc_UNET = OnlineProcessing("UNET", signal_max, calm_mean)
    # proc_TKEO = OnlineProcessing("TKEO", signal_max, calm_mean)
    # proc_SVM = OnlineProcessing("SVM", signal_max, calm_mean)

    count_iter = int(len(emg) / 100)

    for i in range(count_iter):
        part = emg[(i * 100):(i + 1) * 100]
        part = np.array(part)
        unet = proc_UNET.process_data(part)
        # tkeo = proc_TKEO.process_data(part)
        # svm = proc_SVM.process_data(part)

    proc_UNET.validation()
    # proc_SVM.validation()
    # proc_TKEO.validation()

    unet = proc_UNET.emg_record_result
    # tkeo = proc_TKEO.emg_record_result
    # svm = proc_SVM.emg_record_result

    count_UNET = Count(emg=emg, method_output=unet, labels=labels, name_of_method="UNET")
    # count_TKEO = Count(emg=emg, method_output=tkeo, labels=labels, name_of_method="TKEO")
    # count_SVM = Count(emg=emg, method_output=svm, labels=labels, name_of_method="SVM")

    # count_UNET.plot_detected_signal(len(unet))
    # plt.plot(proc_UNET.model_unet.NN_output_debug*1.2)
    # plt.show()
    # count_TKEO.plot_detected_signal(len(tkeo))
    # count_SVM.plot_detected_signal(len(svm))

    count_UNET.count_accuracy_parameters()
    # count_TKEO.count_accuracy_parameters()
    # count_SVM.count_accuracy_parameters()

    """
    specificity_SVM.append(count_SVM.specificity)
    sensitivity_SVM.append(count_SVM.sensitive)
    accuracy_SVM.append(count_SVM.accuracy)
    poz_prediction_SVM.append(count_SVM.poz_prediction)
    neg_prediction_SVM.append(count_SVM.neg_prediction)

    specificity_TKEO.append(count_TKEO.specificity)
    sensitivity_TKEO.append(count_TKEO.sensitive)
    accuracy_TKEO.append(count_TKEO.accuracy)
    poz_prediction_TKEO.append(count_TKEO.poz_prediction)
    neg_prediction_TKEO.append(count_TKEO.neg_prediction)
    """
    specificity_UNET.append(count_UNET.specificity)
    sensitivity_UNET.append(count_UNET.sensitive)
    accuracy_UNET.append(count_UNET.accuracy)
    poz_prediction_UNET.append(count_UNET.poz_prediction)
    neg_prediction_UNET.append(count_UNET.neg_prediction)

    """
    latency_UNET.append(np.mean(count_UNET.count_latency()))
    latency_SVM.append(np.mean(count_SVM.count_latency()))
    latency_TKEO.append(np.mean(count_TKEO.count_latency()))

    variance_UNET.append(np.mean(count_UNET.variance))
    variance_SVM.append(np.mean(count_SVM.variance))
    variance_TKEO.append(np.mean(count_TKEO.variance))
    """
print("SPECIFITA")
print(np.mean(specificity_UNET))
print(np.mean(specificity_SVM))
print(np.mean(specificity_TKEO))

print("SENZITIVITA")
print(np.mean(sensitivity_UNET))
print(np.mean(sensitivity_SVM))
print(np.mean(sensitivity_TKEO))

print("PŘESNOST")
print(np.mean(accuracy_UNET))
print(np.mean(accuracy_SVM))
print(np.mean(accuracy_TKEO))

"""
print("POZITIVNÍ PREDIKCE")
print(np.mean(poz_prediction_UNET))
print(np.mean(poz_prediction_SVM))
print(np.mean(poz_prediction_TKEO))

print("NEGATIVNÍ PREDIKCE")
print(np.mean(neg_prediction_UNET))
print(np.mean(neg_prediction_SVM))
print(np.mean(neg_prediction_TKEO))

print("TIME")
print(np.mean(proc_UNET.duration) * 1000)
print(np.mean(proc_SVM.duration) * 1000)
print(np.mean(proc_TKEO.duration) * 1000)

print("LATENCY")
print(np.mean(latency_UNET))
print(np.mean(latency_SVM))
print(np.mean(latency_TKEO))

print("LATENCY varience")
print(np.mean(variance_UNET))
print(np.mean(variance_SVM))
print(np.mean(variance_TKEO))
"""