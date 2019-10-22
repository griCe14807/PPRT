import os
import matplotlib.pyplot as plt
import pandas as pd


def core_nmr_T2dist(nmr_df, micp_df, common_id_list):
    """

    :param df: T2, Por, BVIPorがあるdf。複数サンプルが縦に共存することを前提としている（groupbyで回す）
    :return:
    """
    # T2 distributionのグラフ描画
    # 参考 (http://sinhrks.hatenablog.com/entry/2015/11/15/222543)
    fig, axes = plt.subplots(5, 4, figsize=(10, 8))
    plt.subplots_adjust(wspace=0.5, hspace=0.5)

    for ax, id in zip(axes.flatten(), common_id_list):
        # 共通したidを持つサンプルのデータを抽出
        nmr_group = nmr_df[nmr_df['ID']==id]
        micp_group = micp_df[micp_df['ID']==id]

        # x軸は対数目盛
        ax.set_xscale("log")
        # 横軸T2で、Sw= 100とirreducible conditionのPorを縦軸に重ねて描画
        ax.plot(nmr_group.T2, nmr_group.Por, linewidth = 0.8)
        ax.plot(micp_group["PTR"], micp_group["Por_micp"], linewidth=0.8)

        ax.set_ylim(0, 4)
        ax.set_ylabel("")
        ax.set_title(id, fontsize=8)

    ax.legend()
    plt.show()


if __name__ == "__main__":

    the_nmr_df = pd.read_csv(r"D:\tmp\calliance1_nmr.csv")
    the_micp_df = pd.read_csv(r"D:\tmp\calliance1_micp.csv")

    the_common_id_list = list(set(the_nmr_df["ID"].unique()) & set(the_micp_df["ID"].unique()))

    # グラフ描画
    core_nmr_T2dist(the_nmr_df, the_micp_df, the_common_id_list)
