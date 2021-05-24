from typing import Union

import pandas as pd
from pandas.core.generic import NDFrame

from quantopy._typing import FrameOrSeries, PythonScalar


def returns(prices: FrameOrSeries, drop_first: bool = True) -> FrameOrSeries:
    """
    Compute simple returns from a timeseries of prices.

    Parameters
    ----------
    prices : pd.Series or pd.DataFrame
        Prices of assets in wide-format, with assets as columns,
        and indexed by datetimes.

    drop_first: bool, default True
        How to handle the initial obvservation.

    Returns
    -------
        returns : pd.Series or pd.DataFrame
            The same type as the calling object.

    """
    out = prices.pct_change()

    if drop_first:
        out = out.iloc[1:]

    return out


def cum_returns_final(returns: FrameOrSeries) -> Union[pd.Series, PythonScalar]:
    """
    Compute total returns from simple returns.
    Parameters
    ----------
    returns : pd.DataFrame, pd.Series
       Noncumulative simple returns of one or more timeseries.

    Returns
    -------
    total_returns : pd.Series or scalar
        If input is 1-dimensional (a Series), the result is a scalar.
        If input is 2-dimensional (a DataFrame), the result is a 1D array
        containing cumulative returns for each column of input.
    """
    return (returns + 1).prod() - 1
