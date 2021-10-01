# Download Data and stitch them

## Create conda environment from environment file

```bash
conda env create -f environments.yml
```

Then activate
```bash
conda activate pages_obspy
```


## Run script

```bash
python download_stations.py
```

Then mini processing sample.

```bash
python process_data.py
```


This should get you from 0 to Normal Mode spectrogram. I haven't played too much
with the processing, but I assume you have your own workflow.

Note the `st.merge()` in `download_stations.py`. This merges your downloaded 
traces.

