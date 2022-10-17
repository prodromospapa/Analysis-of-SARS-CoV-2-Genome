from scipy.stats import fisher_exact
import os
import pandas as pd
import numpy as np
import datetime
from statsmodels.stats.multitest import fdrcorrection
import sys

#file format month_day_year

country=open("country.txt").readline().strip()
sra_txt = sys.argv[1]
number = sys.argv[2]
os.system(f"mkdir -p {country}/p_tables")
sra_list = open(sra_txt)
vcf_list = os.popen(f"find {country}/vcf_ncbi/*/*.vcf").read().split("\n")[:-1]
vcf_list = [i.split("/")[-1].strip('.vcf') for i in vcf_list ]
counter=0

for sample in sra_list.read().split("\n")[:-1]:
    if sample in vcf_list:
        counter+=1
        os.system(f"echo {counter} > fisher_progress_{number}.txt")
        date = os.popen(f"find {country}/vcf_ncbi/*/{sample.strip()}.vcf").read().split("/")[2]
        os.system(f"mkdir -p {country}/p_tables/{date}")
        if f"{sample.strip()}.csv" not in os.listdir(f"{country}/p_tables/{date}"):
            try:
                dataframe = pd.read_csv(f"{country}/vcf_ncbi/{date}/{sample.strip()}.vcf",comment='#',sep="\t",header=None) 
                #window list
                date_formated = datetime.datetime.strptime(date, "%m_%d_%Y")
                first_date = date_formated - datetime.timedelta(days=3)
                window = [datetime.datetime.strftime(first_date, "%m_%d_%Y")]
                for i in range(1,7):
                    window.append(datetime.datetime.strftime(first_date + datetime.timedelta(days=i), "%m_%d_%Y"))
                #window list

                gisaid = pd.DataFrame(0, np.arange(1,29904), columns=['A','G','C','T'])
                n_samples_gisaid = 0
                for day in window:
                    try:
                        table = pd.read_pickle(f"{country}/tables_gisaid/{day}.pickle")
                        n_samples_gisaid += int(pd.read_pickle(f"{country}/tables_gisaid/samples.pickle")[day])
                        gisaid += table
                    except Exception:#if day doesn't exist
                        continue
                pos_list = dataframe[1].tolist()
                alt_list = dataframe[4].tolist()
                depth_list = dataframe[9].tolist()
                ncbi = pd.DataFrame(0, np.arange(1,29904), columns=['A','G','C','T'])
                for index in range(len(alt_list)):
                        pos = pos_list[index]
                        alt = alt_list[index].split(',')
                        depth = depth_list[index].split(":")[1].split(",")
                        for alt_single in alt:
                            if alt_single in ["A", "G", "C", "T"]:
                                ncbi.at[pos,alt_single] += int(depth[alt.index(alt_single) + 1])

                N = n_samples_gisaid
                fisher_list = []
                for pos in range(1,29904):
                    n = ncbi.loc[pos].sum()
                    for base in ['A','G','C','T']:
                        A = int(gisaid.loc[pos][base])
                        x = int(ncbi.loc[pos][base])
                        value_fisher,pvalue = fisher_exact([[x,n-x],[A,N-A]])#N = pos_gisaid_total, A = pos_gisaid_base, n = pos_ncbi_total, x = pos_ncbi_base
                        fisher_list.append(pvalue)
                p_adjusted = fdrcorrection(fisher_list)[1]#p-value correction
                fisher_table = pd.DataFrame({'A':p_adjusted[0:29903],'G':p_adjusted[29903:2*29903],'C':p_adjusted[2*29903:3*29903],'T':p_adjusted[3*29903:4*29903]},index=np.arange(1,29904))
                fisher_table.to_csv(f"{country}/p_tables/{date}/{sample.strip()}.csv")
            except Exception:
                continue
sra_list.close()