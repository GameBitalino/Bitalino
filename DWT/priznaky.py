import matplotlib.pyplot as plt
import pywt
from DWT.LoadData import LoadData
import numpy as np
from scipy import signal
import time as timer
import pandas as pd

data = LoadData()
time, emg = data.load_some_record()
data.plot_data()

wavelets = pywt.wavedec(emg, 'coif6', level=6)[-1] # last
def RMS(signal): #root mean square
    return np.sqrt(sum(signal**2)/len(signal))

def MAV(signal): #mean absolute value
    return np.sum(np.abs(signal))/len(signal)

def MNF(signal): #mean freqency from amplitude spectrum
    FT = np.abs(np.fft.fft(signal))
    N = int(len(FT)/2)
    return np.sum(FT[0:N])/N

def WT(signal):
    return pywt.dwt(signal, 'coif6',  mode='symmetric', axis=-1)
