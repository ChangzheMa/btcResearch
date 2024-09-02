import pandas as pd
import numpy as np

from trade_rs.util import get_trade_column_names


column_names = get_trade_column_names()
df = pd.read_csv('../gate/BTC_USDT-202407.csv', names=column_names)

df["buy"] = (df['size'] > 0).astype(int)
df["sell"] = (df['size'] < 0).astype(int)

pre_tick_count_list = [20, 40, 80, 160, 320, 640, 1280, 2560]   # 5秒 ~ 10分钟
factor_list = []
for pre_tick_count in pre_tick_count_list:
    df[f"buy_count_{pre_tick_count}t"] = df["buy"].rolling(window=pre_tick_count).sum()
    df[f"sell_count_{pre_tick_count}t"] = df["sell"].rolling(window=pre_tick_count).sum()
    df[f"count_ib_{pre_tick_count}t"] = (df[f"buy_count_{pre_tick_count}t"] - df[f"sell_count_{pre_tick_count}t"]) / (df[f"buy_count_{pre_tick_count}t"] + df[f"sell_count_{pre_tick_count}t"])
    factor_list.append(f"count_ib_{pre_tick_count}t")
    df[f"buy_size_{pre_tick_count}t"] = (df["buy"] * df["size"]).rolling(window=pre_tick_count).sum()
    df[f"sell_size_{pre_tick_count}t"] = (df["sell"] * df["size"]).rolling(window=pre_tick_count).sum()
    df[f"size_ib_{pre_tick_count}t"] = (df[f"buy_size_{pre_tick_count}t"] + df[f"sell_size_{pre_tick_count}t"]) / (df[f"buy_size_{pre_tick_count}t"] - df[f"sell_size_{pre_tick_count}t"])
    factor_list.append(f"size_ib_{pre_tick_count}t")

future_return_tick_count_list = [20, 40, 80]    # 5秒， 10秒， 20秒
return_list = []
for future_return_tick_count in future_return_tick_count_list:
    df[f"return_{future_return_tick_count}t"] = (df["price"].shift(-future_return_tick_count) - df["price"]) / df["price"]
    return_list.append(f"return_{future_return_tick_count}t")

df = df.fillna(0)
df = df.replace([np.inf, -np.inf], 0)

corr_list = []
for factor_name in factor_list:
    for return_name in return_list:
        corr = df[factor_name].corr(df[return_name])
        corr_list.append((f"{factor_name}_{return_name}", corr))

corr_list.sort(key=lambda x: abs(x[1]), reverse=True)
print(f"use ticks:")
for pair in corr_list:
    print(pair)
