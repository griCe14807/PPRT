import sys
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# my module
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, '../'))
import timor_coates as ktim
import calc_cutoff_BVI

def confirm_c_coates(Calliance1_nmr_df):
    """
    c_coatesを変えると、プロット上ではどんな変化をするのか（平行移動？）確認.
    :param Calliance1_nmr_df:
    :return:
    """

    c_coates_list = [0.1, 0.2, 0.4, 0.8]

    # predicted permeability vs core permeability
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    for c_coates_ in c_coates_list:
        Calliance1_result_df = ktim.main(Calliance1_nmr_df, c_coates=c_coates_)
        print(Calliance1_result_df)

        x = Calliance1_result_df["ktim"]
        y = Calliance1_result_df["cperm"]
        ax.scatter(x, y, label=c_coates_)
        for i, row in Calliance1_result_df.iterrows():
            ax.annotate(row["ID"], (row["ktim"], row["cperm"]), size=8)

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim([0.000001, 1000000])
    ax.set_ylim([0.000001, 1000000])
    ax.legend()
    plt.show()


if __name__ == "__main__":
    # ---------inputs-------------------

    input_folderpath = r"D:"
    input_filename_list = ["Calliance1.csv"]

    # output_file = r"D:\PPRT関係\result\Caliance1_ktim.csv"

    # ---------------------------------

    # csvファイル読み込み
    the_input_df = pd.concat(pd.read_csv(os.path.join(input_folderpath, input_filename)) for input_filename in input_filename_list)

    # cut_coatesを辞書型で取得
    the_cut_coates_dict = calc_cutoff_BVI.main(the_input_df)

    # c_coatesを変えると、プロット上ではどんな変化をするのか（平行移動？）確認.
    # confirm_c_coates(Calliance1_nmr_df)

    # cut_coatesをしていしたverと指定しないverでそれぞれcperm vs ktimのプロットを作成し、どの程度それっぽさがアップするかを確認

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    the_nmr_result_df_dict = {}
    # default cut_coates
    the_nmr_result_df_dict["default_cut"] = ktim.main(the_input_df)
    # my defined cut coates
    the_nmr_result_df_dict["my_cut"] = ktim.main(the_input_df, cut_coates_dict=the_cut_coates_dict)

    for key, the_result_df in the_nmr_result_df_dict.items():
        print(key, the_result_df)

        x = the_result_df["ktim"]
        y = the_result_df["cperm"]

        ax.scatter(x, y, label=key)
        for i, row in the_result_df.iterrows():
            ax.annotate(row["ID"], (row["ktim"], row["cperm"]), size=8)

    # 描画範囲の指定
    pict_range = [0.001, 100000]
    # 参考にx=yのラインを追加。
    x = np.arange(pict_range[0], pict_range[1])
    y = x
    ax.plot(x, y)

    # 軸の設定など
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(pict_range)
    ax.set_ylim(pict_range)
    ax.set_xlabel('perm_pred')
    ax.set_ylabel('perm_core')
    ax.legend()
    plt.show()