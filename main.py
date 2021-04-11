import argparse
import os
import pandas as pd
import geopandas as gpd
import pickle
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap


def load_obj(name):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)


def load_shape(name):
    for root, dirs, files in os.walk(f"shapefiles/{name}"):
        for file in files:
            if file.endswith(".shp"):
                return gpd.read_file(os.path.join(root, file))


if __name__ == "__main__":
    # read in germany wide ew19 statistic
    # wahlinfos = load_obj("wahlinfos")
    # # clean file
    # ew19 = wahlinfos['EW_19_Kreise']
    # ew19.columns = ew19.loc[1].values
    # ew19 = ew19.iloc[4:]
    #
    # ew19_volt = ew19[["Nr", "Gebiet", "gehört zu", "Wahlberechtigte", "Wähler/-innen", "Ungültige", "Gültige", "Volt Deutschland"]]

    ew19_wbz = load_obj("ew19_wbz")

    # get only bs. for definitions, consult ew19_wbz_leitband.csv
    ew19_wb_bs = ew19_wbz.loc[(ew19_wbz['Land'] == 3) & (ew19_wbz['Regierungsbezirk'] == 1) & (ew19_wbz['Kreis'] == 1) & (ew19_wbz['Verbandsgemeinde'] == 0) & (ew19_wbz['Gemeinde'] == 0) & (ew19_wbz['Kennziffer Briefwahlzugeh�rigkeit'] == 0)]

    # load shapefile
    shape_bs = load_shape("braunschweig")
    shape_bs = shape_bs.rename(columns={'Wahlbez_Nr': 'Wahlbezirk'})

    # merge shapefile and data
    data = shape_bs.merge(ew19_wb_bs, on="Wahlbezirk")

    # calc size of the areas in km**2
    data["size"] = data['geometry'].to_crs({'proj': 'cea'}).area / 10**6

    # add data column
    #data["data"] = data["Volt"]
    #data["data"] = data["Wahlberechtigte (A)"]
    #data["data"] = data['SPD']
    #data["data"] = data["Volt"] / data["W�hler (B)"]
    #data["data"] = data["Volt"] / data['G�ltig']
    #data["data"] = data["Volt"] / data['Ung�ltig']
    #data["data"] = data["Volt"] / data['GR�NE']
    #data["data"] = data["Volt"] / data['PIRATEN']
    #data["data"] = data["Volt"] / data['DIE LINKE']
    #data["data"] = data["Volt"] / data['AfD']
    #data["data"] = data["Volt"] / data['SPD']

    data["data"] = data["Wahlberechtigte (A)"] / data['size']
    label = "Stimmen"
    title = 'Wahlberechtigte pro km²'

    # setting the colormap
    colors = [(0.8, 0.9, 0.8), (0.05, 0.5, 0.05)]  # grüne
    #colors = [(0.8, 0.7, 1), (0.36, 0.15, 0.55)]  # volt
    #cm = LinearSegmentedColormap.from_list('test', colors, N=10)
    cm = "magma_r"


    # https://geopandas.org/docs/user_guide/mapping.html
    fig, ax = plt.subplots(1, 1)
    fig.suptitle(title, fontsize=16)
    data.plot(column='data', cmap=cm, ax=ax, legend=True, legend_kwds={'label': label})
    plt.axis('off')
    plt.savefig(f"images/{title.replace(' ', '_')}.png", bbox_inches='tight')
    plt.show()
