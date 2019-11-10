from classification.SVM_clasifficator import *

muj_SVM = SVMmodel(2,5)
from classification.LoadData import LoadData, load_parsed_record

data = LoadData()
time, emg = data.load_record(r"D:\5. ročník\DP\Bitalino\recordings\EMG_cont2.csv")
emg_abs = abs(emg)

detection = np.ones(np.shape(emg))*5
for i in range(int(len(emg) / 100)-1):
    vysl = countAll(muj_SVM, emg_abs[i*100:(i+1)*100])[0]
    detection[i * 100:(i + 1) * 100] = np.ones(100)*vysl

plt.figure(1)
plt.plot(emg, color = 'blue')
plt.plot(emg[np.array(np.where(detection == 1)[0])],color='red')
plt.show()

