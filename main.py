import data
import pandas as pd
from strategy.price_momentum import ma5_ma10
from backtest import do_backtest


if __name__ == '__main__':
    df = data.load_klines()
    df = ma5_ma10(df)
    do_backtest(df)
