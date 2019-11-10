import matplotlib.pyplot as plt
import pywt
from DWT.LoadData import LoadData
import numpy as np
from scipy import signal
import time as timer
import pandas as pd

data = LoadData()
time, emg = data.load_record(r"D:\5. ročník\DP\Bitalino\recordings\EMG_klid.csv")
data.plot_data()

wavelets = pywt.wavedec(emg, 'coif6', level=6)[-1]  # last


def RMS(signal):  # root mean square
    return np.sqrt(sum(signal ** 2) / len(signal))


def MAV(signal):  # mean absolute value
    return np.sum(np.abs(signal)) / len(signal)


def MNF(signal):  # mean freqency from amplitude spectrum
    FT = np.abs(np.fft.fft(signal))
    N = int(len(FT) / 2)
    return np.sum(FT[0:N]) / N


def WT(signal):
    return pywt.dwt(signal, 'coif6', mode='symmetric', axis=-1)


# zero crossing
def ZC(signal):
    return np.where(np.diff(np.sign(signal)))[0]

# Waveform length(WL)
def WL(signal):
    return np.sum(np.abs(np.diff(signal)))


# slope sign change
def SSC(signal):
    ssc = []
    for i in range(1, len(signal) - 1):
        pom = (signal[i] - signal[i - 1])*(signal[i] - signal[i + 1])
        ssc.append(pom)
    fig = plt.figure()
    ax1 = fig.add_subplot(211)
    ax1.plot(signal)
    ax2 = fig.add_subplot(212)
    ax2.plot(ssc)
    ax1.title.set_text('EMG')
    ax2.title.set_text('Slope sign change')
    plt.show()
    return np.sum(ssc)