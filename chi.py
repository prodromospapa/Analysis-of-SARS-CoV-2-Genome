import os
import pandas as pd
import numpy as np
import datetime
from statsmodels.stats.multitest import fdrcorrection
import sys
from scipy.stats import chi2_contingency

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
        os.system(f"echo {counter} > chi_progress_{number}.txt")
        date = os.popen(f"find {country}/vcf_ncbi/*/{sample.strip()}.vcf").read().split("/")[2]
        os.system(f"mkdir -p {country}/p_tables/{date}")
        if f"{sample.strip()}.csv" not in os.listdir(f"{country}/p_tables/{date}"):
            try:
                dataframe = pd.read_csv(f"{country}/vcf_ncbi/{date}/{sample.strip()}.vcf",comment='#',sep="\t",header=None) 
                #window list
                first_date = 5 #if you want to start in a previous day add minus in front of the number
                window_days_range = 7
                date_formatted = datetime.datetime.strptime(date, "%m_%d_%Y")                
                first_date_formatted = date_formatted + datetime.timedelta(days=first_date)
                window = [datetime.datetime.strftime(first_date_formatted, "%m_%d_%Y")]
                for day in range(1,window_days_range):
                    window.append(datetime.datetime.strftime(first_date_formatted + datetime.timedelta(days=day), "%m_%d_%Y"))
                #window list
                gisaid = pd.DataFrame(0, np.arange(1,29904), columns=['A','G','C','T'])
                for day in window:
                    try:
                        table = pd.read_pickle(f"{country}/tables_gisaid/{day}.pickle")
                        gisaid += table
                    except Exception:#if day doesn't exist
                        continue
                gisaid = gisaid.replace(0,10**(-100))

                pos_list = dataframe[1].tolist()
                ref_list = dataframe[3].tolist()
                alt_list = dataframe[4].tolist()
                depth_list = dataframe[9].tolist()
                ncbi = pd.DataFrame(0, np.arange(1,29904), columns=['A','G','C','T'])
                for index in range(len(alt_list)):
                        pos = pos_list[index]
                        ref_single = ref_list[index]
                        alt = alt_list[index].split(',')
                        depth = depth_list[index].split(":")[1].split(",")
                        for alt_single in alt:
                            if alt_single in ["A", "G", "C", "T"]:
                                ncbi.at[pos,alt_single] += int(depth[alt.index(alt_single) + 1])
                        ncbi.at[pos,ref_single] += int(depth[0])
                ncbi = ncbi.replace(0,10**(-100))

                p_values = []
                for pos in range(1,29904):
                    p_values.append(chi2_contingency([ncbi.loc[pos].tolist(),gisaid.loc[pos].tolist()])[1])

                p_adjusted = fdrcorrection(p_values)[1]#p-value correction
                chi_table = pd.DataFrame({'p-values':p_adjusted},index=np.arange(1,29904))
                chi_table.to_csv(f"{country}/p_tables/{date}/{sample.strip()}.csv")
            except Exception:
                continue
sra_list.close()