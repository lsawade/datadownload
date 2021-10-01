# %% 
# External
import os
from obspy import UTCDateTime, read, read_inventory

# 'Internal'
from download_data import download_data

# %% 
# Make directory structure for download
localdir = os.path.dirname(os.path.abspath(__file__))
datadir = os.path.join(localdir, 'data')
waveformdir = os.path.join(datadir, 'waveforms')
stationdir = os.path.join(datadir, 'stations')

def makedirs(dirlist: list):
    for _dir in dirlist:
        if os.path.exists(_dir) is False:
            os.makedirs(_dir)

dirlist = [datadir, waveformdir, stationdir]
makedirs(dirlist)

# %% 
# Now define some stations you to download data for
download_dict = dict(
    IU=['ANMO', 'HRV', 'KONO'],
    II=['BFO']
)

# %% 
# Define start and endtimes as well as length of the segments
time0 = UTCDateTime(2011, 3, 11, 0,0,0)
time1 = UTCDateTime(2011, 3, 15, 0,0,0)
dt = 12*3600 # seconds in a day
overlap = 0.0025 # fraction in overlap between traces

# %% 
download_data(download_dict, time0, time1, dt, dry=False, overlap=overlap,
              outdir=datadir)


# %% 
# Read in the data
st = read(os.path.join(waveformdir, "*.mseed"))
inv = read_inventory(os.path.join(stationdir, "*.xml"))
stbu = st.copy()

# %%
# Merge traces
st.merge()

# %%
# Quick processing
st.attach_response(inv)
pre_filt = [0.0005, 0.001, 0.003, 0.001]
st.remove_response(inv, output='VEL', water_level=60, pre_filt=pre_filt)

# %%
sampling_rate = 0.
st.filter("bandpass", freqmin=pre_filt[1], freqmax=pre_filt[2])
st.resample(sampling_rate, window='hanning')

# %%
# Plot the third trace
st[0].plot()

# Plot specttrogram of third trace
st[1].spectrogram()