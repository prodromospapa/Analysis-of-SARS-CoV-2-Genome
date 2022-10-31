import os
import pandas as pd

country=open("country.txt").readline().strip()
samples_files_n=[filename for filename in os.listdir(f'{country}/tables_gisaid') if filename.startswith("samples_")]

dates = []
for sample_n in samples_files_n:
    dates += pd.read_pickle(f"{country}/tables_gisaid/{sample_n}").columns.tolist()

dates = list(set(dates))
samples = pd.DataFrame(0, index=['n_samples'], columns=dates)
for sample_n in samples_files_n:
    table = pd.read_pickle(f"{country}/tables_gisaid/{sample_n}")
    samples[table.columns.tolist()] = samples[table.columns.tolist()].add(table)

idx = pd.to_datetime(samples.columns, errors='coerce', format='%m_%d_%Y').argsort()
samples = samples.iloc[:, idx]
samples.to_pickle(f"{country}/tables_gisaid/samples.pickle")