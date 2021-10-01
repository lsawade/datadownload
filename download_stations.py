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
# Date is the start of the Tohoku events
time0 = UTCDateTime(2011, 3, 11, 0,0,0)
time1 = UTCDateTime(2011, 3, 15, 0,0,0)
dt = 12*3600 # seconds in a half a day

# %% 
download_data(download_dict, time0, time1, dt, dry=False, outdir=datadir)

