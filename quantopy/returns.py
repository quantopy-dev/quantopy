from typing import Union, overload

import pandas as pd
import numpy as np
from pandas.core.generic import NDFrame
import quantopy

from quantopy._typing import FrameOrSeries, PythonScalar
from quantopy import periods


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


@overload
def effect(nominal_rate: pd.Series, period: periods.Period = ...) -> pd.Series:
    ...


@overload
def effect(nominal_rate: np.ndarray, period: periods.Period = ...) -> np.ndarray:
    ...


@overload
def effect(nominal_rate: PythonScalar, period: periods.Period = ...) -> PythonScalar:
    ...


def effect(
    nominal_rate,
    period=periods.Period.DAILY,
):
    """
    Determines the annual effective annual interest rate given the nominal rate and
    the compounding period.

    Parameters
    ----------
    nominal_rate : pd.Series, np.ndarray or PythonScalar
        The nominal interest rate.

    period : periods.Period, deafult periods.Period.DAILY
        Defines the periodicity of the 'returns' data for purposes of
        annualizing.

    Returns
    -------
        effective_annual_rate : pd.Series, np.ndarray or PythonScalar
    """
    ann_factor = periods.annualization_factor[period]

    return (nominal_rate + 1) ** ann_factor - 1
