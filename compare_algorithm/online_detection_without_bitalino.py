from pandas import DataFrame
from BITalino import BITalino
import numpy as np
import matplotlib.pyplot as plt
from time import time


class OnlineProcessing:
    def __init__(self, method, max_value_emg, mean_value_calm_emg, read_frames=100):
        self.emg_record = []
        self.emg_current_record = []
        self.mean_value_calm_emg = mean_value_calm_emg
        self.method = method
        self.current_emg_result = []
        self.emg_record_result = []
        self.max_value_emg = max_value_emg
        self.reaction_time = []
        self.title_save_file = []
        self.duration = []

        if self.method == "UNET":
            from segmentation.ClassificationUNET import ClassificationUNET
            self.model_unet = ClassificationUNET()  # return ndarray

        elif self.method == "SVM":
            from classification.ClassificationSVM import ClassificationSVM
            self.model_svm = ClassificationSVM(nFrames=10)  # return ndarray

        elif self.method == "TKEO":
            from DWT.ClassificationTKEO import ClassificationTKEO
            self.model_tkeo = ClassificationTKEO()  # return ndarray - true/false

        else:
            raise ValueError('Wrong method.')

    def process_data(self, emg_current_record):
        self.emg_current_record = emg_current_record
        self.emg_record = np.concatenate([self.emg_record, emg_current_record])
        start = time()
        if self.method == "UNET":
            self.current_emg_result = self.model_unet.predict_data(emg=self.emg_current_record)

        elif self.method == "SVM":
            self.current_emg_result = self.model_svm.predict_data(emg=self.emg_current_record,
                                                                  maximum=self.max_value_emg)


        elif self.method == "TKEO":
            self.current_emg_result = self.model_tkeo.predict_data(
                emg=self.emg_current_record, mean_value=self.mean_value_calm_emg)
        else:
            raise ValueError('Wrong method.')
        dur = time() - start
        self.duration.append(dur)
        self.emg_record_result = np.concatenate([self.emg_record_result, self.current_emg_result])
        activity_result = np.sum(self.current_emg_result[:-50]) > 40
        # print("activity: " + str(activity_result))
        return activity_result  # return true/false

    def validation(self):
        # emg must be length more than 25 milliseconds (25 samples)
        d = np.diff(self.emg_record_result)
        count_of_samples = int(25000 / 1000)  # 25 samples if fvz = 1000
        change_to_activity = np.where(d == 1)
        self.emg_record_result = np.array(self.emg_record_result)
        for it in change_to_activity[0]:
            if it + count_of_samples >= len(self.emg_record_result):
                self.emg_record_result = np.array(list(self.emg_record_result) + list(np.zeros(25)))
            interval = self.emg_record_result[(it + 1):(it + count_of_samples + 1)]
            if np.sum(interval) < count_of_samples:
                replace = 0
            else:
                replace = 1
            self.emg_record_result[(it + 1):(it + count_of_samples + 1)] = replace
