import os
import pandas as pd
import numpy as np

def calc_t2_cumulative(df):
    """
    csvにcumulative porosity行と、cumulative BVI行を追記
    :param df:
    :return:
    """
    group_list = []
    for key, group in df.groupby("ID"):
        group["Por_cum"] = np.cumsum(group.Por)
        group["BVI_Por_cum"] = np.cumsum(group.BVI_Por)

        group_list.append(group)

    output_df = pd.concat(group_list)

    return output_df


if __name__ == "__main__":


    # ---------inputs-------------------

    input_folderpath = r"D:\tmp"
    input_filename = "calliance1_nmr.csv"

    # ---------------------------------

    input_file = os.path.join(input_folderpath, input_filename)
    the_df = pd.read_csv(input_file)

    the_new_df = calc_t2_cumulative(the_df)
    the_new_df.to_csv(os.path.join(input_folderpath, input_filename), index=False)