import pandas as pd
import os, os.path
import datetime 
import numpy as np
import warnings
import sys

warnings.filterwarnings('ignore')#mutes pandas fragmentation warning

def validate(date_text):
        try:
            datetime.datetime.strptime(date_text, '%Y-%m-%d')
            return True
        except ValueError:
            return False


def create_table(table):
    column = dataframe[name].tolist()
    for index in range(len(column)):
        base_pos = pos_list[index]
        if column[index]-1 >= 0:
            base = alt_list[index].replace(",","")[column[index]-1]
            if base in ["A","G","C","T"]:
                table.at[base_pos,base] += 1
        else:
            base = ref[index]
            table.at[base_pos,base] += 1
    table.to_pickle(f"{country}/tables_gisaid/{date}.pickle")
    
def samples_per_day(date,sample_n):#function to count number of samples each day
    if os.path.exists(f"{country}/tables_gisaid/samples_{sample_n}.pickle"):
        dates_table = pd.read_pickle(f"{country}/tables_gisaid/samples_{sample_n}.pickle")
        if date in dates_table:
            dates_table[date] += 1
        else:
            dates_table[date] = 1
        dates_table.to_pickle(f"{country}/tables_gisaid/samples_{sample_n}.pickle")
    else:
       dates_table = pd.DataFrame(1, index=["n_samples"], columns=[date])
       dates_table.to_pickle(f"{country}/tables_gisaid/samples_{sample_n}.pickle")


with open("refseq/EPI_ISL_402124.fasta") as f:
    f.readline()
    ref = f.readline().strip()

vcfs = sys.argv[1:-1]
sample_n = int(sys.argv[-1])
total=len(vcfs)*30000
country=open("country.txt").readline().strip()

if len(vcfs) >= 0:
    n_vcf=0
    for vcf in vcfs:
        n_vcf+=1
        with open(vcf) as f:
            for i in range(3):
                f.readline()
            header = f.readline().replace("\n","")
        header = header.replace("#","").split("\t")

        dataframe = pd.read_csv(vcf,comment='#',sep="\t",header=None,names=header)

        alt_list = dataframe["ALT"].tolist()
        pos_list = dataframe["POS"].tolist()
        names = header[10:]
        dataframe = dataframe.iloc[:,10:]
        os.system(f"mkdir -p {country}/tables_gisaid")
        for name in names:
            date = name.split("|")[2]
            if validate(date):
                date = datetime.datetime.strptime(date, '%Y-%m-%d').strftime("%m_%d_%Y") #matches ncbi day format
                samples_per_day(date,sample_n)
                while True:
                    try:
                        if os.path.exists(f"{country}/tables_gisaid/{date}.pickle"):
                            table = pd.read_pickle(f"{country}/tables_gisaid/{date}.pickle")
                            create_table(table) 
                        else:
                            table = pd.DataFrame(0, np.arange(1,29904), columns=["A","G","C","T"])
                            create_table(table)
                    except Exception:
                        continue
                    break
            os.system(f"echo {n_vcf} > tables_progress_{sample_n}.txt")