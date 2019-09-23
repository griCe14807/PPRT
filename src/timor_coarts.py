import os
import pandas as pd
import numpy as np
from scipy import interpolate


def k_timor_coates(df, cut_coates=None, c_coates=0.1, phit=None):
    """
    T2 distributionからtimor coats permeabilityを計算。
    :param df: T2 distributionのdf. "T2" columnと"Por" columnは必須。"BVI_Por" columnもあったほうがいい。
    :param cut_coates: T2のカットオフ値. これ以下のT2はBVIとして扱う
    :param c_coates: 地層に依存して決まる定数
    :param por: den-neu phitなど、使いたい孔隙率があればinput. なければNMR phitを用いる
    :return:
    """
    # defaultで値を入れるのではなくこうすることで、一部のデータだけphitを指定することができる。
    if phit == None:
        t2cum = np.cumsum(df.Por) / 100
        phit = t2cum.iloc[-1]

    if cut_coates == None:
        cut_coates = 33

    # cut_coatesの時のt2cumの値。（T2-t2cumの関係を、スプライン補完でインターポレートして算出）
    bvi = float(interpolate.interp1d(df.T2, t2cum, kind="cubic")(cut_coates))
    ffi = max(0, phit - bvi)
    ktim = (phit / c_coates) ** 4 * (ffi / bvi) ** 2

    return ktim


def main(df, cut_coates_dict={}):
    output_dict = {"ID": [], "ktim": [], "cperm": []}
    for key, group in df.groupby("ID"):
        ktim = k_timor_coates(group, cut_coates=cut_coates_dict.get(key))
        output_dict["ID"].append(key)
        output_dict["ktim"].append(ktim)
        output_dict["cperm"].append(group.cperm.iloc[1])

        print("{0}のcperm={1}, ktim={2}".format(key, group.cperm.iloc[1], ktim))

    output_df = pd.DataFrame(output_dict)
    # print(output_df)

    return output_df


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

    ktim_result_df = main(Calliance1_nmr_df)