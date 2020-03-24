import numpy as np
from compare_algorithm.count_parameters import Count
from compare_algorithm.online_detection_without_bitalino import OnlineProcessing
from classification.LoadData import LoadData
import csv
from itertools import zip_longest
import os

# path:  name of proband
from results.reaction_time_statistics import load_information

path = "Verča Rem"
entries = os.listdir(path)

SIGNAL_LENGTH = 1024
loader = LoadData()


def count_reaction_time(start_samples, emg_detected, ambulance, title):
    # save reaction times
    reaction_time = []
    detected_activity_samples = []
    for sample in start_samples:
        part_emg = np.array(emg_detected[sample:sample + 3000])
        react_time = np.where(part_emg == 1)[0]  # samples where is activity
        if len(react_time) > 0:
            detected_activity_samples.append(react_time[0] + sample)
            react_time = react_time[0] / 1000
            reaction_time.append(react_time)
        else:
            reaction_time.append(0)
    #reaction_time = np.array(reaction_time)
    #reaction_time = reaction_time[np.where(reaction_time > 0)]
    whole_data = [reaction_time, ambulance, start_samples, detected_activity_samples]
    with open(title + "_.csv", "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Reaction time", "Ambulance", "Start stimulus (sample)", "Detected activity (sample)"])
        for values in zip_longest(*whole_data):
            writer.writerow(values)
    return reaction_time


for signal in entries:
    file = signal[:-4]
    if file[-10:] == "whole_data" or signal[-3:] != "csv":
        pass
    else:
        emg, clas = loader.load_record(path + os.sep + signal)
        labels = clas
        print(file)

        # processing
        signal_max = np.max(emg)
        calm_mean = np.mean(emg[:1000])
        proc_UNET = OnlineProcessing("UNET", signal_max, calm_mean)
        count_iter = int(len(emg) / 100)

        for i in range(count_iter):
            part = emg[(i * 100):(i + 1) * 100]
            part = np.array(part)
            unet = proc_UNET.process_data(part)

        proc_UNET.validation()
        unet = proc_UNET.emg_record_result
        count_UNET = Count(emg=emg, method_output=unet, labels=clas, name_of_method="UNET")
        count_UNET.plot_detected_signal(len(unet), labels=False)
        save_data = input("Chceš uložit data? ")
        if save_data == "ano":
            # load information
            title = path + os.sep + file + "_whole_data"
            reaction_time, ambulance, start_stimulus, detected_activity = load_information(title + ".csv")
            reaction_time_new = count_reaction_time(start_stimulus, unet, ambulance, title)
            print(reaction_time_new)
            reaction_time = np.array(reaction_time)
            reaction_time = reaction_time[np.where(reaction_time > 0)]
            print("prumerny reakcni cas: ", np.mean(reaction_time_new))
            print("prumerny reackci cas old: ", np.mean(reaction_time))

            data = [emg, unet]
            with open(path + os.sep + file + "_.csv", "w", newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["EMG", "Classification"])
                for values in zip_longest(*data):
                    writer.writerow(values)
            print("Saving is done ")
