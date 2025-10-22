import pandas as pd
from scipy.signal import find_peaks
import matplotlib.pyplot as plt

df = pd.read_csv('C:/Cristian Hernandez/Python Code for Two-Room/Tests/Average_Temp_2025-10-13_10-35-14.csv') # CHANGE TO FILE PATH AND NAME

#Setting the x-axis as time (hours)
x = df.iloc[:,0]

Room_1 = df["Room 1"]
Room_2 = df["Room 2"]
peaks1, _ = find_peaks(Room_1, height = 81.25, distance=40, prominence=1)
peaks2, _ = find_peaks(Room_2, height = 81.25, distance =40, prominence=1)

plt.plot(x, Room_1, label = 'Room 1', color = 'r')
plt.plot(x.iloc[peaks1], Room_1.iloc[peaks1],'x', label = 'Room 1 Peak', color = 'r')

plt.plot(x, Room_2, label = 'Room 2', color = 'b')
plt.plot(x.iloc[peaks2], Room_2.iloc[peaks2],'x', label = 'Room 2 Peak', color = 'b')

# Plot for Temperature with Peaks
plt.title('Average Room Temperatures with Peaks')
plt.xlabel('Time (Hours)') 
plt.ylabel('Temperature (\u00b0F)')
plt.legend()
plt.grid(True)
plt.show()

min_len = min(len(peaks1), len(peaks2))
peaks1_diff = Room_1.iloc[peaks1[:min_len]].reset_index(drop=True)
peaks2_diff = Room_2.iloc[peaks2[:min_len]].reset_index(drop=True)
time_peaks = x.iloc[peaks1[:min_len]].reset_index(drop=True)

peak_diff = peaks1_diff - peaks2_diff # Difference between peaks

# Plot for room temperature difference
plt.figure()
plt.plot(time_peaks, peak_diff, linestyle='-', color='purple')
plt.title('Difference Between Peaks (Room 1 - Room 2)')
plt.xlabel('Time (Hours)')
plt.ylabel('Temperature Difference (\u00b0F)')
plt.grid(True)
plt.show()