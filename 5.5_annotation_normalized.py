from snapgene_reader import snapgene_file_to_dict
import pandas as pd

country=open("country.txt").readline().strip()
dictionary = snapgene_file_to_dict('annotation.dna')
CDS = [k for k in dictionary["features"] if k['type'] == "CDS"]
mat_peptide = [k for k in dictionary["features"] if k['type'] == "mat_peptide"]
genes = [k for k in dictionary["features"] if k['type'] == "gene"]

pos_dict = {}

for peptide in mat_peptide[:-1]:#petaei to teleftaio poy einai tou ORF1 mikro kommati
  pos_dict[peptide['qualifiers']['product']] = [peptide['start'],peptide['end']]

for gene in genes[1:]:
  pos_dict[gene['qualifiers']['gene']] = [gene['start'],gene['end']]

data = pd.read_csv(f"{country}/heatmap/heatmap.csv", index_col=0)

for name in pos_dict.keys():
    length = pos_dict[name][1] - pos_dict[name][0]
    data.loc[name] = data.loc[name]/length

data.to_csv(f"{country}/heatmap_norm.csv")