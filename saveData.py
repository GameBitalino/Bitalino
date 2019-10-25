from pandas import DataFrame
from datetime import datetime
import csv

now = datetime.now()
name = "EMG_date_" + now.strftime("%m_%d_%Y") + "_time_"+ str(now.strftime("%H_%M_%S") + ".csv")

def saveEMG(time, EMG):
    time.tolist()
    EMG.tolist()
    Data = {'Time':time,
            'EMG': EMG
            }
    df = DataFrame(Data, columns=['Time', 'EMG'])
    df.to_csv(name, index=None,
                           header=True)  # Don't forget to add '.csv' at the end of the path
    print("Saving is done " + name)