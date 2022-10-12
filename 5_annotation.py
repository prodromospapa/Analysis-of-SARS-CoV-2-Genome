#https://github.com/Edinburgh-Genome-Foundry/SnapGeneReader
#https://www.snapgene.com/resources/coronavirus-resources/?resource=SARS-CoV-2_(COVID-19)_Genome

from snapgene_reader import snapgene_file_to_dict, snapgene_file_to_seqrecord
import pandas as pd
import os
import datetime
import statistics
import warnings

warnings.filterwarnings('ignore')#mutes pandas fragmentation warning

dictionary = snapgene_file_to_dict('annotation.dna')
CDS = [k for k in dictionary["features"] if k['type'] == "CDS"]
mat_peptide = [k for k in dictionary["features"] if k['type'] == "mat_peptide"]
genes = [k for k in dictionary["features"] if k['type'] == "gene"]

pos_dict = {}

for peptide in mat_peptide[:-1]:
  pos_dict[peptide['qualifiers']['product']] = [peptide['start'],peptide['end']]

for gene in genes[1:]:
  pos_dict[gene['qualifiers']['gene']] = [gene['start'],gene['end']]


country=open("country.txt").readline().strip()

dates = os.listdir("p_tables")
dates = [datetime.datetime.strptime(ts, "%m_%d_%Y") for ts in dates]
dates.sort()
dates = [datetime.datetime.strftime(ts, "%m_%d_%Y") for ts in dates]

final_table = pd.DataFrame([[[] for i in range(len(dates))] for i in range(len(pos_dict.keys()))], index=pos_dict.keys(), columns=dates)

total = int(os.popen(f"find {country}/p_tables/*/*.csv | wc -l").read())
count = 0
os.system(f"mkdir -p {country}/heatmap")
for day in dates:
    vcfs = os.listdir(f"{country}/p_tables/{day}")
    for vcf in vcfs:
      count +=1
      table = pd.read_csv(f"{country}/p_tables/{day}/{vcf}",index_col=0)
      table = table[table<=0.05].dropna(axis = 0, how = 'all')
      for label in pos_dict:
        pos = pos_dict[label]
        number_of_diff = len(table.loc[pos[0]:pos[1]])
        final_table.at[label,day].append(number_of_diff)
      print(f"{round(count/total,2)}%",end="\r")
    

final_table = final_table.applymap(lambda x : statistics.mean(x))
  
final_table.to_csv(f"{country}/heatmap/heatmap.csv")