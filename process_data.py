# External
import os
from obspy import UTCDateTime, read, read_inventory
import numpy as np
import matplotlib.pyplot as plt

# Define directories
localdir = os.path.dirname(os.path.abspath(__file__))
datadir = os.path.join(localdir, 'data')
waveformdir = os.path.join(datadir, 'waveforms')
stationdir = os.path.join(datadir, 'stations')

# %% 
# Read in the data
print("Loading ...")
st = read(os.path.join(waveformdir, "*.mseed"))
inv = read_inventory(os.path.join(stationdir, "*.xml"))
stbu = st.copy()

# %%
# Merge traces IMPORTANT!!!! 
print("Merging ...")
st.merge()

# %%
# Quick processing
print("Removing response ...")
st.attach_response(inv)
pre_filt = [0.0009, 0.001, 0.003, 0.001]
st.remove_response(inv, output='VEL', water_level=10, pre_filt=pre_filt)

# %%
print("Filtering and resampling ...")
sampling_rate = 0.1
st.filter("bandpass", freqmin=pre_filt[1], freqmax=pre_filt[2])
st.resample(sampling_rate, window='hanning')

# %%
# Plot the third trace
print("Plotting ...")
st[1].plot(block=False)

# %%
# Get raw data
t = st[1].times()
dt = t[1] - t[0]
y = st[1].data


# %%
Y    = np.fft.fft(y)
freq = np.fft.fftfreq(len(y), dt)

# %%
# Plot 
plt.figure()
plt.plot(freq, np.abs(Y))
plt.xlim(0.0005, 0.0032)
plt.xlabel('Hz')
plt.ylabel('$|\hat{Y}|$')
plt.show(block=True)
