from pandas import DataFrame
from datetime import datetime
import csv
import numpy as np

now = datetime.now()
name = "./recordings/EMG_date_" + now.strftime("%d_%m_%Y") + "_time_" + str(now.strftime("%H_%M_%S") + ".csv")


def saveEMG(time, EMG, title=name):
    time.tolist()
    EMG.tolist()
    Data = {'Time': time,
            'EMG': EMG
            }
    df = DataFrame(Data, columns=['Time', 'EMG'])
    df.to_csv(title, index=None,
              header=True)  # Don't forget to add '.csv' at the end of the path
    print("Saving is done " + title)


name_parse = "./recordings/EMG_date_" + now.strftime("%d_%m_%Y") + "_time_" + str(
    now.strftime("%H_%M_%S") + "_parsed_.csv")


def savePartsOfEMG(emg, nFrames=100, title=name_parse):
    rows = int(len(emg) / nFrames) - 1
    matrix = np.zeros((rows, nFrames))
    for i in range(rows):
        if i == 0:
            matrix[i, :] = emg[0:nFrames]
        else:
            matrix[i, :] = emg[nFrames * i:nFrames * (i + 1)]
    df = DataFrame(matrix)
    df.to_csv(title, index=None,
              header=True)  # Don't forget to add '.csv' at the end of the path
    print("Saving is done " + title)


def saveLabeledData(emg, labels, path, nFrames=512):
    files = int(len(emg) / nFrames) - 1
    matrix = np.zeros((2, nFrames))
    for i in range(files):
        if i == 0:
            matrix[0, :] = emg[0:nFrames]
            matrix[1, :] = labels[0:nFrames]
        else:
            matrix[0, :] = emg[nFrames * i:nFrames * (i + 1)]
            matrix[1, :] = labels[nFrames * i:nFrames * (i + 1)]
        df = DataFrame(matrix)
        df.to_csv(path + "_labels_parsed_" + str(i) + ".csv", index=None,
                  header=True)  # Don't forget to add '.csv' at the end of the path
    print("Saving is done " + path)
