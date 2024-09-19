import numpy as np
import pandas as pd
from bisect import bisect_left, bisect_right


def get_trade_column_names():
    return ['timestamp', 'id', 'price', 'size']


def get_lob_column_names():
    return ['timestamp', 'action', 'price', 'size', 'begin_id', 'merged']


def get_lob_factor_name_list():
    return [
        'lob_vol_ib1', 'lob_vol_ib2', 'lob_vol_ib3', 'lob_vol_ib4', 'lob_vol_ib5',
        'lob_vol_ib6', 'lob_vol_ib7', 'lob_vol_ib8', 'lob_vol_ib9', 'lob_vol_ib10'   # 某档位挂单不平衡度，从 1 开始
    ]


# def cal_column_by_cond(row, df, data_column_name, time_range_in_sec=(-5, 0), operation='sum'):
#     current_time = row['timestamp']
#     mask = (df['timestamp'] >= current_time + time_range_in_sec[0]) & (df['timestamp'] <= current_time + time_range_in_sec[1])
#     if operation == 'sum':
#         return df.loc[mask, data_column_name].sum()
#     elif operation == 'count':
#         return df.loc[mask, data_column_name].count()
#     else:
#         raise ValueError(f"Unsupported operation: {operation}")


def cal_column_by_cond(df, data_column_name, time_range_in_sec=(-5, 0), operation='sum'):
    timestamps = df['timestamp_sec']

    result = np.zeros(len(df))

    for i, current_time in enumerate(timestamps):
        start_time = current_time + time_range_in_sec[0]
        end_time = current_time + time_range_in_sec[1]

        start_idx = bisect_left(timestamps, start_time)
        end_idx = bisect_left(timestamps, end_time)

        if operation == 'sum':
            result[i] = df.iloc[start_idx:end_idx][data_column_name].sum()
        elif operation == 'count':
            result[i] = end_idx - start_idx
        else:
            raise ValueError(f"Unsupported operation: {operation}")

    return result
