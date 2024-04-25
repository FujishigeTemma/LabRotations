import h5py as h5
import numpy as np
from scipy.signal import correlate, welch


def preprocess(data, fs, max_time):
    N = len(data)
    binary_data = []

    for i in range(N):
        spike_times = data[i]
        spike_train = np.zeros(max_time)
        spike_indices = (spike_times * fs / 1000).astype(int)
        spike_train[spike_indices] = 1
        binary_data.append(spike_train)

    return binary_data


def analyze(binary_data, fs):
    N = len(binary_data)
    autocorr_list = []
    psd_list = []
    freq_list = []

    for i in range(N):
        spike_train = binary_data[i]

        # 自己相関関数の計算
        autocorr = correlate(spike_train, spike_train, mode="full")
        autocorr = autocorr[len(autocorr) // 2 :]
        autocorr_list.append(autocorr / np.max(autocorr))  # 自己相関関数を正規化

        # パワースペクトル密度の計算
        freq, psd = welch(spike_train, fs=fs, nperseg=len(spike_train))
        psd_list.append(psd / np.max(psd))  # パワースペクトル密度を正規化
        freq_list.append(freq)

    # 自己相関関数の平均
    max_len = max(len(autocorr) for autocorr in autocorr_list)
    autocorr_padded = np.array([np.pad(autocorr[1:], (0, max_len - len(autocorr)), "constant") for autocorr in autocorr_list])
    mean_autocorr = np.mean(autocorr_padded, axis=0)

    # パワースペクトル密度の平均
    max_freq_len = max(len(freq) for freq in freq_list)
    psd_padded = np.array([np.pad(psd, (0, max_freq_len - len(psd)), "constant") for psd in psd_list])
    mean_psd = np.mean(psd_padded, axis=0)
    mean_freq = freq_list[0][:max_freq_len]  # 周波数軸は全て同じ

    return mean_autocorr, mean_freq, mean_psd


f = h5.File("outputs/job_01hwb3r8vqfzqb0ks9dzmzft9a/ring.h5", "r")
data = f["action_potentials/Population(BasketCell)#1"]
assert isinstance(data, h5.Dataset)

# 使用例
dt = 0.1
fs = 1000 / dt
max_time = int(np.ceil(np.max([np.max(spikes) for spikes in data]) * fs / 1000))
binary_data = preprocess(data, fs, max_time)
mean_autocorr, mean_freq, mean_psd = analyze(binary_data, int(fs))

# 結果の可視化
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 4))
plt.subplot(1, 2, 1)
plt.plot(np.arange(len(mean_autocorr)) / fs, mean_autocorr)
plt.xlabel("Time lag (s)")
plt.ylabel("Auto-correlation")
plt.title("Mean Auto-correlation")

plt.subplot(1, 2, 2)
plt.plot(mean_freq, mean_psd)
plt.xlabel("Frequency (Hz)")
plt.ylabel("Power Spectral Density")
plt.title("Mean Power Spectral Density")
plt.tight_layout()
plt.show()
