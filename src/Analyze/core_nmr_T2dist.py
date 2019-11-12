import os
import matplotlib.pyplot as plt
import pandas as pd

def core_nmr_T2dist(df):
    """

    :param df: T2, Por, BVIPorがあるdf。複数サンプルが縦に共存することを前提としている（groupbyで回す）
    :return:
    """
    # T2 distributionのグラフ描画
    # 参考 (http://sinhrks.hatenablog.com/entry/2015/11/15/222543)
    fig, axes = plt.subplots(5, 4, figsize=(10, 8))
    plt.subplots_adjust(wspace=0.5, hspace=0.5)

    for ax, (key, group) in zip(axes.flatten(), df.groupby("ID")):

        # x軸は対数目盛
        ax.set_xscale("log")
        # 横軸T2で、Sw= 100とirreducible conditionのPorを縦軸に重ねて描画
        ax.plot(group["T2"], group["Por"], linewidth = 0.8)
        ax.plot(group["T2"], group["BVI_Por"], linewidth = 0.8)

        # cumulative porosityも描画
        ax2 = ax.twinx()
        ax2.plot(group["T2"], group["Por_cum"], linestyle='dashed', linewidth = 0.8)
        ax2.plot(group["T2"], group["BVI_Por_cum"], linestyle='dashed', linewidth = 0.8)

        ax.set_ylim(0, 4)
        ax2.set_ylim(0, 25)
        ax.set_ylabel("")
        ax.set_title(key, fontsize=8)

    plt.show()


if __name__ == "__main__":

    # ---------inputs-------------------

    input_folderpath = r"D:"
    input_filename = "Calliance1.csv"

    # ---------------------------------

    input_file = os.path.join(input_folderpath, input_filename)
    Calliance1_nmr_df = pd.read_csv(input_file)

    print(Calliance1_nmr_df["ID"].unique())

    # T2 distributionのグラフ描画
    core_nmr_T2dist(Calliance1_nmr_df)
