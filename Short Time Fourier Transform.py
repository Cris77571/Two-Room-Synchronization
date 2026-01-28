'Short Time Fourier Transform for Two Room system'
import pandas as pd
import numpy as np
from scipy.signal import ShortTimeFFT
from scipy.signal import stft
from scipy.signal.windows import hann
import matplotlib.pyplot as plt

df = pd.read_csv('C:/Cristian Hernandez/Python Code for Two-Room/Tests/TC_Temp_Reader_2026-01-24_17-49-47.csv') # CHANGE TO FILE PATH AND NAME Average_Temp_2025-10-13_10-35-14  24hr_Test

#Setting the time I want to see 
start_time = 4
end_time = 10

subset_df = df[(df["Time (h)"] >= start_time) & (df["Time (h)"] <= end_time)]

Room_1 = subset_df["Room 1"].values
Room_2 = subset_df["Room 2"].values
times = subset_df["Time (h)"].values

fs = 1 # Sampling frequency (Sampled every second in the test)
win_len = 3600  # 1 hour window length
hop = win_len // 16 # might need to change to 8 since we have small oscillations
hann_window = hann(win_len)

stft_temp = ShortTimeFFT(
    win = hann_window, 
    fs=fs,
    hop = hop
)

# pad = win_len // 2
# Room_1_pad = np.pad(Room_1, (pad, pad), mode='constant')
# Room_2_pad = np.pad(Room_2, (pad, pad), mode='constant')

# sx1 = stft_temp.stft(Room_1_pad)
# sx2 = stft_temp.stft(Room_2_pad)

# Performing the STFT
sx1 = stft_temp.stft(Room_1)
sx2 = stft_temp.stft(Room_2)

# Setting the frequency for the y axis in cycles per hour
freq = stft_temp.f * 3600  
num_frames = sx1.shape[1]  # Number of STFT frames
frame_centers = np.arange(num_frames) * hop + win_len // 2  # in samples
time_stft = frame_centers/ 3600 + start_time

#diff_sx = np.abs(sx1) - np.abs(sx2) 

plt.subplot(1,2,1)
plt.pcolormesh(time_stft,freq, 20*np.log10(np.abs(sx1)+1e-6), shading = 'gouraud', cmap='jet')
plt.title("Short-Time Fourier Transform - Room 1")
plt.xlabel("Time (Hours)")
plt.ylabel("Frequency (Cycles/Hour)")
plt.colorbar(label="Magnitude (dB)")

plt.subplot(1,2,2)
plt.pcolormesh(time_stft,freq, 20*np.log10(np.abs(sx2)+1e-6), shading = 'gouraud', cmap='jet') # coolwarm
plt.title("Short-Time Fourier Transform - Room 2")
plt.xlabel("Time (Hours)")
plt.ylabel("Frequency (Cycles/Hour)")
plt.colorbar(label="Magnitude (dB)")

plt.show()