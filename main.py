import data
import pandas as pd
from strategy.price_momentum import ma5_ma10, ma5_ma10_ma20, vwap5_vwap10_vwap20, ma5_ma10_ma20_choice, ma5_ma10_ma20_choice_and_decay
from backtest import do_backtest
import matplotlib.pyplot as plt


if __name__ == '__main__':
    period = "1s"
    resample = "3s"
    df = data.load_klines(period, resample)
    df, label = ma5_ma10_ma20_choice(df, revert=False)
    portfolios, day_portfolios = do_backtest(df, period, resample, delay=1, label=label)
