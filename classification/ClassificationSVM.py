import numpy as np
from classification.SVM_clasifficator import countAll
from classification.prepareData import rectification, normalization


class ClassificationSVM:
    def __init__(self, nFrames=10):
        self.svm_model = None
        self.nFrames = nFrames
        from joblib import load
        self.svm_model = load(r'D:\5. ročník\DP\Bitalino\classification\svm_model.joblib')

    def predict_data(self, emg, max=None):
        emg = rectification(emg)
        emg = normalization(emg, max)
        detection = np.ones(len(emg))
        for i in range(int(len(emg) / self.nFrames) - 1):
            vysl = countAll(self.svm_model, emg[i * self.nFrames:(i + 1) * self.nFrames])[0]
            detection[i * self.nFrames:(i + 1) * self.nFrames] = np.ones(self.nFrames) * vysl
        return detection