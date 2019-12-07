from pandas import DataFrame
from datetime import datetime
import csv
import numpy as np
import os

path = r"D:\5. ročník\DP\Bitalino\recordings\train_data" + os.sep

zeros = list(np.zeros((1000)))
ones = list(np.ones(1000))

sample_1 = zeros[:300] + ones[:200] + zeros[:300] + ones[:200]
sample_2 = zeros + ones
sample_3 = zeros[:100] + ones[:100] + zeros[:200] + ones[:100] + zeros[:300] + ones[:50] + zeros[:50] + ones[:100]
sample_4 = zeros[:400] + ones[:100] + zeros[:200] + ones[:300]
sample_5 = ones[:100] + zeros[:800] + ones[:100]
sample_6 = ones[:800] + zeros[:200]
sample_7 = ones[:80] + zeros[:20] + ones[:100] + zeros[:200] + ones[:500] + zeros[:100]
sample_8 = ones[:200] + zeros[:20] + ones[:100] + zeros[:80] + ones[:100] + zeros[:500]
sample_9 = list(np.random.randint(2, size=1000))
sample_10 = list(np.random.randint(2, size=1000))

samples = [sample_1, sample_2, sample_3, sample_4, sample_5, sample_6, sample_7, sample_8, sample_9, sample_10]

def saveData(data, title=path):
    df = DataFrame(data)
    df.to_csv(title, index=None,
              header=True)  # Don't forget to add '.csv' at the end of the path

for v in range(10):
    title = path + str(v) + '.csv'
    saveData(samples[v], title)
