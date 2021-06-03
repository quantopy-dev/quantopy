from typing import overload

import numpy as np

import quantopy as qp


@overload
def gmean(simple_returns: qp.ReturnSeries) -> np.float64:
    ...


@overload
def gmean(
    simple_returns: qp.ReturnDataFrame,
) -> qp.ReturnSeries:
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
