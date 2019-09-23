import sys
import os
import pandas as pd

# my module
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, '../'))
import timor_coates as ktim

if __name__ == "__main__":
    # ---------inputs-------------------

    input_folderpath = r"D:\PPRT関係\data"
    input_filename = "Calliance1.csv"

    # output_file = r"D:\PPRT関係\result\Caliance1_ktim.csv"

    # ---------------------------------

    # csvファイル読み込み
    input_file = os.path.join(input_folderpath, input_filename)
    Calliance1_nmr_df = pd.read_csv(input_file)

    # グラフをみてじぶんで定義したcut_coates
    cut_coates_dict = {"Calliance1_22": 15,
                       "Calliance1_24": 20,
                       "Calliance1_28": 26
                       }

    ktim_result_df = ktim.main(Calliance1_nmr_df)

    # TODO: cut_coatesをしていしたverと指定しないverでそれぞれcperm vs ktimのプロットを作成し、どの程度それっぽさがアップするかを確認
    # TODO: c_coatesを変えると、プロット上ではどんな変化をするのか（平行移動？）確認。