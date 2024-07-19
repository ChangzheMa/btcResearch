import datetime

import data
import pandas as pd
import matplotlib.pyplot as plt
from strategy.price_momentum import ma5_ma10
from util import print_portfolio_metrics

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


def do_backtest(klines, period="1s", resample=None, delay=3, label=""):
    print(f"回测参数, period: {period}, resample: {resample}, delay: {delay}")
    # 回测参数
    CASH = 1
    POS = 0
    DELAY = delay
    ROWS_PER_DAY = 3600 * 24 if period == "1s" and resample is None \
        else 3600 * 24 / 3 if period == "1s" and resample == "3s" \
        else 3600 * 24 / 5 if period == "1s" and resample == "5s" \
        else 60 * 24 if period == "1m" \
        else 12 * 24 if period == "5m" \
        else 24 if period == "1h" \
        else 1

    portfolios = [CASH]
    day_portfolios = [CASH]
    total_value = float(CASH)

    for index in range(DELAY, len(klines)):
        total_value = CASH + POS * klines.iloc[index]['open']
        if total_value < 0:
            raise "爆仓了"

        portfolios.append(total_value)
        if index % ROWS_PER_DAY == 0:
            print(f"day {int(index / ROWS_PER_DAY):2d}, value {total_value:.5f}")
            day_portfolios.append(total_value)

        ops = klines.iloc[index - DELAY]['ops']
        CASH = (1 - ops) * total_value
        POS = ops * total_value / klines.iloc[index]['open']

    day_portfolios.append(total_value)

    annualized_return, max_drawdown, annualized_sharpe_ratio = print_portfolio_metrics(day_portfolios)
    plt.plot(portfolios)
    plt.yscale('log')
    plt.title(
        f"{label} \n period: {period}, resample: {resample}, delay: {delay}, sharp: {annualized_sharpe_ratio:.3f}")
    plt.savefig(f"test_result\\period{period}_resample{resample}_delay{delay}.png")

    return portfolios, day_portfolios


def do_backtest_detailed(klines: pd.DataFrame, period="1s", resample=None, delay=3, exec_threshold=0.3, exec_price_check_type="open_close", label=""):
    """
    细致的回测，会考虑挂单是否能成交，要求 klines 上有 volume 和 taker_buy_volume 列
    :param klines: k线数据，要求有 volume 和 taker_buy_volume 列
    :param period: k线的原始周期
    :param resample: k线读取后经过缩放的周期，我们这里用缩放后周期回测
    :param delay: 延迟几跳下单
    :param exec_threshold: 当k线上满足方向的成交比例大于x时，方能成交
    :param exec_price_check_type: "open_close" | "high_low"，当局下单价格在 open/close 或 high/low 之间时才可能成交
    :param label: 说明信息
    :return:
    """
    print(f"回测参数, period: {period}, resample: {resample}, delay: {delay}, exec_threshold: {exec_threshold}")
    # 回测参数
    CASH = 1
    DELAY = delay
    ROWS_PER_DAY = 3600 * 24 if period == "1s" and resample is None \
        else 3600 * 24 / 3 if period == "1s" and resample == "3s" \
        else 3600 * 24 / 5 if period == "1s" and resample == "5s" \
        else 60 * 24 if period == "1m" \
        else 12 * 24 if period == "5m" \
        else 24 if period == "1h" \
        else 1

    klines['taker_sell_volume'] = klines['volume'] - klines['taker_buy_volume']
    klines['can_buy'] = klines['taker_sell_volume'] > klines['volume'] * exec_threshold
    klines['can_sell'] = klines['taker_buy_volume'] > klines['volume'] * exec_threshold
    klines['position'] = 0
    klines['cash'] = CASH

    print(f"[{datetime.datetime.now()}]")

    portfolios = []
    day_portfolios = []
    order_arr = [0] * DELAY
    order_price_arr = [0] * DELAY
    pre_row = None
    curr_row = None
    for idx, row in klines.iterrows():
        # 更新当前数据
        pre_row = curr_row if curr_row is not None else row
        curr_row = row
        order = order_arr[-DELAY]
        order_price = order_price_arr[-DELAY]

        # 执行
        if exec_price_check_type == "open_close":
            executed = (
                    (order_price - curr_row.open) * (order_price - curr_row.close) < 0
                    and (curr_row.can_buy if order > 0 else curr_row.can_sell))
        elif exec_price_check_type == "high_low":
            executed = (
                    (order_price - curr_row.high) * (order_price - curr_row.low) < 0
                    and (curr_row.can_buy if order > 0 else curr_row.can_sell))
        else:
            raise "exec_price_check_type 不正确，只能为 open_close 或 high_low"
        if executed:
            position = pre_row.position + order
            cash = pre_row.cash - order * order_price
        else:
            position = pre_row.position
            cash = pre_row.cash
        curr_row['position', 'cash'] = [position, cash]

        # 下单
        next_order_price = curr_row.order_price if curr_row.order_price is not None else curr_row.close
        value = position * next_order_price + cash
        next_order = value * curr_row.ops / next_order_price - position
        order_arr.append(next_order)
        order_price_arr.append(next_order_price)

        # 记录资产并按日打印
        close_value = curr_row.cash + curr_row.position * curr_row.close
        portfolios.append(close_value)
        if idx % ROWS_PER_DAY == 0 or idx == len(klines)-1:
            print(f"day {int(idx / ROWS_PER_DAY):2d}, value {close_value:.5f} [{datetime.datetime.now()}]")
            day_portfolios.append(close_value)

    annualized_return, max_drawdown, annualized_sharpe_ratio = print_portfolio_metrics(day_portfolios)
    plt.plot(portfolios)
    plt.title(
        f"{label} \n period: {period}, resample: {resample}, delay: {delay}, sharp: {annualized_sharpe_ratio:.3f}")
    plt.savefig(f"test_result\\period{period}_resample{resample}_delay{delay}.png")

    return portfolios, day_portfolios
