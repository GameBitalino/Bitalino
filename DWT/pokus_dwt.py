from DWT.filtrationMethods import standard_deviation, TKEO, DWT
from classification.LoadData import LoadData

data = LoadData()
time, emg = data.load_some_record()
data.plot_data()

filtered_DWT = DWT(emg)
standard_deviation(filtered_DWT)

filtered_TKEO = TKEO(emg)
standard_deviation(filtered_TKEO)

"""
# slope
EMG = np.array(y1_n)
TIME = (time.values).T
slope = []
kolik = 10
for i in range(kolik, len(TIME) - kolik):
    X = EMG[i - kolik:i + kolik]
    Y = TIME[i - kolik:i + kolik]
    # slope.append(((X * Y).mean() - X.mean() * Y.mean()) / ((X ** 2).mean() - (X.mean()) ** 2))
    s = stats.linregress(X, Y)
    slope.append(s.slope)

fig2 = plt.figure()
figures = 200  # 2
ax1 = fig2.add_subplot(figures + 11)
ax1.plot(EMG)
ax2 = fig2.add_subplot(figures + 12)
ax2.plot(slope)
ax1.title.set_text('EMG')
ax2.title.set_text('Slope')
ax1.set(xlabel="Vzorky[-]", ylabel="Napětí")
ax2.set(xlabel="Vzorky[-]", ylabel="Napětí")
plt.show()
"""
# nefunguje:
"""
#slope of peaks
peaks = signal.find_peaks(EMG)[0]
peaks = peaks[peaks < 5000]

EMG = np.array(y1_n)
TIME = (time.values).T
slope = []
kolik  = 10
E = EMG[peaks]
T = TIME[peaks]

for i in range(kolik, len(peaks) - kolik - 1):
    X = E[i-kolik:kolik+i]
    Y = T[i-kolik:kolik+i]
    s = stats.linregress(X, Y)
    g = np.gradient(X)
    slope.append(s.slope)


fig2 = plt.figure()
figures = 300 # 2
ax1 = fig2.add_subplot(figures + 11)
ax1.plot(EMG)
ax2 = fig2.add_subplot(figures + 12)
ax2.stem(peaks, EMG[peaks])
ax2.plot(EMG[:5000], "-b", linewidth = 0.5)
ax1.title.set_text('EMG')
ax2.title.set_text('Slope of peaks')
ax1.set(xlabel="Vzorky[-]", ylabel="Napětí")
ax2.set(xlabel="Vzorky[-]", ylabel="")
ax3 =fig2.add_subplot(figures + 13)
ax3.plot(slope)
plt.show()
"""
