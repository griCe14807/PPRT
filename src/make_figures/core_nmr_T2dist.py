import os
import matplotlib.pyplot as plt
import pandas as pd

def core_nmr_T2dist(df):
    """

    :param df: T2, Por, BVIPorがあるdf
    :return:
    """
    # T2 distributionのグラフ描画
    # 参考 (http://sinhrks.hatenablog.com/entry/2015/11/15/222543)
    fig, axes = plt.subplots(4, 3, figsize=(8, 6))
    plt.subplots_adjust(wspace=0.5, hspace=0.5)

    for ax, (key, group) in zip(axes.flatten(), df.groupby("ID")):

        # x軸は対数目盛
        ax.set_xscale("log")
        # 横軸T2で、Sw= 100とirreducible conditionのPorを縦軸に重ねて描画
        ax.plot(group["T2"], group["Por"])
        ax.plot(group["T2"], group["BVI_Por"])
        ax.set_ylabel("")
        ax.set_title(key, fontsize=8)

    plt.show()


if __name__ == "__main__":

    # ---------inputs-------------------

    input_folderpath = r"D:\PPRT関係\data"
    input_filename = "Calliance1.csv"

    # ---------------------------------

    input_file = os.path.join(input_folderpath, input_filename)
    Calliance1_nmr_df = pd.read_csv(input_file)

    # T2 distributionのグラフ描画
    core_nmr_T2dist(Calliance1_nmr_df)
