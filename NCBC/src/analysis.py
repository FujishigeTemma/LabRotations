import os

import h5py as h5
import matplotlib.pyplot as plt
import numpy as np
from recorders.db import DB
from scipy.signal import correlate, welch

dt = 0.1
fs = 1000 / dt


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


def analyze(output, job_id):
    f = h5.File(os.path.join(output, job_id, "ring.h5"), "r")
    data = f["action_potentials/Population(BasketCell)#1"]
    assert isinstance(data, h5.Dataset)

    data = [spikes for spikes in data if len(spikes) > 0]

    max_time = int(np.ceil(np.max([np.max(spikes) for spikes in data]) * fs / 1000))
    binary_data = preprocess(data, fs, max_time)

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

    # 周波数の最大値を1000Hzに設定
    max_freq = 1000
    freq_indices = np.where(mean_freq <= max_freq)[0]
    mean_freq = mean_freq[freq_indices]
    mean_psd = mean_psd[freq_indices]

    # 0-20Hz, 20-100Hz, 100-300Hzの区間での密度の最大値を求める
    freq_ranges = [(0, 20), (20, 100), (100, 300)]
    max_psd_values = []

    for fmin, fmax in freq_ranges:
        freq_indices = np.where((mean_freq >= fmin) & (mean_freq <= fmax))[0]
        max_psd = np.max(mean_psd[freq_indices])
        max_psd_values.append(max_psd)

    plt.figure(figsize=(10, 4))
    plt.subplot(1, 2, 1)
    plt.plot(np.arange(len(mean_autocorr)) / fs, mean_autocorr)
    plt.xlabel("Time lag (s)")
    plt.ylabel("Auto-correlation")
    plt.title("Mean Auto-correlation")

    plt.subplot(1, 2, 2)
    plt.plot(mean_freq, mean_psd)
    for freq in [20, 100, 300]:
        plt.axvline(x=freq, color="red", linestyle="--", linewidth=1)

    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Power Spectral Density")
    plt.title("Mean Power Spectral Density")
    plt.tight_layout()
    plt.savefig(os.path.join(output, job_id, "analysis.png"))

    with DB(os.path.join(output, "ring.sqlite")) as db:
        db.update_density("jobs", job_id, *max_psd_values)

    return plt.close("all")
