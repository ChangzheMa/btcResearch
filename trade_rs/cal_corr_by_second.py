import pandas as pd
import numpy as np
from scipy.stats import pearsonr

from trade_rs.util import get_trade_column_names, cal_column_by_cond

column_names = get_trade_column_names()
df = pd.read_csv('../gate/BTC_USDT-202407.csv', names=column_names)

# df = df[:20000]

df["buy"] = (df['size'] > 0).astype(int)
df["buy_size"] = df["buy"] * df["size"]
df["sell"] = (df['size'] < 0).astype(int)
df["sell_size"] = df["sell"] * df["size"]
df["timestamp_sec"] = df["timestamp"].astype(int)
# df["sec_index"] = np.where(df.groupby('timestamp_sec').cumcount().eq(0), df.index, np.nan)
# df["sec_index"] = df["sec_index"].fillna(method="ffill")

pre_sec_count_list = [5, 10, 20, 40, 80, 160, 320, 640]   # 5秒 ~ 10分钟
factor_list = []
for pre_sec_count in pre_sec_count_list:
    print(f"正在计算前 {pre_sec_count} 秒的买卖不平衡度")
    df[f"buy_count_{pre_sec_count}s"] = cal_column_by_cond(df=df, data_column_name='buy', time_range_in_sec=(-pre_sec_count, 0), operation='sum')
    df[f"sell_count_{pre_sec_count}s"] = cal_column_by_cond(df=df, data_column_name='sell', time_range_in_sec=(-pre_sec_count, 0), operation='sum')
    df[f"count_ib_{pre_sec_count}s"] = (df[f"buy_count_{pre_sec_count}s"] - df[f"sell_count_{pre_sec_count}s"]) / (df[f"buy_count_{pre_sec_count}s"] + df[f"sell_count_{pre_sec_count}s"])
    factor_list.append(f"count_ib_{pre_sec_count}s")
    df[f"buy_size_{pre_sec_count}s"] = cal_column_by_cond(df=df, data_column_name='buy_size', time_range_in_sec=(-pre_sec_count, 0), operation='sum')
    df[f"sell_size_{pre_sec_count}s"] = cal_column_by_cond(df=df, data_column_name='sell_size', time_range_in_sec=(-pre_sec_count, 0), operation='sum')
    df[f"size_ib_{pre_sec_count}s"] = (df[f"buy_size_{pre_sec_count}s"] + df[f"sell_size_{pre_sec_count}s"]) / (df[f"buy_size_{pre_sec_count}s"] - df[f"sell_size_{pre_sec_count}s"])
    factor_list.append(f"size_ib_{pre_sec_count}s")

# future_return_tick_count_list = [20, 40, 80]    # 5秒， 10秒， 20秒
# return_list = []
# for future_return_tick_count in future_return_tick_count_list:
#     df[f"return_{future_return_tick_count}t"] = (df["price"].shift(-future_return_tick_count) - df["price"]) / df["price"]
#     return_list.append(f"return_{future_return_tick_count}t")
#
# df = df.fillna(0)
# df = df.replace([np.inf, -np.inf], 0)
#
# # # 计算 corr
# # corr_list = []
# # for factor_name in factor_list:
# #     for return_name in return_list:
# #         corr, p_value = pearsonr(df[factor_name], df[return_name])
# #         corr_list.append((f"{factor_name}|{return_name}", corr, p_value))
# #
# # corr_list.sort(key=lambda x: abs(x[1]), reverse=True)
# # print(f"use ticks:")
# # for pair in corr_list[:12]:
# #     print(pair)
#
#
# # 每秒抽样，然后计算 corr
# df_sampled = df.groupby("timestamp_sec", as_index=False).first()
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
