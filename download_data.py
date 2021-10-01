import os
from typing import Union, Tuple
from obspy import UTCDateTime, Stream, Inventory
from obspy.clients.fdsn.mass_downloader import RectangularDomain,\
     Restrictions, MassDownloader
from obspy.clients.fdsn import Client
import numpy as np
from time import time

def download_data(
    stationdict: dict, 
    start: UTCDateTime,
    end: UTCDateTime, 
    segment: float,
    channel: str = "BH*",
    location: str = "00",
    dry: bool = False,
    outdir: str = "."):
    """Downloads data in bulk and writes them to waveform and station directory.

    Parameters
    ----------
    stationdict : dict
        dictionary providing the networks stations etc.
    start : UTCDatetime
        starttime download
    end : UTCDatetime
        endtime download
    segment : float
        segment length in seconds
    channel : str, optional
        channel, by default "00"
    location : str, optional
        location, by default "00"
    """

    # Create bulk request for an inventory
    bulk = list()
    for network, stations in stationdict.items():
        for station in stations:
            bulk.append(
                    (network, station, location, channel, start, end))
    
    if dry:
        for row in bulk:
            print(row)
        return

    # Create communicator
    client = Client("IRIS")

    # Get stations
    print('Downloading the stations ...')
    t0 = time()
    inv = client.get_stations_bulk(bulk)
    t1 = time()
    print(f'done after {t1-t0:.2f} s.')


    # Domain
    # Note that the domain encloses the entire world.
    # The domain is a required input, but since we know which stations,
    # we can restrict the download using the inventory we fetched. 
    domain = RectangularDomain(minlatitude=-90, maxlatitude=90,
                           minlongitude=-180, maxlongitude=180)

    # Restrictions
    restrictions = Restrictions(
        # Start and end times
        starttime=start,
        endtime=end,
        # Defines the chunklength of each trace
        chunklength_in_sec=segment,
        channel=channel,
        location=location,
        # This restricts the download to the given stations
        limit_stations_to_inventory=inv)

    # The mass downloader enables parallel download.
    print('Downloading the waveforms ...')
    t0 = time()
    mdl = MassDownloader(providers=["IRIS"])
    mdl.download(domain, restrictions, 
                 mseed_storage=os.path.join(outdir, "waveforms"),
                 stationxml_storage=os.path.join(outdir, "stations"))
    t1 = time()
    print(f'done after {t1-t0:.2f} s.')



