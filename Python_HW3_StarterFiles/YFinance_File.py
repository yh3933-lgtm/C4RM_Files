import numpy as np
import pandas as pd

def Data2returns(YahooData=None, symbol='AAPL'):
    """
    Input:
    YahooData = data from Yahoo Finance

    Output:
    returns = array of returns

    Steps:
    extract 'Close' and symbol (This is a 2d column. Demo below.)
    calculate and return the lagged returns
    """

    if YahooData is None or not isinstance(YahooData, pd.DataFrame) or YahooData.empty:
        raise ValueError("YahooData must be a non-empty pandas DataFrame.")

    close_series = None
    columns = YahooData.columns

    if isinstance(columns, pd.MultiIndex):

        if 'Close' in columns.get_level_values(0) and symbol in columns.get_level_values(1):
            close_series = YahooData[('Close', symbol)]

        elif symbol in columns.get_level_values(0) and 'Close' in columns.get_level_values(1):
            close_series = YahooData[(symbol, 'Close')]

        elif 'Close' in columns.get_level_values(0):
            close_series = YahooData.xs('Close', axis=1, level=0).iloc[:, 0]

        elif 'Close' in columns.get_level_values(1):
            close_series = YahooData.xs('Close', axis=1, level=1).iloc[:, 0]

    else:
        if 'Close' in columns:
            close_series = YahooData['Close']
        elif symbol in columns:
            close_series = YahooData[symbol]
        else:
            close_series = YahooData.iloc[:, 0]

    if close_series is None:
        raise ValueError("Could not locate Close price column for the provided YahooData/symbol.")

    prices = np.asarray(close_series, dtype=float)
    prices = prices[~np.isnan(prices)]

    if prices.size < 2:
        raise ValueError("Need at least 2 valid close prices to compute returns.")

    returns = prices[1:] / prices[:-1] - 1
    return returns
