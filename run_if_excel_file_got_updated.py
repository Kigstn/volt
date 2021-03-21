import pandas as pd
import pickle


def save_obj(obj, name):
    with open('obj/' + name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


# update the dataframe which holds the excel infos. Could skip this, but loading excel files takes like 30s
wahlinfos = pd.read_csv("ew19_wbz_ergebnisse.csv", skiprows=4, delimiter=";")
save_obj(wahlinfos, "ew19_wbz")

wahlinfos = pd.read_excel("wahlinfos.xlsx", sheet_name=None)
save_obj(wahlinfos, "wahlinfos")


