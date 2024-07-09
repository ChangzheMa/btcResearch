import numpy as np


def calculate_portfolio_metrics(portfolio, risk_free_rate=0.01, trading_days=365):
    portfolio = np.array(portfolio)
    daily_returns = np.diff(portfolio) / portfolio[:-1]

    total_return = portfolio[-1] / portfolio[0] - 1
    annualized_return = (1 + total_return) ** (trading_days / len(portfolio)) - 1

    cumulative_max = np.maximum.accumulate(portfolio)
    drawdown = portfolio / cumulative_max - 1
    max_drawdown = drawdown.min()

    mean_daily_return = np.mean(daily_returns)
    std_daily_return = np.std(daily_returns)
    annualized_sharpe_ratio = (mean_daily_return - risk_free_rate / trading_days) / std_daily_return * np.sqrt(
        trading_days)

    return annualized_return, max_drawdown, annualized_sharpe_ratio


def print_portfolio_metrics(portfolio):
    annualized_return, max_drawdown, annualized_sharpe_ratio = calculate_portfolio_metrics(portfolio)
    print(f"年化回报: {annualized_return*100:.3f}%, 最大回撤: {max_drawdown*100:.3f}%, 夏普率: {annualized_sharpe_ratio:.5f}")
