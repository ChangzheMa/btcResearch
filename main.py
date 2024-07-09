import data
import pandas as pd
from strategy.price_momentum import ma5_ma10, ma5_ma10_ma20, vwap5_vwap10_vwap20
from backtest import do_backtest


if __name__ == '__main__':
    df = data.load_klines()
    df = ma5_ma10_ma20(df)
    do_backtest(df)
