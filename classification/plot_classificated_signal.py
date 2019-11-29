from classification.SVM_clasifficator import *
from classification.createDataSet import rectification, normalization
from classification.LoadData import LoadData, load_parsed_record

muj_SVM = SVMmodel(2, 5)
data = LoadData()
time, emg = data.load_record(r"D:\5. ročník\DP\Bitalino\recordings\EMG_mixed_leg2.csv")
# prepare data
emg_abs = rectification(emg)
emg_abs = normalization(emg_abs)

# detection using SVM model
nFrames = 10
detection = np.ones(np.shape(emg)) * 5
for i in range(int(len(emg) / nFrames) - 1):
    vysl = countAll(muj_SVM, emg_abs[i * nFrames:(i + 1) * nFrames])[0]
    detection[i * nFrames:(i + 1) * nFrames] = np.ones(nFrames) * vysl

plt.figure(1)
plt.plot(emg, color='blue')
plt.plot(emg[np.array(np.where(detection == 1)[0])], color='red')
plt.show()

# draw only part of signal
emg_part = emg[:20000]
plt.figure(1)
plt.plot(emg_part, color='blue')
plt.plot(emg_part[np.array(np.where(detection == 1)[0])], color='red')
plt.show()
