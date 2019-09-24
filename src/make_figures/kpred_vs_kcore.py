import sys
import os
import pandas as pd
import matplotlib.pyplot as plt

# my module
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, '../'))
import timor_coates as ktim


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
    # ax.set_ylim([0.000001, 1000000])
    ax.legend()
    plt.show()


if __name__ == "__main__":
    # ---------inputs-------------------

    input_folderpath = r"D:\PPRT関係\data"
    input_filename = "Calliance1.csv"

    # output_file = r"D:\PPRT関係\result\Caliance1_ktim.csv"

    # ---------------------------------

    # csvファイル読み込み
    input_file = os.path.join(input_folderpath, input_filename)
    Calliance1_nmr_df = pd.read_csv(input_file)

    # c_coatesを変えると、プロット上ではどんな変化をするのか（平行移動？）確認.
    # confirm_c_coates(Calliance1_nmr_df)

    # cut_coatesをしていしたverと指定しないverでそれぞれcperm vs ktimのプロットを作成し、どの程度それっぽさがアップするかを確認
    # グラフをみてじぶんで定義したcut_coates
    the_cut_coates_dict = {"Calliance1_22": 15,
                           "Calliance1_24": 20,
                           "Calliance1_28": 26
                           }

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    Calliance1_nmr_result_df_dict = {}
    # default cut_coates
    Calliance1_nmr_result_df_dict["default_cut"] = ktim.main(Calliance1_nmr_df)
    # my defined cut coates
    Calliance1_nmr_result_df_dict["my_cut"] = ktim.main(Calliance1_nmr_df, cut_coates_dict=the_cut_coates_dict)

    for key, Calliance1_result_df in Calliance1_nmr_result_df_dict.items():
        print(key, Calliance1_result_df)

        x = Calliance1_result_df["ktim"]
        y = Calliance1_result_df["cperm"]

        ax.scatter(x, y, label=key)
        for i, row in Calliance1_result_df.iterrows():
            ax.annotate(row["ID"], (row["ktim"], row["cperm"]), size=8)

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim([0.000001, 1000000])
    # ax.set_ylim([0.000001, 1000000])
    ax.set_xlabel('perm_pred')
    ax.set_ylabel('perm_core')
    ax.legend()
    plt.show()

