from sklearn.svm import SVC
from classification.prepareData import *
from classification.extracted_features import features
from classification.prepareData import rectification, normalization
from joblib import dump, load


def drawTwo(first, second):
    data = createDataset()
    #  feature = [RMS(signal), SSC(signal), MNF(signal),  MAV(signal),ZC(signal), WL(signal)]
    y = data[:, -1]  # last column
    X = data[:, first:second + 1]  # select just 2 features
    y[y == 0] = -1  # klid
    ind = np.random.rand(len(y)) > 0.2

    X_train = X[ind, :]
    y_train = y[ind]
    X_test = X[ind == 0, :]
    y_test = y[ind == 0]

    muj_SVM = SVC(gamma='scale', kernel='poly', C=10,
                  degree=3)  # C - kolik bodu muze byt spatne - jak vybrat: ve for cyklu hodnoti klasifikaci - cross validace
    muj_SVM.fit(X_train, y_train)

    # vykresleni
    xx1, xx2 = np.meshgrid(np.linspace(np.min(X[:, 0]), np.max(X[:, 0]), 100),
                           np.linspace(np.min(X[:, 1]), np.max(X[:, 1]), 100))
    xx = np.stack((xx1.ravel(), xx2.ravel()), axis=1)

    yy = muj_SVM.predict(xx)
    yy = yy.reshape(xx1.shape)

    plt.contourf(xx1, xx2, yy)
    plt.scatter(X_test[:, 0], X_test[:, 1], c=y_test)
    plt.show()


def SVMmodel(d=3, pocetZlych=5, name="SVM_model"):
    data = createDataset()
    y = data[:, -1]  # last column
    X = data[:, :-1]
    y[y == 0] = -1  # klid
    X_train = X
    y_train = y

    muj_SVM = SVC(gamma='scale', kernel='poly', C=pocetZlych,
                  degree=d)  # C - kolik bodu muze byt spatne - jak vybrat: ve for cyklu hodnoti klasifikaci - cross validace
    muj_SVM.fit(X_train, y_train)
    dump(muj_SVM, name + ".joblib")
    return muj_SVM


def countAll(model_SVM, x_test):
    muj_SVM = model_SVM
    feature = features(x_test)
    if muj_SVM.predict(np.array([feature])) == 1:
        return [0, "klid"]
    else:
        return [1, "kontrakce"]


def predictData(model, emg, max=None, nFrames=10):
    emg = rectification(emg)
    emg = normalization(emg, max)
    detection = np.ones(len(emg))
    for i in range(int(len(emg) / nFrames) - 1):
        vysl = countAll(model, emg[i * nFrames:(i + 1) * nFrames])[0]
        detection[i * nFrames:(i + 1) * nFrames] = np.ones(nFrames) * vysl
    return detection
