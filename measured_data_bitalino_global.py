from datetime import datetime

from pandas import DataFrame

from BITalino import BITalino
from numpy import sum, max, concatenate
import need_py_speed_game.Game.variables_for_reaction_time as reaction_times


class OnlineProcessing:
    def __init__(self, method, read_frames=100):
        self.emg_record = []
        self.emg_current_record = []
        self.mean_value_calm_emg = None
        self.method = method
        self.current_emg_result = []
        self.emg_record_result = []
        self.max_value_emg = 650

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
        print("Connecting BITalino...")
        self.device = BITalino(nFrames=read_frames)
        self.device.start_recording()
        self.startTime = self.device.startTime

    def read_data(self):
        self.emg_current_record = self.device.read_data()
        self.emg_record = self.device.emg_full_record

    def count_max_of_signal(self):
        self.max_value_emg = max(self.emg_record)

    def process_data(self):
        self.read_data()
        if self.method == "UNET":
            self.current_emg_result = self.model_unet.predict_data(emg=self.emg_current_record)

        elif self.method == "SVM":
            self.current_emg_result = self.model_svm.predict_data(emg=self.emg_current_record,
                                                                  maximum=self.max_value_emg)


        elif self.method == "TKEO":
            if self.mean_value_calm_emg is not None:
                self.current_emg_result = self.model_tkeo.predict_data(emg=self.emg_current_record,
                                                                       mean_value=self.model_tkeo.mean_deviation_value)
            else:
                self.current_emg_result = self.model_tkeo.predict_data(emg=self.emg_current_record)
        else:
            raise ValueError('Wrong method.')
        self.emg_record_result = concatenate([self.emg_record_result, self.current_emg_result])
        activity_result = sum(self.current_emg_result[:-50]) > 40
        print("activity: " + str(activity_result))
        return activity_result  # return true/false

    def save_EMG(self):
        title = "./recordings/EMG_date_" + self.device.startTime.strftime("%d_%m_%Y") + "_time_" + str(
            self.device.startTime.strftime("%H_%M_%S") + ".csv")

        Data = {
            'EMG': self.emg_record,
            'Classification': self.emg_record_result
        }
        df = DataFrame(Data, columns=['EMG', 'Classification'])
        df.to_csv(title, index=None,
                  header=True)  # Don't forget to add '.csv' at the end of the path
        print("Saving is done " + title)

    def count_reaction_time(self):
        # TODO
        print("dodedej")
        reaction_time = []
        return reaction_time
