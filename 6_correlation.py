import pandas as pd
import datetime
import os
import numpy as np

country=open("country.txt").readline().strip()
os.system(f"mkdir -p {country}/correlation")

dates_table = pd.read_pickle(f"{country}/tables_gisaid/samples.pickle")
dates = dates_table.columns.values.tolist()
ref = open('refseq/NC_045512.fasta')
ref.readline()
ref = ref.read().replace('\n','')
table = pd.DataFrame(0, index=np.arange(1,29904), columns=["to_remove"])
total = len(dates)
counter = 0
for day in dates:
    pickle = pd.read_pickle(f"{country}/tables_gisaid/{day}.pickle")
    for i in range(len(ref)):
        pickle.iloc[i][ref[i]] = 0
    pickle = pickle.sum(axis=1).rename(day)
    table = pd.concat([table,pickle],axis=1)#enwnei oles tis hmeromhnies se mia
    counter+=1
    print(f"{round(counter*100/total,2)}%",end="\r")
table = table.iloc[: , 1:].div(dates_table.iloc[0].tolist())#vgazei thn to_remove kai kanei normalizing

table.to_csv(f"{country}/correlation/total_variant.csv")