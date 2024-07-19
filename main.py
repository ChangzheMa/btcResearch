import data
import pandas as pd
from strategy.price_momentum import ma5_ma10, ma5_ma10_ma20, ma5_ma10_ma20_revert, vwap5_vwap10_vwap20, ma5_ma10_ma20_choice, ma5_ma10_ma20_choice_and_decay
from backtest import do_backtest, do_backtest_detailed
import matplotlib.pyplot as plt


if __name__ == '__main__':
    period = "1s"
    resample = None
    df = data.load_klines(period, resample)
    df, label = ma5_ma10_ma20_choice(df, revert=True)
    portfolios, day_portfolios = do_backtest_detailed(df, period, resample, delay=2, exec_threshold=0.25, label=label)
