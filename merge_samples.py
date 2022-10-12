import sys
import pandas as pd
samples_files_n = range(1,int(sys.argv[1])+1)
country=open("country.txt").readline().strip()

dates = []
for sample_n in samples_files_n:
    dates += pd.read_pickle(f"{country}/tables_gisaid/samples_{sample_n}.pickle").columns.tolist()

dates = set(dates)
samples = pd.DataFrame(0, index=['n_samples'], columns=dates)
for sample_n in samples_files_n:
    table = pd.read_pickle(f"{country}/tables_gisaid/samples_{sample_n}.pickle")
    samples[table.columns.tolist()] = samples[table.columns.tolist()].add(table)

samples.to_pickle(f"{country}/tables_gisaid/samples.pickle")