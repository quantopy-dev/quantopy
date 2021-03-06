from typing import (
    TYPE_CHECKING,
    overload,
)

import numpy as np
import scipy.stats

from quantopy.stats.period import (
    annualization_factor,
    period,
)

if TYPE_CHECKING:
    from quantopy.core.return_frame import ReturnDataFrame
    from quantopy.core.return_series import ReturnSeries


@overload
def gmean(simple_returns: "ReturnSeries") -> np.float64:
    ...


@overload
def gmean(
    simple_returns: "ReturnDataFrame",
) -> "ReturnSeries":
    ...


def gmean(simple_returns):
    """
    Compute the geometric mean of series of returns. Commonly used to determine the
    performance results of an investment or portfolio.

    Return the geometric average of the simple returns.
    That is:  n-th root of (1+R1) * (1+R2) * ... * (1+Rn)

    Parameters
    ----------
    simple_returns : qp.ReturnDataFrame or qp.ReturnSeries
        The simple returns series.

    Returns
    -------
    qp.ReturnSeries or np.float64
        The geometric mean of past simple returns

    References
    ----------
    .. [1] "Weighted Geometric Mean", *Wikipedia*,
                https://en.wikipedia.org/wiki/Weighted_geometric_mean.

    Examples
    --------
    >>> qp.stats.gmean(qp.ReturnSeries([-0.1, 0.25, 0.05]))
    0.057094
    >>> qp.stats.gmean(qp.ReturnDataFrame(
                    {
                        "stock_1": [0.5, 0.333333],
                        "stock_2": [-0.333333, 0.75]
                    }
            ))
    stock_1    0.414213
    stock_2    0.080124
    dtype: float64
    """
    return (simple_returns + 1).aggregate(scipy.stats.gmean) - 1


@overload
def annualized(
    simple_returns: "ReturnDataFrame", period: period = ...
) -> "ReturnSeries":
    ...


@overload
def annualized(simple_returns: "ReturnSeries", period: period = ...) -> np.float64:
    ...


def annualized(simple_returns, period=period.MONTHLY):
    """
    Determines the annualized rate of return. Commonly used for comparison
    of investment that have different time lenghts.

    Parameters
    ----------
    simple_returns : qp.ReturnSeries or qp.ReturnDataFrame
        The simple returns series.

    period : period, default period.MONTHLY
        Defines the periodicity of the 'returns' for purposes of
        annualizing.

    Returns
    -------
    np.float64 or qp.ReturnSeries
        The annualized rate of return

    Examples
    --------
    >>> qp.stats.annualized(qp.ReturnSeries([0.01, 0.02]), period=qp.stats.period.MONTHLY)
    0.195444
    >>> qp.stats.annualized(qp.ReturnDataFrame(
            {
                "stock_1": [0.01, 0.02],
                "stock_2": [-0.333333, 0.75]
            }),
            period=qp.stats.period.WEEKLY
        )
    stock_1     1.167505
    stock_2    54.032872
    dtype: float64
    """
    ann_factor = annualization_factor[period]

    return (simple_returns.gmean() + 1) ** ann_factor - 1


@overload
def effect_vol(
    simple_returns: "ReturnDataFrame", period: period = ...
) -> "ReturnSeries":
    ...


@overload
def effect_vol(simple_returns: "ReturnSeries", period: period = ...) -> np.float64:
    ...


def effect_vol(
    simple_returns,
    period=period.MONTHLY,
):
    """
    Determines the annual effective annual volatility given the compounding period.

    Parameters
    ----------
    period : period, default period.MONTHLY
        Defines the periodicity of the 'returns' data for purposes of
        annualizing.

    Returns
    -------
    effective_annual_volatility : qp.ReturnSeries or qp.ReturnDataFrame
    """
    ann_factor = annualization_factor[period]

    return simple_returns.std() * np.sqrt(ann_factor)


@overload
def total_return(simple_returns: "ReturnDataFrame") -> "ReturnSeries":
    ...


@overload
def total_return(simple_returns: "ReturnSeries") -> np.float64:
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
