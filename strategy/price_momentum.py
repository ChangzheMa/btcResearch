def ma5_ma10(klines):
    print("收盘价、5日均线、10日均线 动量策略")
    klines['MA5'] = klines['close'].rolling(window=5).mean()
    klines['MA10'] = klines['close'].rolling(window=10).mean()
    klines['MA5'] = klines['MA5'].fillna(method='bfill')
    klines['MA10'] = klines['MA10'].fillna(method='bfill')
    cond_down = (klines['close'] < klines['MA5']) & (klines['MA5'] < klines['MA10'])
    cond_up = (klines['close'] > klines['MA5']) & (klines['MA5'] > klines['MA10'])
    klines['ops'] = 0
    klines.loc[cond_down, 'ops'] = -1
    klines.loc[cond_up, 'ops'] = 1
    return klines


def ma5_ma10_ma20(klines):
    print("收盘价、5日均线、10日均线、20日均线 动量策略")
    klines['MA5'] = klines['close'].rolling(window=5).mean()
    klines['MA10'] = klines['close'].rolling(window=10).mean()
    klines['MA20'] = klines['close'].rolling(window=20).mean()
    klines['MA5'] = klines['MA5'].fillna(method='bfill')
    klines['MA10'] = klines['MA10'].fillna(method='bfill')
    klines['MA20'] = klines['MA20'].fillna(method='bfill')

    cond_down = (klines['close'] < klines['MA5']) & (klines['MA5'] < klines['MA10']) & (klines['MA10'] < klines['MA20'])
    cond_up = (klines['close'] > klines['MA5']) & (klines['MA5'] > klines['MA10']) & (klines['MA10'] > klines['MA20'])
    klines['ops'] = 0
    klines.loc[cond_down, 'ops'] = -1
    klines.loc[cond_up, 'ops'] = 1
    return klines


def ma5_ma10_ma20_revert(klines):
    print("收盘价、5日均线、10日均线、20日均线 动量策略及反转")
    klines['MA5'] = klines['close'].rolling(window=5).mean()
    klines['MA10'] = klines['close'].rolling(window=10).mean()
    klines['MA20'] = klines['close'].rolling(window=20).mean()
    klines['MA5'] = klines['MA5'].fillna(method='bfill')
    klines['MA10'] = klines['MA10'].fillna(method='bfill')
    klines['MA20'] = klines['MA20'].fillna(method='bfill')

    cond_down = (klines['close'] < klines['MA5']) & (klines['MA5'] < klines['MA10']) & (klines['MA10'] > klines['MA20'])
    cond_up = (klines['close'] > klines['MA5']) & (klines['MA5'] > klines['MA10']) & (klines['MA10'] < klines['MA20'])
    klines['ops'] = 0
    klines.loc[cond_down, 'ops'] = -1
    klines.loc[cond_up, 'ops'] = 1
    return klines

