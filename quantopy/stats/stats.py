from typing import TYPE_CHECKING, overload

import numpy as np
from quantopy.stats.period import annualization_factor, period

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
    """Compute the geometric mean of series of returns. Commonly used to determine the
    performance results of an investment or portfolio.

    Return the geometric average of the simple returns.
    That is:  n-th root of (1+R1) * (1+R2) * ... * (1+Rn)

    Parameters
    ----------
    simple_returns : qp.ReturnDataFrame or qp.ReturnSeries
        Input array or object that can be converted to an array.

    Returns
    -------
    gmean : qp.ReturnSeries or np.float64

    References
    ----------
    .. [1] "Weighted Geometric Mean", *Wikipedia*, https://en.wikipedia.org/wiki/Weighted_geometric_mean.
    """
    log_values = np.log(simple_returns + 1)

    return np.exp(log_values.mean()) - 1


@overload
def effect(simple_returns: "ReturnDataFrame", period: period = ...) -> "ReturnSeries":
    ...


@overload
def effect(simple_returns: "ReturnSeries", period: period = ...) -> np.float64:
    ...


def effect(
    simple_returns,
    period=period.MONTHLY,
):
    """
    Determines the annual effective annual interest rate given the nominal rate and
    the compounding period.

    Parameters
    ----------
    simple_returns : qp.ReturnSeries or qp.ReturnDataFrame
        The simple returns series of frame.

    period : period, default period.MONTHLY
        Defines the periodicity of the 'returns' data for purposes of
        annualizing.

    Returns
    -------
    effective_annual_rate : qp.ReturnSeries or qp.ReturnDataFrame
    """
    ann_factor = annualization_factor[period]

    return (simple_returns.mean() + 1) ** ann_factor - 1
