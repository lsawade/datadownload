# Download seismic data and stitch them together

## Create conda environment from environment file

If you don't have obspy installed,

```bash
conda env create -f environment.yml
```
then activate
```bash
conda activate obspyenv
```

Otherwise, skip this step.

## Run scripts

This downloads data for a couple of stationns in 12 hour chunks

```bash
python download_stations.py
```

This computes a normal mode spectrogram for one of the stations.

```bash
python process_data.py
```

This should get you from 0 to normal mode spectrogram at a seismic statiton. 
I haven't played too much with the processing, so something is not quite 
right in the final spectrogram, but I assume you have your own workflow, so I'm
not going to dig...

Note the `st.merge()` in `download_stations.py`. This merges your downloaded 
traces. 

At any point during the processing you can write your stream to a file using 
``st.write(<filename>, format=<yourfavoriteformat>)
See this: https://docs.obspy.org/packages/autogen/obspy.core.stream.Stream.write.html#obspy.core.stream.Stream.write
