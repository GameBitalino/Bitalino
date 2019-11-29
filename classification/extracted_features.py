import matplotlib.pyplot as plt
import pywt
from classification.LoadData import LoadData, load_parsed_record
import numpy as np
import time as timer
from scipy import signal
import time as timer
import pandas as pd

data = LoadData()
time, emg = data.load_record(r"D:\5. ročník\DP\Bitalino\recordings\EMG_date_10_15_2019_time_18_01_51.csv")
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
    return len(np.where(np.diff(np.sign(signal)))[0])


# Waveform length(WL)
def WL(signal):
    return np.sum(np.abs(np.diff(signal)))


# slope sign change
def SSC(signal):
    ssc = []
    signal = np.array(signal)
    for i in range(1, len(signal) - 1):
        pom = (signal[i] - signal[i - 1]) * (signal[i] - signal[i + 1])
        ssc.append(pom)
        """
    fig = plt.figure()
    ax1 = fig.add_subplot(211)
    ax1.plot(signal)
    ax2 = fig.add_subplot(212)
    ax2.plot(ssc)
    ax1.title.set_text('EMG')
    ax2.title.set_text('Slope sign change')
    plt.show()
    """
    return np.sum(ssc)

def STD(signal):
    return np.std(signal)

def features(signal):
    signal = abs(signal)
    start = timer.time()
    # feature = [RMS(signal), SSC(signal), MNF(signal),  MAV(signal),ZC(signal), WL(signal)]
    feature = [MAV(signal), MNF(signal), RMS(signal), WL(signal), STD(signal)]
    #print(timer.time() - start)
    #print(feature)
    return feature
