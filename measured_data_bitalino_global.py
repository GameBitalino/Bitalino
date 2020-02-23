from datetime import datetime

from pandas import DataFrame

from BITalino import BITalino
import numpy as np
import matplotlib.pyplot as plt


class OnlineProcessing:
    def __init__(self, method, read_frames=100):
        self.emg_record = []
        self.emg_current_record = []
        self.mean_value_calm_emg = None
        self.method = method
        self.current_emg_result = []
        self.emg_record_result = []
        self.max_value_emg = 650
        self.reaction_time = []
        self.title_save_file = []

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
        self.max_value_emg = np.max(self.emg_record)

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
        self.emg_record_result = np.concatenate([self.emg_record_result, self.current_emg_result])
        activity_result = np.sum(self.current_emg_result[:-50]) > 40
        print("activity: " + str(activity_result))
        return activity_result  # return true/false

    def save_EMG(self):
        self.validation()
        self.title = "./recordings/game_EMG_date_" + self.device.startTime.strftime("%d_%m_%Y") + "_time_" + str(
            self.device.startTime.strftime("%H_%M_%S"))
        if len(self.emg_record) != len(self.emg_record_result):
            self.emg_record_result = self.emg_record_result[:len(self.emg_record)]
        print(len(self.emg_record))
        print(len(self.emg_record_result))
        data = {
            'EMG': self.emg_record,
            'Classification': self.emg_record_result
        }
        df = DataFrame(data, columns=['EMG', 'Classification'])
        df.to_csv(self.title + ".csv", index=None,
                  header=True)
        print("Saving is done " + self.title + ".csv")
        import pandas as pd
        pom = pd.Series(self.emg_record)
        pom_result = pd.Series(self.emg_record_result)
        print(pom_result)
        plt.plot(pom)
        plt.plot(pom[np.array(np.where(pom_result == 1))[0]], color='red')
        # plt.plot(pom_result * 100 + 500)
        plt.show()

    def validation(self):
        # emg must be length more than 25 milliseconds (25 samples)
        d = np.diff(self.emg_record_result)
        count_of_samples = int(25000 / self.device.fvz)  # 25 samples if fvz = 1000
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

    def count_reaction_time(self):
        self.validation()
        stimulus = get_reaction_times()
        delta_time = []
        samples = []
        for item in stimulus:
            seconds = (item - self.startTime).total_seconds()
            delta_time.append(seconds)
            samples.append(int(seconds) * self.device.fvz)

        for sample in samples:
            part_emg = np.array(self.emg_record_result[sample:])
            react_time = np.where(part_emg == 1)[0]
            if len(react_time) > 0:
                react_time = react_time[0] / self.device.fvz
                self.reaction_time.append(react_time)
        # save reaction times
        data = {
            'Reaction times': self.reaction_time
        }
        df = DataFrame(data, columns=['Reaction times'])
        df.to_csv(self.title + "reaction_times.csv", index=None,
                  header=True)

        return self.reaction_time


def reaction_times_init():
    global reaction_times
    reaction_times = []


def reaction_times_add_time(new_time):
    global reaction_times
    reaction_times.append(new_time)


def get_reaction_times():
    global reaction_times
    return reaction_times
