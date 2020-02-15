import numpy as np
import math
from BITalino import BITalino


class OnlineProcessing:
    def __init__(self, method):
        self.emg_record = []
        self.emg_current_record = []
        self.mean_value_calm_emg = None
        self.method = method
        self.result = []

        if self.method == "UNET":
            from segmentation.ClassificationUNET import ClassificationUNET
            self.model_unet = ClassificationUNET()  # return ndarray

        elif self.method == "SVM":
            from classification.SVM_clasifficator import ClassificationSVM
            self.model_svm = ClassificationSVM(nFrames=10)  # return ndarray

        elif self.method == "TKEO":
            from DWT.ClassificationTKEO import ClassificationTKEO
            self.model_tkeo = ClassificationTKEO()  # return ndarray - true/false

        else:
            raise ValueError('Wrong method.')

        self.device = BITalino(time=10 * 1000)
        self.device.start_recording()

    def read_data(self):
        self.emg_current_record = self.device.read_data()

    def process_data(self):
        if self.method == "UNET":
            self.result = self.model_unet.predict_data(emg=self.emg_current_record)

        elif self.method == "SVM":
            self.result = self.model_svm.predict_data(emg=self.emg_current_record)

        elif self.method == "TKEO":
            if self.mean_value_calm_emg is not None:
                self.result = self.model_tkeo.predict_data(emg=self.emg_current_record,
                                                           mean_value=self.model_tkeo.mean_deviation_value)
            else:
                self.result = self.model_tkeo.predict_data(emg=self.emg_current_record)
        else:
            raise ValueError('Wrong method.')

