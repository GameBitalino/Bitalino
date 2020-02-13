import pandas as pd
import matplotlib.pyplot as plt
import pywt
from classification.LoadData import LoadData
from .extracted_features import *
import numpy as np
from scipy import signal
import time as timer


def low_pass(row_signal, fvz):
    fmez = 1
    b = signal.firwin(15, (fmez / fvz / 2), pass_zero=True)  # koeficient b filtru DP
    return signal.filtfilt(b, 1, row_signal)


data = LoadData()
time, emg = data.load_some_record()
data.plot_data()

coeffs2 = pywt.wavedec(emg, 'bior2.2', 3)

coeffs2 = pywt.dwt(emg, 'coif6')

wavelets = pywt.wavedec(emg, 'coif6', level=6)
# zacatek je sum
sum = wavelets[-1][0:200]
# remove negative values
sum_nuly = np.where(sum < 0, 0, sum)

fig, ax = plt.subplots(len(wavelets) + 1)
ax[0].plot(emg)
for i, wavelet in enumerate(wavelets):
    ax[i + 1].plot(wavelet)

fig.tight_layout()
plt.show()

K = 5
pocet_radku = np.shape(wavelets)[0]
# H (prahování)
# výpočet adaptivního prahu
tresh = np.zeros(pocet_radku)
for j in range(pocet_radku - 1):
    s = np.median(np.abs(wavelets[j])) / 0.6745  # výpočet mediánu
    # tresh1 = s*sqrt(2*log(length(SWC(j,:)))); %universal treshold
    # tresh1 = K*s # lambda = K*sigma(std) (odhad směrodatné odchylky)
    tresh[j] = K * s

# prahovani vlnkovych koeficientu
y = np.zeros((5, 10000))
for k in range(5):
    current = wavelets[k]
    for i in range(len(current)):
        if np.abs(current[i]) > tresh[k]:
            y[k, i] = current[i]
        else:
            y[k, i] = 0

# obalka
fig, ax = plt.subplots(2)
ax[0].plot(wavelets[-1])
prah = 30
novy = []
for i in range(len(wavelets[-1])):
    if wavelets[-1][i] > prah:
        novy.append(1)
    else:
        novy.append(0)
ax[1].plot(novy)
plt.show()

### priznaky a jejich vykresleni
RMS_zavislost = []
MAV_zavislost = []
FFT_zavislost = []
Vlnk_zav = []
# for i in range(len(emg)-2000):
"""
osa = np.linspace(0, len(emg), int(len(emg) / 100))
for i in range(100, len(emg)-100, 100):
    RMS_zavislost.append(RMS(emg[i - 100:i]))
    MAV_zavislost.append(MAV(emg[i - 100: i]))
    FFT_zavislost.append(MNF(emg[i - 100:i]))
    # Vlnk_zav.append(np.mean(WT(emg[1:i+100])))
"""
for i in range(len(emg) - 100):
    RMS_zavislost.append(RMS(emg[i:i + 100]))
    MAV_zavislost.append(MAV(emg[i:i + 100]))
    FFT_zavislost.append(MNF(emg[i:i + 100]))
    # Vlnk_zav.append(np.mean(WT(emg[1:i+100])))

fig = plt.figure()
ax1 = fig.add_subplot(511)
ax1.plot(emg[:len(MAV_zavislost) * 100])
ax2 = fig.add_subplot(512)
ax2.plot(RMS_zavislost)
ax3 = fig.add_subplot(513)
ax4 = fig.add_subplot(514)
# ax5 = fig.add_subplot(515)
ax3.plot(MAV_zavislost)
ax4.plot(FFT_zavislost)
# ax5.plot(Vlnk_zav)
ax1.title.set_text('EMG')
ax2.title.set_text('RMS')
ax3.title.set_text("MAV")
ax4.title.set_text("FFT")
ax1.set(xlabel='Vzorky [-]', ylabel='Napětí [mV]')
ax2.set(xlabel="Vzorky[-]", ylabel="RMS")
ax3.set(xlabel="Vzorky[-]", ylabel="MAV")
ax4.set(xlabel="Vzorky[-]", ylabel="FFT")
plt.show()

# RMS vykresleni
fig = plt.figure()
ax1 = fig.add_subplot(211)
ax1.plot(emg[:len(RMS_zavislost) * 100])
ax2 = fig.add_subplot(212)
ax2.plot(RMS_zavislost)
ax1.title.set_text('EMG')
ax2.title.set_text('RMS')
ax1.set(xlabel='Vzorky [-]', ylabel='Napětí [mV]')
ax2.set(xlabel="Vzorky[-]", ylabel="RMS")
plt.show()

# slope of curve
length = np.random.random(10)
length.sort()
time = np.random.random(10)
time.sort()
slope, intercept = np.polyfit(emg, time, 1)
print(slope)
plt.loglog(length, time, '--')
plt.show()
