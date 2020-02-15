from BITalino import BITalino


class OnlineProcessing:
    def __init__(self, method, read_frames=512):
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

        self.device = BITalino(nFrames=read_frames)
        self.device.start_recording()
        self.startTime = self.device.startTime

    def read_data(self):
        self.emg_current_record = self.device.read_data()

    def process_data(self):
        self.read_data()
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
        return self.result
