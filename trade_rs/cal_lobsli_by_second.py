import os

import pandas as pd
import numpy as np
from scipy.stats import pearsonr

from trade_rs.util import get_trade_column_names, cal_column_by_cond, get_lob_column_names


def read_file_to_csv(file_path, factor_list=None):
    if factor_list is None:
        factor_list = ['lob_vol_ib1']

    f = open(file_path, 'r')
    lines = f.readlines()
    data = []
    for line in lines:



column_names = get_lob_column_names()
files = [file for file in os.listdir('../gate/lobsli/')]
files.sort()

dfs = [pd.read_csv(f"../gate/lobsli/{file}", names=column_names) for file in files]
print(dfs)

# df["buy"] = (df['size'] > 0).astype(int)
# df["buy_size"] = df["buy"] * df["size"]
# df["sell"] = (df['size'] < 0).astype(int)
# df["sell_size"] = df["sell"] * df["size"]
# df["timestamp_sec"] = df["timestamp"].astype(int)
#
# df_grouped = df.groupby("timestamp_sec").agg(
#     buy_size_sum=('buy_size', 'sum'),
#     buy_count=('buy', 'sum'),
#     sell_size_sum=('sell_size', 'sum'),
#     sell_count=('sell', 'sum'),
#     price=('price', 'first'),
# )
#
# full_range = pd.DataFrame({
#     'timestamp_sec': np.arange(df_grouped.index.min(), df_grouped.index.max() + 1)
# }).set_index('timestamp_sec')
# df_filled = df_grouped.reindex(full_range.index)
# df_filled[['buy_size_sum', 'buy_count', 'sell_size_sum', 'sell_count']] = df_filled[['buy_size_sum', 'buy_count', 'sell_size_sum', 'sell_count']].fillna(0)
# df_filled['price'] = df_filled['price'].fillna(method='ffill')
#
# pre_sec_count_list = [5, 10, 20, 40, 80, 160, 320, 640]   # 5秒 ~ 10分钟
# factor_list = []
# for pre_sec_count in pre_sec_count_list:
#     print(f"正在计算前 {pre_sec_count} 秒的买卖不平衡度")
#     df_filled[f"buy_count_{pre_sec_count}s"] = df_filled["buy_count"].rolling(window=pre_sec_count).sum()
#     df_filled[f"sell_count_{pre_sec_count}s"] = df_filled["sell_count"].rolling(window=pre_sec_count).sum()
#     df_filled[f"count_ib_{pre_sec_count}s"] = (df_filled[f"buy_count_{pre_sec_count}s"] - df_filled[f"sell_count_{pre_sec_count}s"]) / (df_filled[f"buy_count_{pre_sec_count}s"] + df_filled[f"sell_count_{pre_sec_count}s"])
#     factor_list.append(f"count_ib_{pre_sec_count}s")
#     # df_filled[f"buy_size_{pre_sec_count}s"] = df_filled["buy_size_sum"].rolling(window=pre_sec_count).sum()
#     # df_filled[f"sell_size_{pre_sec_count}s"] = df_filled["sell_size_sum"].rolling(window=pre_sec_count).sum()
#     # df_filled[f"size_ib_{pre_sec_count}s"] = (df_filled[f"buy_size_{pre_sec_count}s"] + df_filled[f"sell_size_{pre_sec_count}s"]) / (df_filled[f"buy_size_{pre_sec_count}s"] - df_filled[f"sell_size_{pre_sec_count}s"])
#     # factor_list.append(f"size_ib_{pre_sec_count}s")
#
# future_return_sec_count_list = [5, 10, 20]    # 5秒， 10秒， 20秒
# return_list = []
# for future_return_sec_count in future_return_sec_count_list:
#     df_filled[f"return_{future_return_sec_count}s"] = (df_filled["price"].shift(-future_return_sec_count) - df_filled["price"]) / df_filled["price"]
#     return_list.append(f"return_{future_return_sec_count}s")
#
# df_filled = df_filled.fillna(0)
# df_filled = df_filled.replace([np.inf, -np.inf], 0)
#
#
# # # 每秒抽样，然后计算 corr
# # df_sampled = df_filled
#
# # 每秒抽样并且过滤过去5秒交易很少的行，然后计算 corr
# df_sampled = df_filled[df_filled['buy_count_5s'] + df_filled['sell_count_5s'] >= 3]
#
# corr_list_sampled = []
# for factor_name in factor_list:
#     for return_name in return_list:
#         corr, p_value = pearsonr(df_sampled[factor_name], df_sampled[return_name])
#         corr_list_sampled.append((f"{factor_name}|{return_name}", corr, p_value))
#
# corr_list_sampled.sort(key=lambda x: abs(x[1]), reverse=True)
# print("")
# print(f"use ticks and sampled:")
# for pair in corr_list_sampled[:12]:
#     print(pair)
#
#
# # 分层，然后计算 corr
# bins = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
# for pair in corr_list_sampled[:12]:
#     [factor_name, return_name] = pair[0].split('|')
#     print("")
#     print(f"分层: {factor_name} {return_name}")
#     # print("十分位分层:")
#     # df_sampled['decile'] = pd.qcut(df_sampled[factor_name], q=10, labels=False, duplicates='drop')
#     # sub_dfs = [df_sampled[df_sampled['decile'] == i] for i in range(10)][::-1]
#     # for idx, sub_df in enumerate(sub_dfs):
#     #     if len(sub_df) > 1:
#     #         corr, p_value = pearsonr(sub_df[factor_name], sub_df[return_name])
#     #         print(f"第{idx+1}层[{sub_df[factor_name].min()}~{sub_df[factor_name].max()}]: corr {corr}, p_value {p_value}")
#     #     else:
#     #         print(f"第{idx+1}层没有数据")
#     print("绝对值十分位分层:")
#     # df_sampled['decile'] = pd.qcut(abs(df_sampled[factor_name]), q=10, labels=False, duplicates='drop')
#     # sub_dfs_abs = [df_sampled[df_sampled['decile'] == i] for i in range(10)][::-1]
#     df_sampled['binned'] = pd.cut(abs(df_sampled[factor_name]), bins=bins, labels=False)
#     sub_dfs_abs = [df_sampled[df_sampled['binned'] == i] for i in range(10)][::-1]
#     for idx, sub_df in enumerate(sub_dfs_abs):
#         if len(sub_df) > 1:
#             corr, p_value = pearsonr(sub_df[factor_name], sub_df[return_name])
#             if corr > 0.05:
#                 print(f"第{idx+1}层[{sub_df[factor_name].abs().min()}~{sub_df[factor_name].abs().max()}, {len(sub_df)}]: corr {corr}, p_value {p_value}")
#             else:
#                 print(f"第{idx + 1}层[{sub_df[factor_name].abs().min()}~{sub_df[factor_name].abs().max()}, {len(sub_df)}]: 不显著")
#         else:
#             print(f"第{idx+1}层没有数据")
