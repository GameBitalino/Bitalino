import statistics
import time as timer
import numpy as np
import pandas as pd
import pywt
from matplotlib import pyplot as plt
from scipy import signal
from classification.LoadData import LoadData

data = LoadData()
time, emg = data.load_record(r"D:\5. ročník\DP\recordings\EMG_date_25_12_2019_time_21_04_45.csv")
# data.plot_data()

emg = emg[:10000]
time = time[:10000]
emg[8400:8600] = emg[9100:9300]


def standard_deviation_offline_signal(emg_filter, std_tresh=2, window_half_length=2):
    deviation = []
    for i in range(window_half_length, len(emg_filter) - window_half_length):
        deviation.append(statistics.stdev(emg_filter[i - window_half_length:i + window_half_length]))

    calm_deviation = np.mean(deviation[:500])
    draw = emg_filter[window_half_length:-window_half_length]
    emg_filter = pd.Series(emg_filter)
    positions = np.array(np.where(deviation > (calm_deviation * std_tresh))[0])
    plt.figure()
    plt.plot(draw, 'b')
    plt.plot(emg_filter[positions], color='red')
    plt.title('Detekovaná aktivita EMG')
    plt.legend(['klid', 'aktivita'])
    plt.xlabel(xlabel="Vzorky[-]")
    plt.ylabel(ylabel='TKEO')
    plt.show()

    """
    fig4 = plt.figure()
    figures = 200  # 2
    ax1 = fig4.add_subplot(figures + 11)
    ax1.plot(emg_filter)
    ax2 = fig4.add_subplot(figures + 12)
    ax2.plot(deviation)
    ax1.title.set_text('signál EMG')
    ax2.title.set_text('Směrodatná odchylka')
    ax1.set(xlabel="Vzorky[-]", ylabel="Napětí")
    ax2.set(xlabel="Vzorky[-]", ylabel="Odchylka")
    plt.show()
    """
    return deviation, positions, emg_filter[positions]


# TKEO - filtration
def TKEO(EMG_for_TKEO):
    start = timer.time()
    tkeo = []
    for i in range(1, len(EMG_for_TKEO) - 1):
        tkeo.append(EMG_for_TKEO[i] ** 2 - EMG_for_TKEO[i - 1] * EMG_for_TKEO[i + 1])

    print('Time for TKEO: ', timer.time() - start)
    """
    fig4 = plt.figure()
    figures = 200  # 2
    ax1 = fig4.add_subplot(figures + 11)
    ax1.plot(EMG_for_TKEO)
    ax2 = fig4.add_subplot(figures + 12)
    ax2.plot(tkeo)
    ax1.title.set_text('EMG')
    ax2.title.set_text('TKEO')
    ax1.set(xlabel="Vzorky[-]", ylabel="Napětí")
    ax2.set(xlabel="Vzorky[-]", ylabel="TKEO")
    plt.show()
    """
    return tkeo


def DWT(emg, wave='coif6', level=6):
    wavelets = pywt.wavedec(emg, wavelet=wave, level=level)

    fig4, ax = plt.subplots(len(wavelets) + 1)
    ax[0].plot(emg)
    for i, wavelet in enumerate(wavelets):
        ax[i + 1].plot(wavelet)

    fig4.tight_layout()
    plt.show()

    K = 5
    rows_count = np.shape(wavelets)[0]
    # H (prahování)
    # výpočet adaptivního prahu
    start = timer.time()
    tresh = np.zeros(rows_count)
    for j in range(rows_count - 1):
        s = np.median(np.abs(wavelets[j])) / 0.6745  # median
        # tresh1 = s*sqrt(2*log(length(SWC(j,:)))); %universal treshold
        # tresh1 = K*s # lambda = K*sigma(std) (odhad směrodatné odchylky)
        tresh[j] = K * s

    # prahovani vlnkovych koeficientu
    y = wavelets  # for tresholding
    for k in range(rows_count):
        current = wavelets[k]
        for i in range(len(current)):
            if np.abs(current[i]) > tresh[k]:
                y[k][i] = current[i]
            else:
                y[k][i] = 0

    emg_filter = pywt.waverec(y, wave)
    emg_filter = emg_filter
    cas = timer.time() - start
    print("Time of filtration (WT): ", cas)

    # druhe pasmo:
    """
    y1_n = []
    for i in wavelets[-2]:
        y1_n.append(i)
        y1_n.append(0)
        y1_n.append(0)
        y1_n.append(0)
    
    fig4 = plt.figure()
    figures = 200  # 2
    ax1 = fig4.add_subplot(figures + 11)
    ax1.plot(emg)
    ax2 = fig4.add_subplot(figures + 12)
    ax2.plot(y1_n)
    ax1.title.set_text('EMG')
    ax2.title.set_text('2 pásmo vl.koef')
    ax1.set(xlabel="Vzorky[-]", ylabel="Napětí")
    ax2.set(xlabel="Vzorky[-]", ylabel="Napětí")
    plt.show()
    # vykresleni
    fig4 = plt.figure()
    figures = 200  # 2
    ax1 = fig4.add_subplot(figures + 11)
    ax1.plot(emg)
    ax2 = fig4.add_subplot(figures + 12)
    ax2.plot(emg_filter)
    ax1.title.set_text('původní EMG')
    ax2.title.set_text('filtrované EMG')
    ax1.set(xlabel="Vzorky[-]", ylabel="Napětí")
    ax2.set(xlabel="Vzorky[-]", ylabel="Napětí")
    plt.show()
    """
    return emg_filter


filtered_DWT = DWT(emg)
deviation, positions1, emg_detected = standard_deviation_offline_signal(filtered_DWT, 6)

filtered_TKEO = TKEO(emg)
deviation2, positions2, emg_detected2 = standard_deviation_offline_signal(filtered_TKEO, 5)

"""
# slope
EMG = np.array(y1_n)
TIME = (time.values).T
slope = []
kolik = 10
for i in range(kolik, len(TIME) - kolik):
    X = EMG[i - kolik:i + kolik]
    Y = TIME[i - kolik:i + kolik]
    # slope.append(((X * Y).mean() - X.mean() * Y.mean()) / ((X ** 2).mean() - (X.mean()) ** 2))
    s = stats.linregress(X, Y)
    slope.append(s.slope)

fig2 = plt.figure()
figures = 200  # 2
ax1 = fig2.add_subplot(figures + 11)
ax1.plot(EMG)
ax2 = fig2.add_subplot(figures + 12)
ax2.plot(slope)
ax1.title.set_text('EMG')
ax2.title.set_text('Slope')
ax1.set(xlabel="Vzorky[-]", ylabel="Napětí")
ax2.set(xlabel="Vzorky[-]", ylabel="Napětí")
plt.show()
"""
# nefunguje:
"""
#slope of peaks
peaks = signal.find_peaks(EMG)[0]
peaks = peaks[peaks < 5000]

EMG = np.array(y1_n)
TIME = (time.values).T
slope = []
kolik  = 10
E = EMG[peaks]
T = TIME[peaks]

for i in range(kolik, len(peaks) - kolik - 1):
    X = E[i-kolik:kolik+i]
    Y = T[i-kolik:kolik+i]
    s = stats.linregress(X, Y)
    g = np.gradient(X)
    slope.append(s.slope)


fig2 = plt.figure()
figures = 300 # 2
ax1 = fig2.add_subplot(figures + 11)
ax1.plot(EMG)
ax2 = fig2.add_subplot(figures + 12)
ax2.stem(peaks, EMG[peaks])
ax2.plot(EMG[:5000], "-b", linewidth = 0.5)
ax1.title.set_text('EMG')
ax2.title.set_text('Slope of peaks')
ax1.set(xlabel="Vzorky[-]", ylabel="Napětí")
ax2.set(xlabel="Vzorky[-]", ylabel="")
ax3 =fig2.add_subplot(figures + 13)
ax3.plot(slope)
plt.show()
"""


def low_pass(row_signal, fvz):
    fmez = 1
    b = signal.firwin(15, (fmez / fvz / 2), pass_zero=True)  # coefficient b of low pass filter
    return signal.filtfilt(b, 1, row_signal)


# verification of detected signal - the detected signal has length minimal 25 ms (fvz = 1000 => 25 samples)
positions = positions2
difference = np.diff(positions)
count_of_samples = 25
start_positions = []
every_start_positions = []
for d in range(len(difference) - count_of_samples):
    if difference[d] > 1 and (np.sum(difference[(d + 1):(d + count_of_samples + 1)]) <= count_of_samples + 3):
        # remove next detections in the same activity
        origin_position = positions[d - 1]
        every_start_positions.append(origin_position)
        if len(start_positions) == 0:
            start_positions.append(origin_position)
        else:
            if origin_position - start_positions[-1] > 700:
                start_positions.append(origin_position)

plt.plot(emg)
plt.plot(emg_detected2)
plt.stem(start_positions, emg_detected2[start_positions])
plt.show()
