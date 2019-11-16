import statistics
import time as timer
import numpy as np
import pandas as pd
import pywt
from matplotlib import pyplot as plt
from scipy import signal
from DWT.pokus_dwt import emg


# calculation of standard deviation in floating window
def standard_deviation(emg_filter, window_half_length=2):
    deviation = []
    for i in range(window_half_length, len(emg_filter) - window_half_length):
        deviation.append(statistics.stdev(emg_filter[i - window_half_length:i + window_half_length]))

    calm_deviation = np.mean(deviation[:500])
    draw = emg[window_half_length:-window_half_length]
    emg_filter = pd.Series(emg_filter)
    plt.figure()
    plt.plot(draw, 'b')
    plt.plot(emg_filter[np.array(np.where(deviation > (calm_deviation * 2))[0])], color='red')
    plt.title('Detekovaná aktivita EMG')
    plt.legend(['klid', 'aktivita'])
    plt.xlabel(xlabel="Vzorky[-]")
    plt.ylabel(ylabel='Napětí []')
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
    return deviation


# TKEO - filtration
def TKEO(EMG_for_TKEO):
    start = timer.time()
    tkeo = []
    for i in range(1, len(EMG_for_TKEO) - 1):
        tkeo.append(EMG_for_TKEO[i] ** 2 - EMG_for_TKEO[i - 1] * EMG_for_TKEO[i + 1])

    print('Time for TKEO: ', timer.time() - start)
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
    return tkeo


def low_pass(row_signal, fvz):
    fmez = 1
    b = signal.firwin(15, (fmez / fvz / 2), pass_zero=True)  # coefficient b of low pass filter
    return signal.filtfilt(b, 1, row_signal)


def DWT(emg, wave='coif6', level=6):
    wavelets = pywt.wavedec(emg, wavelet=wave, level=6)

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
    """
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
    return emg_filter
