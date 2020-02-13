from classification.SVM_clasifficator import *
from classification.prepareDate import rectification, normalization
from classification.LoadData import LoadData, load_parsed_record
from joblib import dump, load
import datetime

muj_SVM = SVMmodel(2, 5)
data = LoadData()
time, emg = data.load_some_record()
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
emg_part = emg[:10000]

plt.figure(1)
plt.plot(emg_part, color='blue')
plt.xlabel("Vzorky [-]")
plt.ylabel("Napětí [μV]")
plt.title("Klasifikovaný EMG signál")
plt.plot(emg_part[np.array(np.where(detection == 1)[0])], color='red')
plt.legend(['klid', 'aktivita'])
plt.show()

count_of_samples = 25
verificated = detection
start_positions = []
every_start_positions = []
for d in range(len(verificated) - count_of_samples - 5):
    if verificated[d] == 1 and np.sum(verificated[d:(d + count_of_samples)]) != 1:
        verificated[d] = 0

# same model:
dump(muj_SVM, 'svm_model' + str(datetime.date.today()) + '.joblib')
# load
# model = load('svm_model.joblib')
