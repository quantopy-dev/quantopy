from typing import List, Optional, Tuple, Union, overload

import numpy as np
import pandas as pd

import quantopy as qp
from quantopy._typing import PythonScalar


@overload
def returns(
    mu: PythonScalar,
    sigma: PythonScalar,
    size: Optional[int] = None,
    method: str = ...
) -> qp.ReturnSeries:
    ...


@overload
def returns(
    mu: Union[List[int], List[float]],
    sigma: Union[List[int], List[float]],
    size: Optional[int] = None,
    method: str = ...
) -> qp.ReturnDataFrame:
    ...


def returns(
    mu,
    sigma,
    size=None,
    method='basic'
):
    """Generate random simple returns from a normal (Gaussian) distribution.

    Parameters
    ----------
    mu : float or array_like of floats
        Mean (“centre”) of the distribution.

    sigma : float or array_like of floats
       Standard deviation (spread or “width”) of the distribution. Must be non-negative.

    size : int or tuple of ints, optional
        Output shape. If the given shape is, e.g., (m, n, k), then m * n * k samples
        are drawn. If size is None (default), a single value is returned if mu and sigma
        are both scalars. Otherwise, np.broadcast(mu, sigma).size samples are drawn.

    method: str
        Method used for returns generation

    Returns
    -------
    out : ndarray or scalar
        Drawn samples from the parameterized normal distribution.

    References
    ----------
    .. [1] "Normal distribution", *Wikipedia*, https://en.wikipedia.org/wiki/Normal_distribution.
    """
    mu = np.asarray(mu)
    sigma = np.asarray(sigma)

    if method == 'basic':
        simulated_returns = np.random.normal(mu, sigma, (size,) + mu.shape)
    elif method == 'gbm':
        dt = 1
        brownian_increments = np.random.normal(0, np.sqrt(dt), (size,) + mu.shape)
        simulated_returns = (mu - sigma ** 2 / 2) * dt + brownian_increments
    else:
        raise ValueError(f"Invalid method {method}")

    if len(simulated_returns.shape) == 1:
        return qp.ReturnSeries(simulated_returns)
    else:
        return qp.ReturnDataFrame(simulated_returns)
