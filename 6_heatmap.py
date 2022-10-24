import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

country=open("country.txt").readline().strip()
plt.figure()
data = pd.read_csv(f"{country}/heatmap_norm.csv", index_col=0)
g = sns.heatmap(data)
g.set_yticklabels(g.get_yticklabels(), rotation=0)
g.set_title("ountry")
plt.tight_layout()
plt.savefig(f"{country}/{country}.png")

#https://www.anycodings.com/1questions/3346679/color-scale-by-rows-in-seaborn-heatmap