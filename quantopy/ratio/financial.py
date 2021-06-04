from typing import TYPE_CHECKING, overload

import numpy as np

if TYPE_CHECKING:
    from quantopy.core.return_dataframe import ReturnDataFrame
    from quantopy.core.return_series import ReturnSeries


@overload
def sharpe(simple_returns: "ReturnSeries", riskfree_rate: float) -> np.float64:
    ...


@overload
def sharpe(simple_returns: "ReturnDataFrame", riskfree_rate: float) -> "ReturnSeries":
    ...


def sharpe(simple_returns, riskfree_rate):
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

    Returns
    -------
    sharpe_ratio : qp.ReturnSeries or np.float64

    References
    ----------
    .. [1] "Sharpe Ratio", *Wikipedia*, https://en.wikipedia.org/wiki/Sharpe_ratio.
    """
    excess_return = simple_returns.mean() - riskfree_rate

    return excess_return / simple_returns.std()
