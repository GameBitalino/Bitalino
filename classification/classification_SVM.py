import numpy as np
from classification.SVM_clasifficator import countAll
from classification.prepare_data import rectification, normalization
import os.path


class ClassificationSVM:
    def __init__(self, nFrames=10):
        self.svm_model = None
        self.nFrames = nFrames
        from joblib import load
        my_path = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(my_path, "SVM_heel_model_2.joblib")
        self.svm_model = load(path)

    def predict_data(self, emg, maximum=None):
        emg = rectification(emg)
        emg = normalization(emg, maximum)
        detection = np.ones(len(emg))
        for i in range(int(len(emg) / self.nFrames) - 1):
            vysl = countAll(self.svm_model, emg[i * self.nFrames:(i + 1) * self.nFrames])[0]
            detection[i * self.nFrames:(i + 1) * self.nFrames] = np.ones(self.nFrames) * vysl
        return detection
