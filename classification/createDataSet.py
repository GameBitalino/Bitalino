from classification.LoadData import load_parsed_record
from classification.extracted_features import features
import numpy as np
import matplotlib.pyplot as plt


def create():
    pohyb = load_parsed_record("contractions_parts.csv")
    klid = load_parsed_record("calm.csv")

    # last column is label if it is calm or movement
    rows = np.shape(pohyb)[0]
    columns = len(features(pohyb[0])) + 1
    features_pohyb = np.zeros((rows, columns))
    for i in range(rows - 1):
        features_pohyb[i, :-1] = features(pohyb[i])

    rows2 = np.shape(klid)[0]
    features_klid = np.ones((rows2, columns))  # klid == 0
    for i in range(rows2 - 1):
        features_klid[i, :-1] = features(klid[i])

    all = np.zeros((rows + rows2 - 1, columns))
    all[0:rows, :] = features_pohyb
    all[rows - 1:, :] = features_klid
    return all
