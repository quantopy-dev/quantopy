from typing import TYPE_CHECKING, overload

import numpy as np
from quantopy.stats.period import period

if TYPE_CHECKING:
    from quantopy.core.return_frame import ReturnDataFrame
    from quantopy.core.return_series import ReturnSeries


@overload
def sharpe(
    simple_returns: "ReturnSeries", riskfree_rate: float, period: period = ...
) -> np.float64:
    ...


@overload
def sharpe(
    simple_returns: "ReturnDataFrame", riskfree_rate: float, period: period = ...
) -> "ReturnSeries":
    ...


def sharpe(simple_returns, riskfree_rate, period=period.MONTHLY):
    """Compute the sharpe ratio of series of returns. Commonly used to measure the performance
    of an investment compared to a risk-free asset, after adjusting for its risk.

    Return the difference between the returns of the investment and the risk-free return,
    divided by the standard deviation of the investment.

    Parameters
    ----------
    simple_returns : qp.ReturnDataFrame or qp.ReturnSeries
        Input array or object that can be converted to an array.

    riskfree_rate: float
        Risk free rate, with the same periodicity as simple retuns (e.g. daily, monthly, ...).

    period : period, default period.MONTHLY
        Defines the periodicity of the 'returns' data for purposes of
        annualizing.

    Returns
    -------
    sharpe_ratio : qp.ReturnSeries or np.float64

    References
    ----------
    .. [1] "Sharpe Ratio", *Wikipedia*, https://en.wikipedia.org/wiki/Sharpe_ratio.
    """
    excess_return = simple_returns.effect(period) - riskfree_rate

    return excess_return / simple_returns.effect_vol(period)
