from pandas import read_csv
import numpy as np
from pandas import DataFrame as df
import os

path = "Bětka"
entries = os.listdir(path)


def load_information(path):
    data = read_csv(path, delimiter=',',
                    decimal=".")
    reaction_time = data.iloc[:, 0]
    ambulance = data.iloc[:, 1]
    start_stimulus = data.iloc[:, 2]
    detected_activity = data.iloc[:3]
    return reaction_time, ambulance, start_stimulus, detected_activity


def load_concrete_reaction_times(path):
    data = read_csv(path, delimiter=',',
                    decimal=".")
    sem = data.loc[data['Ambulance'] == False]
    change_to_green = sem[::2]
    change_to_red = sem[1::2]
    display_ambulance = data.loc[data['Ambulance'] == True]
    return change_to_green, change_to_red, display_ambulance


for signal in entries:
    file = signal[:-4]
    if signal[-3:] != "csv":
        pass
    elif file[-11:] == "whole_data_":
        path = path + os.sep + signal
        reaction_time, ambulance, start_stimulus, detected_activity = load_information(path)
        change_to_green, change_to_red, display_ambulance = load_information(path)
