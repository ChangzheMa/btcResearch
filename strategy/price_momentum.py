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
    """
    这个不好，会亏本
    """
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


def vwap5_vwap10_vwap20(klines):
    print("收盘价、5日vwap、10日vwap、20日vwap 动量策略")
    klines['typical_price'] = (klines['high'] + klines['low'] + klines['close']) / 3
    klines['price_volume'] = klines['typical_price'] * klines['volume']

    klines['vwap5'] = klines['price_volume'].rolling(window=5).sum() / klines['volume'].rolling(window=5).sum()
    klines['vwap10'] = klines['price_volume'].rolling(window=10).sum() / klines['volume'].rolling(window=10).sum()
    klines['vwap20'] = klines['price_volume'].rolling(window=20).sum() / klines['volume'].rolling(window=20).sum()
    klines['vwap5'] = klines['vwap5'].fillna(method='bfill')
    klines['vwap10'] = klines['vwap10'].fillna(method='bfill')
    klines['vwap20'] = klines['vwap20'].fillna(method='bfill')

    cond_down = (klines['close'] < klines['vwap5']) & (klines['vwap5'] < klines['vwap10']) & (klines['vwap10'] < klines['vwap20'])
    cond_up = (klines['close'] > klines['vwap5']) & (klines['vwap5'] > klines['vwap10']) & (klines['vwap10'] > klines['vwap20'])
    klines['ops'] = 0
    klines.loc[cond_down, 'ops'] = -1
    klines.loc[cond_up, 'ops'] = 1
    return klines

