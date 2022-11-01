import pandas as pd
import os
import numpy as np
from snapgene_reader import snapgene_file_to_dict

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

dictionary = snapgene_file_to_dict('annotation.dna')
CDS = [k for k in dictionary["features"] if k['type'] == "CDS"]
mat_peptide = [k for k in dictionary["features"] if k['type'] == "mat_peptide"]
genes = [k for k in dictionary["features"] if k['type'] == "gene"]

pos_dict = {}

for peptide in mat_peptide[:-1]:#petaei to teleftaio poy einai tou ORF1 mikro kommati
  pos_dict[peptide['qualifiers']['product']] = [peptide['start'],peptide['end']]

for gene in genes[1:]:
  pos_dict[gene['qualifiers']['gene']] = [gene['start'],gene['end']]

final_table = pd.DataFrame()

for label in pos_dict:
  pos = pos_dict[label]
  new_row = table.loc[pos[0]:pos[1]].mean()
  df = pd.DataFrame([new_row.rename(label)])
  final_table = pd.concat([final_table,df], axis = 0)

final_table.to_csv(f"{country}/correlation/annotation.csv")