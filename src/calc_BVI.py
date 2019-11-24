import os
import pandas as pd
from scipy import interpolate
import numpy as np
import itertools


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


def X_spectral_theoretical(x0, df, Pci):

    """
    spectral BVIをtheoreticalにやった時、
    各コアで最適化したx = sigma / Rho_2 （岩相に依存した係数）の値を求める。
    :inputs
        x first pint of sigma / rho_2
        df
        Pci
    """
    
    # 初期値を指定
    x = x0
    
    # 解きたい方程式 objective
    objective = BVI_spectral_theoretical(x, df, Pci)[0] - df.BVI_Por_cum.iloc[-1]
    objective_dx = BVI_spectral_theoretical(x, df, Pci)[1]
    
    # Newton法で解く。
    for count in range(10000):
        
        x_next = x - objective / objective_dx
        diff_x = abs(x - x_next)
        
        if diff_x > 1:
            x = x_next
            objective = BVI_spectral_theoretical(x, df, Pci)[0] - df.BVI_Por_cum.iloc[-1]
            objective_dx = BVI_spectral_theoretical(x, df, Pci)[1]
        else:
            x = x_next
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
    
    # mについて微分した式
    df["Swi_dm"] = -1 * (df.T2.copy() / ((m * df.T2.copy() + b) ** 2))
    
    # bについて微分した式
    df["Swi_db"] = -1 / ((m * df.T2.copy() + b) ** 2)
    
    # T2 < T2i（すなわちWi > W) のところではSwi = 1, Swiの傾きは0
    df.Swi[df.Swi > 1] = 1
    df.Swi[df.Swi < 0] = 0
    
    df.Swi_dm[df.Swi > 1] = 0
    df.Swi_dm[df.Swi < 0] = 0

    df.Swi_db[df.Swi > 1] = 0
    df.Swi_db[df.Swi < 0] = 0
    
    # spectral BVIを産出
    BVI = df.Por.dot(df.Swi)
    
    # BVIの偏微分を算出
    BVI_dm = df.Por.dot(df.Swi_dm)
    BVI_db = df.Por.dot(df.Swi_db)

    return BVI, BVI_dm, BVI_db


def m_b_spectral_empirical(df, m0, b0):
    
    """
    このモジュールのinput dfは，複数サンプルを含んだdf
    
    """
    
    m_list = []
    b_list = []
    
    # 　inputから，あらゆる組み合わせでsampleを取り出す
    for combi_group in itertools.combinations(df.groupby("ID"), 2):
        key_1, group_1 = combi_group[0]
        key_2, group_2 = combi_group[1]
        
        # 初期設定のmとb
        m = m0
        b = b0

        # objective_1とobjective_2の連立方程式をm, bについて解く
        # ニュートン法を用いる
        for count in range(1000):
            
            objective_1 = BVI_spectral_empirical(group_1, m, b)[0] - group_1.BVI_Por_cum.iloc[-1]
            objective_2 = BVI_spectral_empirical(group_2, m, b)[0] - group_2.BVI_Por_cum.iloc[-1]
            
            objective_dm_1 = BVI_spectral_empirical(group_1, m, b)[1]
            objective_db_1 = BVI_spectral_empirical(group_1, m, b)[2]
            
            objective_dm_2 = BVI_spectral_empirical(group_2, m, b)[1]
            objective_db_2 = BVI_spectral_empirical(group_2, m, b)[2]
            
            # 計算をしやすくするために行列の形にする
            var_array = np.array([m, b])
            
            objective_array = np.array([objective_1, objective_2])
            
            gradient_matrix = np.array([[objective_dm_1, objective_db_1],
                                        [objective_dm_2, objective_db_2]])
            
            # 漸化式を解き、次のステップのm, bを算出
            next_var_array = var_array - np.dot(
                    np.linalg.pinv(gradient_matrix), objective_array)
            m = next_var_array[0]
            b = next_var_array[1]
            
            diff = np.sqrt(np.sum((var_array - next_var_array) ** 2))
            
            if diff > 0.1:
                # print("m={0}, b={1}, continue".format(m, b))
                continue
            else:
                print("break! k1={0}, k2={1}, m={3}, b={4}, count={2}".format(
                        key_1, key_2, count, m, b))
                m_list.append(m)
                b_list.append(b)
                break
    
    # 条件で搾れるようarrayに直す
    m_list = np.array(m_list)
    b_list = np.array(b_list)
    
    # 0 < m < 0.1, b > 0 を満たすべき
    m_list_adopted = m_list[(0 < m_list) & (m_list < 0.2) & (0 < b_list) & (b_list < 3)]
    b_list_adopted = b_list[(0 < m_list) & (m_list < 0.2) & (0 < b_list) & (b_list < 3)]
        
    # m_listおよびb_listの平均値を最適なm, bの値とする
    optimized_m = sum(m_list_adopted) / len(m_list_adopted)
    optimized_b = sum(b_list_adopted) / len(b_list_adopted)
    
    print("optimized_m = {0}".format(optimized_m))
    print("optimized_b = {0}".format(optimized_b))
    
    return m_list_adopted, b_list_adopted, optimized_m, optimized_b


if __name__ == "__main__":


    # ---------inputs-------------------

    input_folderpath = r"C:\Users\02217013\Documents"
    input_filename = "calliance1_nmr.csv"
    
    # irreducible conditionのときのPc とりあえずPsiで構わん（というか統一してあれば単位何でもいい）
    the_Pci = 50

    # newton法をすたーとするx, m, bの値
    x0 = 1000

    m0 = 0.055
    b0 = 1
    
    # default cutoff値
    C = 33

    # ---------------------------------

    input_file = os.path.join(input_folderpath, input_filename)
    the_df = pd.read_csv(input_file)
    # the_cut_coates_dict = main(the_df)
    
    m_list, b_list, optimized_m, optimized_b = m_b_spectral_empirical(the_df, m0, b0)
    
    """
    for key, group in the_df.groupby("ID"):
        
        # cutoff BVIを算出
        the_BVI_cutoff = BVI_cutoff(group, C)
        
        # calc_T2_cutoff
        the_t2_cutoff = calc_cutoff_C(group)
        
        # calc best x using newton method
        optimized_x = X_spectral_theoretical(x0, group, the_Pci)
        
        
        print(the_BVI_cutoff, the_t2_cutoff, optimized_x)
    """