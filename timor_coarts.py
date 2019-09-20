import os
import pandas as pd
import matplotlib as plt


# ---------inputs-------------------

input_folderpath = r"C:\Users\02217013\Documents\201907-_DOMEE\PPRT勉強会\02_Data\nmr"
input_filename = "Calliance1.csv"

# ---------------------------------

input_file = os.path.join(input_folderpath, input_filename)
Calliance1_nmr_df = pd.read_csv(input_file)
print(Calliance1_nmr_df.head)




# T2 distributionの表示
# fig = plt.figure()
# ax = fig.add_subplot(111)

# ax.plot(Calliance1_nmr_df[])