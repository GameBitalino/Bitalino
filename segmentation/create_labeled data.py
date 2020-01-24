from DWT.LoadData import LoadData
from matplotlib import pyplot as plt
from DWT.filtration import *
import numpy as np
import saveData

path = r"D:\5. ročník\DP\Bitalino\recordings\EMG_recordings_not_parsed\EMG_date_25_12_2019_time_20_57_23"
loader = LoadData()
time, emg = loader.load_record(path + ".csv")


plt.plot(time, emg)
plt.title("Záznam EMG")
plt.xlabel("Čas [s]")
plt.ylabel("Napětí [μV]")
plt.show()

filtered_DWT = DWT(emg)
deviation, positions1, emg_detected = standard_deviation(filtered_DWT, 6)

filtered_TKEO = TKEO(emg)
deviation2, positions2, emg_detected2 = standard_deviation(filtered_TKEO, 2)


plt.figure()
plt.plot(emg, 'b')
plt.plot(emg_detected2[positions2], color='red')
plt.title('Detekovaná aktivita EMG - TKEO')
plt.legend(['klid', 'aktivita'])
plt.xlabel(xlabel="Vzorky[-]")
plt.ylabel(ylabel='Napětí []')
plt.show()

"""
plt.figure()
plt.plot(emg, 'b')
plt.plot(emg_detected[positions], color='red')
plt.title('Detekovaná aktivita EMG - DWT')
plt.legend(['klid', 'aktivita'])
plt.xlabel(xlabel="Vzorky[-]")
plt.ylabel(ylabel='Napětí []')
plt.show()
"""

labels = np.zeros((len(emg)))
# activity => 1

# EMG_date_10_15_2019_time_18_01_51: 1.:
# 658-1478, 2: 2723-3476, 3: 4684 - 5481
"""
labels[658:1478] = 1
labels[2723:3476] = 1
labels[4684:5481] = 1
"""


# EMG_date_25_12_2019_time_20_57_23:

labels[4894:5450] = 1
labels[8954:9465] = 1
labels[9650:9710] = 1
labels[13146:13924] = 1
labels[16906:17877] = 1
labels[20590:21488] = 1
labels[23976:24992] = 1
labels[27934:29155] = 1


# EMG_date_25_12_2019_time_21_00_07
"""
labels[806:1660] = 1
labels[2788:3355] = 1
labels[4481:5036] = 1
labels[7684:8587] = 1
labels[10562:11097] = 1
labels[12602:13130] = 1
labels[16540:17180] = 1
labels[20347:20833] = 1
labels[23190:23907] = 1
labels[27380:28154] = 1
"""


# EMG_date_25_12_2019_time_21_00_55
"""
labels = np.zeros((len(emg)))
labels[1966:2711] = 1
labels[4402:4813] = 1
labels[64340:6730] = 1
labels[9643:10027] = 1
labels[14262:14732] = 1
labels[19940:20120] = 1
labels[25810:26290] = 1
labels[27716:29000] = 1
"""

# EMG_date_25_12_2019_time_21_04_45
"""
labels = np.zeros((len(emg)))
labels[1006:1643] = 1
labels[3566:4036] = 1
labels[5928:6219] = 1
labels[7620:8568] = 1
labels[12547:13313] = 1
labels[16204:16858] = 1
labels[18207:18943] = 1
labels[21966:22629] = 1
labels[24466:25556] = 1
labels[28889:30000] = 1
"""

# EMG_date_25_12_2019_time_21_06_41
"""
labels = np.zeros((len(emg)))
labels[1083:1788] = 1
labels[4458:5271] = 1
labels[7943:8786] = 1
labels[11964:12767] = 1
labels[15279:16233] = 1
labels[19832:20642] = 1
labels[24545:25391]=1
labels[27786:28687] = 1
"""

#EMG_date_25_12_2019_time_21_07_59
"""
labels = np.zeros((len(emg)))
labels[1288:2090] = 1
labels[4112:5042] = 1
labels[7088:7970] = 1
labels[9276:10400] = 1
labels[13490:14471] = 1
labels[22286:23290] = 1
labels[25584:26510] = 1
labels[27208:27715] = 1
labels[28767:29262] = 1
"""

# EMG_date_25_12_2019_time_21_10_07
"""
labels = np.zeros((len(emg)))
labels[3101:3937] = 1
labels[4908:5418] = 1
labels[6895:7344] = 1
labels[8966:9481] = 1
labels[13090:13852] = 1
labels[16152:16672] = 1
labels[17586:17835] = 1
labels[19722:19891] = 1
labels[22066:22424] = 1
labels[24396:24721] = 1
labels[26618:26831] = 1
labels[29871:30000] = 1
"""

# EMG_date_25_12_2019_time_21_11_38
"""
labels = np.zeros((len(emg)))
labels[1096:1745] = 1
labels[3548:4120] = 1
labels[6348:7050] = 1
labels[8920:9476] = 1
labels[12100:12500] = 1
labels[16944:17245] = 1
labels[17350:17420] = 1
labels[21855:22430] = 1
labels[27180:27750] = 1
labels[29545:30000] = 1
"""

# EMG_date_25_12_2019_time_21_12_26
"""
labels = np.zeros((len(emg)))
labels[1782:2360] = 1
labels[4763:5512] = 1
labels[7554:8304] = 1
labels[14704:15483] = 1
labels[17466:18135] = 1
labels[20040:20761] = 1
labels[22589:23388] = 1
labels[25036:25725] = 1
labels[27715:28341] = 1
"""

#EMG_date_25_12_2019_time_21_16_16
"""
labels = np.zeros((len(emg)))
labels[1038:1749] = 1
labels[5080:5590] = 1
labels[8552:9186] = 1
labels[11392:11850] = 1
labels[14450:14965] = 1
labels[17745:18458] = 1
labels[21960:22617] = 1
labels[26060:26378] = 1
labels[26886:27275] = 1
labels[27760:28200] = 1
labels[29620:30000] = 1
"""

plt.plot(emg)
plt.plot(labels*100)
plt.show()

#saveData.saveLabeledData(emg, labels, path, 1024)
