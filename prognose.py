import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

from main import load_shape


prognosedaten = pd.read_excel("bs_prognose.xlsx", sheet_name="Tabelle1")

shape_bs = load_shape("braunschweig")
shape_bs = shape_bs.rename(columns={'Wahlbez_Nr': 'UWB'})
shape_bs["UWB"] = shape_bs["UWB"].astype(int)

data = shape_bs.merge(prognosedaten, on="UWB")

data["data"] = data["prediction"]
label = "p = "
title = 'Vorausage von Volt'

colors = [(0.8, 0.7, 1), (0.36, 0.15, 0.55)]
cm = LinearSegmentedColormap.from_list('test', colors, N=10)

fig, ax = plt.subplots(1, 1)
fig.suptitle(title, fontsize=16)
data.plot(column='data', cmap=cm, ax=ax, legend=True, legend_kwds={'label': label})
plt.axis('off')
plt.savefig(f"images/{title.replace(' ', '_')}.png", bbox_inches='tight')
plt.show(bbox_inches='tight')
