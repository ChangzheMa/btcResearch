import numpy as np
import pandas as pd
import datetime as dt

import os

os.chdir('E:\\src\\btcResearch')


def load_klines(period="1s", resample=None):
    dfs = []
    folder = 'binance/trade'
    for file in os.listdir(folder):
        if file.startswith(f"BTCFDUSD-{period}-"):
            dfs.append(pd.read_csv(os.path.join(folder, file),
                                   names=['open_time', 'open', 'high', 'low', 'close', 'volume', 'close_time',
                                          'quote_volume', 'count', 'taker_buy_volume', 'taker_buy_quote_volume',
                                          'ignore']))
    df = pd.concat(dfs)
    if resample is not None:
        df['open_time'] = pd.to_datetime(df['open_time'], unit='ms')
        df.set_index('open_time', inplace=True)
        df = df.resample(resample).apply({
            'open': 'first',
            'high': 'max',
            'low': 'min',
            'close': 'last',
            'volume': 'sum',
            'close_time': 'last',
            'quote_volume': 'sum',
            'count': 'sum',
            'taker_buy_volume': 'sum',
            'taker_buy_quote_volume': 'sum',
            'ignore': 'first'
        })
        df.dropna(how='any', inplace=True)
    df.reset_index(inplace=True)
    return df


def load_aggTrades():
    dfs = []
    folder = 'binance/trade'
    for file in os.listdir(folder):
        if file.startswith('BTCFDUSD-aggTrades-'):
            dfs.append(pd.read_csv(os.path.join(folder, file),
                                   names=['agg_trade_id', 'price', 'quantity', 'first_trade_id', 'last_trade_id',
                                          'transact_time', 'is_buyer_maker', 'ignore']))
    return pd.concat(dfs)


def load_tickTrades():
    dfs = []
    folder = 'binance/trade'
    for file in os.listdir(folder):
        if file.startswith('BTCFDUSD-trades-'):
            dfs.append(pd.read_csv(os.path.join(folder, file),
                                   names=['id', 'price', 'qty', 'base_qty', 'time', 'is_buyer_maker', 'ignore']))
    return pd.concat(dfs)
