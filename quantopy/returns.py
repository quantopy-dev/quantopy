from typing import overload

import numpy as np
import pandas as pd

from quantopy import periods
from quantopy._typing import FrameOrSeries, PythonScalar


@overload
def returns(prices: pd.DataFrame, drop_first: bool = ...) -> pd.DataFrame:
    ...


@overload
def returns(prices: pd.Series, drop_first: bool = ...) -> pd.Series:
    ...


@overload
def returns(prices: np.ndarray, drop_first: bool = ...) -> np.ndarray:
    ...


def returns(prices, drop_first=True):
    """
    Compute simple returns from a timeseries of prices.

    Parameters
    ----------
    prices : pd.Series, pd.DataFrame or np.ndarray
        Prices of assets in wide-format, with assets as columns,
        and indexed by datetimes.

    drop_first: bool, default True
        How to handle the initial obvservation.

    Returns
    -------
    returns : pd.Series, pd.DataFrame or np.ndarray
    """
    if isinstance(prices, (pd.DataFrame, pd.Series)):
        out = prices.pct_change()

        if drop_first:
            out = out.iloc[1:]
    else:
        # Assume np.ndarray
        out = np.diff(prices, axis=0)
        np.divide(out, prices[:-1], out=out)

        if not drop_first:
            out = np.insert(out, 0, np.NaN, axis=0)

    return out


@overload
def total_return(simple_returns: pd.DataFrame) -> pd.Series:
    ...


@overload
def total_return(simple_returns: pd.Series) -> PythonScalar:
    ...


@overload
def total_return(simple_returns: np.ndarray) -> PythonScalar:
    ...


def total_return(simple_returns):
    """
    Compute total returns from simple returns.

    Parameters
    ----------
    returns : pd.DataFrame or pd.Series
       Noncumulative simple returns of one or more timeseries.

    Returns
    -------
    total_returns : pd.Series or PythonScalar
    """
    return (simple_returns + 1).prod() - 1


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

    period : periods.Period, default periods.Period.DAILY
        Defines the periodicity of the 'returns' data for purposes of
        annualizing.

    Returns
    -------
    effective_annual_rate : pd.Series, np.ndarray or PythonScalar
    """
    ann_factor = periods.annualization_factor[period]

    return (nominal_rate + 1) ** ann_factor - 1


@overload
def effect_vol(nominal_vol: pd.Series, period: periods.Period = ...) -> pd.Series:
    ...


@overload
def effect_vol(nominal_vol: np.ndarray, period: periods.Period = ...) -> np.ndarray:
    ...


@overload
def effect_vol(nominal_vol: PythonScalar, period: periods.Period = ...) -> PythonScalar:
    ...


def effect_vol(nominal_vol, period=periods.Period.DAILY):
    """
    Determines the annual effective annual volatility given the nominal volatility and
    the compounding period.

    Parameters
    ----------
    nominal_vol : pd.Series, np.ndarray or PythonScalar
        The nominal volatility.

    period : periods.Period, default periods.Period.DAILY
        Defines the periodicity of the 'returns' data for purposes of
        annualizing.

    Returns
    -------
    effective_annual_volatility : pd.Series, np.ndarray or PythonScalar
    """
    ann_factor = periods.annualization_factor[period]

    return nominal_vol * np.sqrt(ann_factor)
