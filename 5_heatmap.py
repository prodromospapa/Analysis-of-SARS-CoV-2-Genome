from snapgene_reader import snapgene_file_to_dict
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import datetime
import statistics
import warnings
import matplotlib.pyplot as plt

warnings.filterwarnings('ignore')#mutes pandas fragmentation warning

dictionary = snapgene_file_to_dict('annotation.dna')
mat_peptide = [k for k in dictionary["features"] if k['type'] == "mat_peptide"]
genes = [k for k in dictionary["features"] if k['type'] == "gene"]

pos_dict = {}

for peptide in mat_peptide[:-1]:
  pos_dict[peptide['qualifiers']['product']] = [peptide['start'],peptide['end']]

for gene in genes[1:]:
  pos_dict[gene['qualifiers']['gene']] = [gene['start'],gene['end']]

country=open("country.txt").readline().strip()
dates = os.listdir(f"{country}/p_tables")
dates = [datetime.datetime.strptime(ts, "%m_%d_%Y") for ts in dates]
dates.sort()
dates = [datetime.datetime.strftime(ts, "%m_%d_%Y") for ts in dates]

final_table = pd.DataFrame([[[] for i in range(len(dates))] for i in range(len(pos_dict.keys()))], index=pos_dict.keys(), columns=dates)

total = int(os.popen(f"find {country}/p_tables/*/*.csv | wc -l").read()) + len(pos_dict.keys()) + 1 + len(dates)
count = 0
os.system(f"mkdir -p {country}/heatmap")
samples=[]
for day in dates:
    csvs = os.listdir(f"{country}/p_tables/{day}")
    samples.append(len(os.listdir(f'{country}/vcf_ncbi/{day}')))
    for csv in csvs:
      count +=1
      table = pd.read_csv(f"{country}/p_tables/{day}/{csv}",index_col=0)
      table = table[table<=0.05].dropna(axis = 0, how = 'all')
      for label in pos_dict:
        pos = pos_dict[label]
        number_of_diff = len(table.loc[pos[0]:pos[1]])
        final_table.at[label,day].append(number_of_diff)
      print(f"{round((count/total)*100,2)}%",end="\r")
    

final_table = final_table.applymap(lambda x : statistics.mean(x))

#normalizing
for name in pos_dict.keys():
    length = pos_dict[name][1] - pos_dict[name][0]
    final_table.loc[name] = final_table.loc[name]/length
    count +=1
    print(f"{round((count/total)*100,2)}%",end="\r")

#final_table = final_table.applymap(lambda x : 1 - x)#converts differences to similarities
final_table.to_csv(f"{country}/heatmap/heatmap.csv")

#heatmap
plt.figure()
g = sns.heatmap(final_table)
g.set_yticklabels(g.get_yticklabels(), rotation=0)
g.set_title(country)
plt.tight_layout()

n_genes = len(final_table.index.tolist())
max_n_samples = max(samples)

samples = [(i*n_genes*0.5)/max_n_samples for i in samples]

plt.xticks(rotation=45)
plt.locator_params(axis='x', nbins=10)
plt.plot(dates,samples,alpha=0.5, label="NCBI")
plt.tight_layout()
plt.gca().invert_yaxis()

samples = pd.read_pickle(f'{country}/tables_gisaid/samples.pickle')

gisaid_dates = samples.columns.tolist()
gisaid_samples = samples.iloc[0].tolist()

#window list
#numbers bellow must be the same with those in fisher.py
first_date = 5 #if you want to start in a previous day add minus in front of the number
window_days_range = 7
gisaid_window_samples = []
for date in dates:
    count +=1
    date_formatted = datetime.datetime.strptime(date, "%m_%d_%Y")                
    first_date_formatted = date_formatted + datetime.timedelta(days=first_date)
    window = [datetime.datetime.strftime(first_date_formatted, "%m_%d_%Y")]
    window_samples = 0
    for n_day in range(0,window_days_range):
        day = datetime.datetime.strftime(first_date_formatted + datetime.timedelta(days=n_day), "%m_%d_%Y")
        if day in gisaid_dates:
            window_samples += gisaid_samples[gisaid_dates.index(day)]
    gisaid_window_samples.append(window_samples)
#window list

max_n_gisaid_samples = max(gisaid_window_samples)
gisaid_window_samples = [(i*n_genes*0.5)/max_n_gisaid_samples for i in gisaid_window_samples]
plt.plot(dates,gisaid_window_samples,alpha=0.5,color='green',label="GISAID")
plt.legend(["NCBI","GISAID"],bbox_to_anchor=(-0.1,0))

plt.savefig(f"{country}/heatmap/{country}.png",dpi=500)
count +=1
print(f"{round((count/total)*100,2)}%",end="\r")
print('all done')