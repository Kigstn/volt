import argparse
import os
import pandas as pd
import geopandas as gpd
import pickle
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

from main import load_shape


strukturdaten = pd.read_excel("bs_strukturdaten.xlsx", sheet_name="Sheet1")
shape = load_shape("braunschweig_struktur")
shape["StatistBez"] = shape["StatistBez"].astype(int)

data = shape.merge(strukturdaten, on="StatistBez")


data["data"] = data["ab 65"]
label = "Menschen"
title = 'ab 65'

# setting the colormap
# colors = [(0.8, 0.9, 0.8), (0.05, 0.5, 0.05)]  # grüne
# colors = [(0.8, 0.7, 1), (0.36, 0.15, 0.55)]  # volt
# cm = LinearSegmentedColormap.from_list('test', colors, N=10)
cm = "magma_r"


fig, ax = plt.subplots(1, 1)
fig.suptitle(title, fontsize=16)
data.plot(column='data', cmap=cm, ax=ax, legend=True, legend_kwds={'label': label})
plt.axis('off')
plt.savefig(f"images/{title.replace(' ', '_')}.png", bbox_inches='tight')
plt.show(bbox_inches='tight')
