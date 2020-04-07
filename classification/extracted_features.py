import pywt
import numpy as np


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
    return np.sum(ssc)


def STD(signal):
    return np.std(signal)


def features(signal):
    signal = abs(signal)
    # feature = [RMS(signal), SSC(signal), MNF(signal),  MAV(signal),ZC(signal), WL(signal)]
    feature = [MAV(signal), MNF(signal), RMS(signal), WL(signal), STD(signal)]
    return feature
