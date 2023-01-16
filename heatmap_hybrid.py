import pandas as pd
import os
import datetime
import matplotlib.pyplot as plt
import seaborn as sns

country=open("country.txt").readline().strip()
final_table = pd.read_csv(f"{country}/heatmap/heatmap.csv",index_col=[0])

#heatmap
plt.figure()
g = sns.heatmap(final_table)
g.set_yticklabels(g.get_yticklabels(), rotation=0)
g.set_title(country)
plt.tight_layout()

dates = os.listdir(f'{country}/vcf_ncbi')
dates = [datetime.datetime.strptime(ts, "%m_%d_%Y") for ts in dates]
dates.sort()
dates = [datetime.datetime.strftime(ts, "%m_%d_%Y") for ts in dates]
samples=[]
for day in dates:
    samples.append(len(os.listdir(f'{country}/vcf_ncbi/{day}')))

n_genes = len(final_table.index.tolist())
max_n_samples = max(samples)

samples = [(i*n_genes*0.5)/max_n_samples for i in samples]

plt.xticks(rotation=45)
plt.locator_params(axis='x', nbins=10)
plt.plot(dates,samples,alpha=0.5, label="NCBI")
plt.tight_layout()
plt.gca().invert_yaxis()

samples = pd.read_pickle(f'{country}/tables_gisaid/samples.pickle')
idx = pd.to_datetime(samples.columns, errors='coerce', format='%m_%d_%Y').argsort()#afto bgale to meta
samples = samples.iloc[:, idx]#afto bgale to meta
#ftiaxe to samples na einai sorted

gisaid_dates = samples.columns.tolist()
gisaid_samples = samples.iloc[0].tolist()

#window list
first_date = 5 #if you want to start in a previous day add minus in front of the number
window_days_range = 7
gisaid_window_samples = []
gisaid_dates = os.listdir(f'{country}/tables_gisaid')
gisaid_dates = [i.replace(".pickle","") for i in gisaid_dates]
for date in dates:
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
plt.savefig(f"{country}/{country}_samples.png")
