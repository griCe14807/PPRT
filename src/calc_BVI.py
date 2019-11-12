import os
import pandas as pd
from scipy import interpolate
import numpy as np


def BVI_cutoff(df, C):

    """
    cutoff BVIを計算
    """

    return np.sum(df.Por[df.T2 < C])


def calc_cutoff_C(df):
    """
    各コアで最適なcutff Cの値を算出する。
    
    :param df: groupbyで単一sampleについてのデータにしてからinputする必要ある。
    :return: t2_cutoff 最適化されたcutoff値
    
    """
    # xの増分が0だとうまくinterpolateできないため、微小量増加を入れる
    cum_por = []
    for i, cum_por_ in enumerate(df.Por_cum):
        cum_por_ = cum_por_ + 0.00001 * i
        cum_por.append(cum_por_)

    # cutoff値を計算
    t2_cutoff = float(interpolate.interp1d(cum_por, df.T2, kind="linear")(df.BVI_Por_cum.iloc[-1]))

    return t2_cutoff


def BVI_spectral_theoretical(x, df, Pci):
    
    """
    X, df, Pciをインプットとして、コアサンプルのspectral BVIおよびそのx微分値を返す。
    ただしx = sigma / rho2 とする。
    
    """
        
    # 各T2におけるSwiの列を作成
    T2i = x / Pci
    df["Swi"] = T2i / df.T2.copy() * (2 - T2i / df.T2.copy())
    
    # 微分した式
    df["Swi_dx"] = 2 / (df.T2 * Pci) - 2 * x / (df.T2 * df.T2 * Pci * Pci)

    # T2 < T2i（すなわちWi > W) のところではSwi = 1, Swiの傾きは0
    df.Swi[df.T2 < T2i] = 1
    df.Swi_dx[df.T2 < T2i] = 0

    # spectral BVIを産出
    BVI = df.Por.dot(df.Swi)
    
    # spectral BVIのx微分の値は
    BVI_dx = df.Por.dot(df.Swi_dx)
    
    return BVI, BVI_dx


def X_spectral_theoretical(x, df, Pci):

    """
    spectral BVIをtheoreticalにやった時、
    各コアで最適化したx = sigma / Rho_2 （岩相に依存した係数）の値を求める。
    :inputs
        x first pint of sigma / rho_2
        df
        Pci
    """
    
    objective = BVI_spectral(x, df, Pci)[0] - df.BVI_Por_cum.iloc[-1]
    objective_dx = BVI_spectral(x, df, Pci)[1]
    
    # Newton法で解く。
    for count in range(10000):
        
        x_next = x - objective / objective_dx
        diff_x = abs(x - x_next)
        
        if diff_x > 1:
            x = x_next
            objective = BVI_spectral(x, df, Pci)[0] - df.BVI_Por_cum.iloc[-1]
            objective_dx = BVI_spectral(x, df, Pci)[1]
        else:
            # print("sample={4}, count={0}, x={1}, objective={2}, diff_x={3}, dx={5}".format(
              #       count, x, objective, diff_x, df.ID.iloc[1], objective_dx))
            break
    
    return x


def BVI_spectral_empirical(df, m, b):

    """
    経験式に基づいたspectral BVIの算出
    
    """
        
    # 各T2におけるSwiの列を作成
    df["Swi"] = 1 / (m * df.T2.copy() + b)
    
    # T2 < T2i（すなわちWi > W) のところではSwi = 1, Swiの傾きは0
    df.Swi[df.Swi > 1] = 1
    df.Swi[df.Swi < 0] = 0

    # spectral BVIを産出
    BVI = df.Por.dot(df.Swi)

    return BVI



if __name__ == "__main__":


    # ---------inputs-------------------

    input_folderpath = r"C:\Users\02217013\Documents"
    input_filename = "calliance1_nmr.csv"
    
    # irreducible conditionのときのPc とりあえずPsiで構わん（というか統一してあれば単位何でもいい）
    the_Pci = 50

    # newton法をすたーとするxの値
    x0 = 1000
    
    # default cutoff値
    C = 33

    # ---------------------------------

    input_file = os.path.join(input_folderpath, input_filename)
    the_df = pd.read_csv(input_file)
    # the_cut_coates_dict = main(the_df)
    
    for key, group in the_df.groupby("ID"):
        
        # cutoff BVIを算出
        the_BVI_cutoff = BVI_cutoff(group, C)
        
        # calc_T2_cutoff
        the_t2_cutoff = calc_cutoff_C(group)
        
        # calc best x using newton method
        optimized_x = X_spectral_theoretical(x0, group, the_Pci)
        
        
        print(the_BVI_cutoff, the_t2_cutoff, optimized_x)