from scipy import interpolate
import os
import pandas as pd
import matplotlib.pyplot as plt

def calc_t2_cutoff(df):
    """
    groupbyで単一sampleについてのデータにしてからinputする必要ある。
    :param df:
    :return:
    """
    # xの増分が0だとうまくinterpolateできないため、微小量増加を入れる
    cum_por = []
    for i, cum_por_ in enumerate(df.Por_cum):
        cum_por_ = cum_por_ + 0.00001 * i
        cum_por.append(cum_por_)

    # cutoff値を計算
    t2_cutoff = float(interpolate.interp1d(cum_por, df.T2, kind="linear")(df.BVI_Por_cum.iloc[-1]))

    return t2_cutoff

def main(df):
    """
    複数sampleが含まれるdf
    :param df:
    :return:
    """
    cut_coates_dict = {}

    for key, group in df.groupby("ID"):
        the_t2_cutoff = calc_t2_cutoff(group)
        print(key, the_t2_cutoff)
        if the_t2_cutoff < 0 or the_t2_cutoff > 200:
            cut_coates_dict[key] = 0
        else:
            cut_coates_dict[key] = the_t2_cutoff

    return cut_coates_dict

if __name__ == "__main__":


    # ---------inputs-------------------

    input_folderpath = r"D:"
    input_filename = "Calliance1.csv"

    # ---------------------------------

    input_file = os.path.join(input_folderpath, input_filename)
    the_df = pd.read_csv(input_file)

    the_cut_coates_dict = main(the_df)