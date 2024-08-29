import pandas as pd

from trade_rs.util import get_trade_column_names


column_names = get_trade_column_names()
df = pd.read_csv('../gate/BTC_USDT-202407.csv', names=column_names)

df["buy"] = (df['size'] > 0).astype(int)
df["sell"] = (df['size'] < 0).astype(int)

pre_tick_count_list = [20, 40, 80, 160, 320, 640, 1280, 2560]   # 5秒 ~ 10分钟
for pre_tick_count in pre_tick_count_list:
    df[f"buy_count_{pre_tick_count}"] = df["buy"].rolling(window=pre_tick_count).sum()
    df[f"sell_count_{pre_tick_count}"] = df["sell"].rolling(window=pre_tick_count).sum()
    df[f"count_ib_{pre_tick_count}"] = (df[f"buy_count_{pre_tick_count}"] - df[f"sell_count_{pre_tick_count}"]) / (df[f"buy_count_{pre_tick_count}"] + df[f"sell_count_{pre_tick_count}"])
    df[f"buy_size_{pre_tick_count}"] = (df["buy"] * df["size"]).rolling(window=pre_tick_count).sum()
    df[f"sell_size_{pre_tick_count}"] = (df["sell"] * df["size"]).rolling(window=pre_tick_count).sum()
    df[f"size_ib_{pre_tick_count}"] = (df[f"buy_size_{pre_tick_count}"] + df[f"sell_size_{pre_tick_count}"]) / (df[f"buy_size_{pre_tick_count}"] - df[f"sell_size_{pre_tick_count}"])

future_return_tick_count_list = [20, 40, 80]    # 5秒， 10秒， 20秒
for future_return_tick_count in future_return_tick_count_list:
    df[f"return_{future_return_tick_count}"] = (df["price"].shift(-future_return_tick_count) - df["price"]) / df["price"]
