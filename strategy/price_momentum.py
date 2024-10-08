def ma5_ma10(klines, revert=False):
    label = "收盘价、5日均线、10日均线 动量策略"
    print(label)
    klines['MA5'] = klines['close'].rolling(window=5).mean()
    klines['MA10'] = klines['close'].rolling(window=10).mean()
    klines['MA5'] = klines['MA5'].fillna(method='bfill')
    klines['MA10'] = klines['MA10'].fillna(method='bfill')
    cond_down = (klines['close'] < klines['MA5']) & (klines['MA5'] < klines['MA10'])
    cond_up = (klines['close'] > klines['MA5']) & (klines['MA5'] > klines['MA10'])
    klines['ops'] = 0
    klines.loc[cond_down, 'ops'] = -1
    klines.loc[cond_up, 'ops'] = 1
    klines['order_price'] = klines['close']
    if revert:
        klines['ops'] = -klines['ops']
    return klines, label


def ma5_ma10_ma20(klines, revert=False):
    label = "收盘价、5日均线、10日均线、20日均线 动量策略"
    print(label)
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
    klines['order_price'] = klines['close']
    if revert:
        klines['ops'] = -klines['ops']
    return klines, label


def ma5_ma10_ma20_revert(klines, revert=False):
    """
    这个不好，会亏本
    """
    label = "收盘价、5日均线、10日均线、20日均线 动量策略及反转"
    print(label)
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
    klines['order_price'] = klines['close']
    if revert:
        klines['ops'] = -klines['ops']
    return klines, label


def vwap5_vwap10_vwap20(klines, revert=False):
    label = "收盘价、5日vwap、10日vwap、20日vwap 动量策略"
    print(label)
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
    klines['order_price'] = klines['close']
    if revert:
        klines['ops'] = -klines['ops']
    return klines, label


def ma5_ma10_ma20_choice(klines, revert=False):
    label = "收盘价、5日均线、10日均线、20日均线 动量策略，添加分钟线择时"
    print(label)
    klines['MA5'] = klines['close'].rolling(window=5).mean()
    klines['MA10'] = klines['close'].rolling(window=10).mean()
    klines['MA20'] = klines['close'].rolling(window=20).mean()
    klines['MA5'] = klines['MA5'].fillna(method='bfill')
    klines['MA10'] = klines['MA10'].fillna(method='bfill')
    klines['MA20'] = klines['MA20'].fillna(method='bfill')

    klines['MA300'] = klines['close'].rolling(window=300).mean()
    klines['MA600'] = klines['close'].rolling(window=600).mean()
    klines['MA300'] = klines['MA300'].fillna(method='bfill')
    klines['MA600'] = klines['MA600'].fillna(method='bfill')

    cond_down = (klines['close'] < klines['MA5']) & (klines['MA5'] < klines['MA10']) & (klines['MA10'] < klines['MA20'])
    cond_up = (klines['close'] > klines['MA5']) & (klines['MA5'] > klines['MA10']) & (klines['MA10'] > klines['MA20'])
    cond_down_reverse = ((klines['close'] < klines['MA300']) & (klines['MA300'] < klines['MA600']))
    cond_up_reverse = (klines['close'] > klines['MA300']) & (klines['MA300'] > klines['MA600'])

    klines['ops'] = 0
    klines.loc[cond_down & (~cond_down_reverse), 'ops'] = -1
    klines.loc[cond_up & (~cond_up_reverse), 'ops'] = 1
    klines['order_price'] = klines['close']
    if revert:
        klines['ops'] = -klines['ops']
    return klines, label


def ma5_ma10_ma20_choice_and_decay(klines, revert=False):
    decay = 0.7
    label = f"收盘价、5日均线、10日均线、20日均线 动量策略，添加分钟线择时，{decay}衰减"
    print(label)
    klines['MA5'] = klines['close'].rolling(window=5).mean()
    klines['MA10'] = klines['close'].rolling(window=10).mean()
    klines['MA20'] = klines['close'].rolling(window=20).mean()
    klines['MA5'] = klines['MA5'].fillna(method='bfill')
    klines['MA10'] = klines['MA10'].fillna(method='bfill')
    klines['MA20'] = klines['MA20'].fillna(method='bfill')

    klines['MA300'] = klines['close'].rolling(window=300).mean()
    klines['MA600'] = klines['close'].rolling(window=600).mean()
    klines['MA300'] = klines['MA300'].fillna(method='bfill')
    klines['MA600'] = klines['MA600'].fillna(method='bfill')

    cond_down = (klines['close'] < klines['MA5']) & (klines['MA5'] < klines['MA10']) & (klines['MA10'] < klines['MA20'])
    cond_up = (klines['close'] > klines['MA5']) & (klines['MA5'] > klines['MA10']) & (klines['MA10'] > klines['MA20'])
    cond_down_reverse = ((klines['close'] < klines['MA300']) & (klines['MA300'] < klines['MA600']))
    cond_up_reverse = (klines['close'] > klines['MA300']) & (klines['MA300'] > klines['MA600'])

    klines['_ops'] = 0
    klines.loc[cond_down & (~cond_down_reverse), '_ops'] = -1
    klines.loc[cond_up & (~cond_up_reverse), '_ops'] = 1
    klines['ops'] = klines['_ops'] * decay + klines['_ops'].shift(1) * (1-decay)
    klines['ops'] = klines['ops'].fillna(method='bfill')
    klines['order_price'] = klines['close']
    if revert:
        klines['ops'] = -klines['ops']
    return klines, label
