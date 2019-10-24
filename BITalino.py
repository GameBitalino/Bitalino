import bitalino
from time import sleep
import numpy as np
from matplotlib import pyplot as plt
from pandas import DataFrame
from datetime import datetime


class BITalino:

    def __init__(self, time, fvz=1000):
        self.macAddress = "20:18:06:13:21:59"
        self.fvz = fvz
        self.nframes = 100
        self.device = None
        self.emg_record_current_frame = []
        self.emg_full_record = []
        self.running_time = time
        self.time_line = []

    def start_recording(self):
        self.device = bitalino.BITalino(self.macAddress)
        sleep(1)
        self.device.start(self.fvz, [0])
        print("START")

    def read_data(self):
        self.emg_record_current_frame = self.device.read(self.nframes)[:, -1]
        self.emg_full_record = np.concatenate([self.emg_full_record, self.emg_record_current_frame])
        return self.emg_record_current_frame

    def get_recording(self):
        print(len(self.emg_full_record))
        return self.emg_full_record

    def stop_recording(self):
        self.device.stop()
        self.device.close()
        print("STOP")

    def plot_graph(self):
        # subtract mean value
        meanValue = np.mean(self.emg_full_record)
        for i in range(len(self.emg_full_record)):
            self.emg_full_record[i] -= meanValue

        self.time_line = np.linspace(0, int(self.running_time), len(self.emg_full_record))
        # plot EMG record
        plt.figure()
        plt.style.use("ggplot")
        plt.plot(self.time_line, self.emg_full_record)
        plt.title("EMG")
        plt.xlabel("Time [s]")
        plt.ylabel("Voltage [μV]")
        plt.show()

    def save_data(self):
        now = datetime.now()
        path = r"D:\Diplomka - Hra\zaznam\recordingsData"
        name = path + "\EMG_record_" + now.strftime("%m_%d_%Y") + "_time_" + str(now.strftime("%H_%M_%S") + ".csv")
        self.time_line = np.linspace(0, int(self.running_time*60), len(self.emg_full_record))
        print(self.running_time)
        print(self.time_line)
        print(self.emg_full_record)
        self.time_line.tolist()
        self.emg_full_record.tolist()
        data = {'Time': self.time_line,
                'EMG': self.emg_full_record
                }
        df = DataFrame(data, columns=['Time', 'EMG'])
        df.to_csv(name, index=None, header=True)  # Don't forget to add '.csv' at the end of the path
        print("Saving is done")
