import statistics

import numpy as np


class ClassificationTKEO:
    def __init__(self, window_half_length=2):
        self.window_half_length = 2
        self.tkeo = []

    def TKEO(self, EMG_for_TKEO):
        self.tkeo = []
        for i in range(1, len(EMG_for_TKEO) - 1):
            self.tkeo.append(EMG_for_TKEO[i] ** 2 - EMG_for_TKEO[i - 1] * EMG_for_TKEO[i + 1])
        return self.tkeo

    def count_mean_deviation_value(self):
        self.mean_deviation_value = np.mean(self.deviation[:512])

    def predict_data(self, emg, mean_value=None):
        self.mean_deviation_value = mean_value
        emg_filtered = self.TKEO(emg)
        self.deviation = []
        for i in range(self.window_half_length, len(emg_filtered) - self.window_half_length):
            self.deviation.append(
                statistics.stdev(emg_filtered[i - self.window_half_length:i + self.window_half_length]))
        if self.mean_deviation_value is None:
            self.count_mean_deviation_value()
        return self.deviation > (self.mean_deviation_value * 5)
