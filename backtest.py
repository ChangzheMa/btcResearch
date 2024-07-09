import data
import pandas as pd
import matplotlib.pyplot as plt
from strategy.price_momentum import ma5_ma10
from util import print_portfolio_metrics


def do_backtest(klines):
    # 回测参数
    CASH = 1e6
    POS = 0
    DELAY = 3

    portfolios = [CASH]
    day_portfolios = [CASH]
    total_value = float(CASH)

    for index in range(DELAY, len(klines)):
        total_value = CASH + POS * klines.iloc[index]['open']
        if total_value < 0:
            raise "爆仓了"

        portfolios.append(total_value)
        if index % (3600 * 24) == 0:
            print(f"day {int(index / 3600 / 24):2d}, value {total_value:.5f}")
            day_portfolios.append(total_value)

        ops = klines.iloc[index - DELAY]['ops']
        CASH = (1 - ops) * total_value
        POS = ops * total_value / klines.iloc[index]['open']

    day_portfolios.append(total_value)

    plt.plot(portfolios)
    plt.show()
    print_portfolio_metrics(day_portfolios)
