import pandas as pd
import numpy as np


class ClassificationTKEO:
    def __init__(self, window_length=5):
        self.window_length = window_length
        self.tkeo = []
        self.std = None
        self.filtered_emg_start = []
        self.mean_deviation_value = None
        self.emg_filtered = []

    def TKEO(self, emg):
        emg_filtered = emg[1:-1] ** 2 - emg[:-2] * emg[2:]  # np array
        emg_filtered = np.insert(emg_filtered, 0, emg_filtered[1])
        self.emg_filtered = np.append(emg_filtered, emg_filtered[-2])
        return self.emg_filtered

    def count_mean_deviation_value(self):
        self.mean_deviation_value = np.mean(self.std)

    def predict_data(self, emg, mean_value=None):
        self.mean_deviation_value = mean_value
        self.emg_filtered = self.TKEO(emg)
        self.std = pd.Series(self.emg_filtered).rolling(self.window_length).std()
        if self.mean_deviation_value is None:
            print("count deviation - mean value")
            self.count_mean_deviation_value()
        self.std[0:5] = self.std[5:10]
        return self.std > (self.mean_deviation_value * 5)
