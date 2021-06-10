from typing import (
    List,
    Optional,
    Union,
    overload,
)

import numpy as np
import pandas as pd

from quantopy._typing import PythonScalar
from quantopy.core.return_frame import ReturnDataFrame
from quantopy.core.return_series import ReturnSeries


def normal_returns(mu: np.ndarray, sigma: np.ndarray, size: int) -> np.ndarray:
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

    Returns
    -------
    out : ndarray or scalar
        Drawn samples from a a normal (Gaussian) distribution.

    References
    ----------
    .. [1] "Normal distribution", *Wikipedia*, https://en.wikipedia.org/wiki/Normal_distribution.
    """
    return np.random.normal(mu, sigma, (size,) + mu.shape)


def log_normal_returns(mu: np.ndarray, sigma: np.ndarray, size: int) -> np.ndarray:
    """Generate random simple returns from a log-normal distribution.

    Parameters
    ----------
    mu : float or array_like of floats
        Mean value of the underlying normal distribution.

    sigma : float or array_like of floats
       Standard deviation of the underlying normal distribution.

    size : int or tuple of ints, optional
        Output shape. If the given shape is, e.g., (m, n, k), then m * n * k samples
        are drawn. If size is None (default), a single value is returned if mu and sigma
        are both scalars. Otherwise, np.broadcast(mu, sigma).size samples are drawn.

    Returns
    -------
    out : ndarray or scalar
        Drawn samples from the parameterized log-normal distribution.

    References
    ----------
    .. [1] "Log-Normal distribution", *Wikipedia*,
                https://en.wikipedia.org/wiki/Log-normal_distribution.
    """
    log_returns = np.random.normal(mu, sigma, (size,) + mu.shape)

    return np.exp(log_returns) - 1


# def geometric_brownian_motion(
#     mu: np.ndarray, sigma: np.ndarray, size: int, dt: int = 1
# ) -> np.ndarray:
#     """Generate random simple returns from a geometric brownian motion.

#     Parameters
#     ----------
#     mu : float or array_like of floats
#         Mean (“centre”) of the distribution.

#     sigma : float or array_like of floats
#        Standard deviation (spread or “width”) of the distribution. Must be non-negative.

#     size : int or tuple of ints, optional
#         Output shape. If the given shape is, e.g., (m, n, k), then m * n * k samples
#         are drawn. If size is None (default), a single value is returned if mu and sigma
#         are both scalars. Otherwise, np.broadcast(mu, sigma).size samples are drawn.

#     Returns
#     -------
#     out : ndarray or scalar
#         Drawn samples from a geometric brownian motion.

#     References
#     ----------
#     .. [1] "Geometric Brownian Motion", *Wikipedia*,
#                 https://en.wikipedia.org/wiki/Geometric_Brownian_motion.
#     """
#     brownian_path = np.random.normal(0, np.sqrt(dt), size=(size,) + mu.shape)

#     drift = mu - sigma ** 2 / 2
#     difussion = sigma * brownian_path

#     simulated_returns = drift + difussion

#     return simulated_returns


@overload
def returns(
    mu: PythonScalar, sigma: PythonScalar, size: Optional[int] = None, method: str = ...
) -> ReturnSeries:
    ...


@overload
def returns(
    mu: Union[List[int], List[float]],
    sigma: Union[List[int], List[float]],
    size: Optional[int] = None,
    method: str = ...,
) -> ReturnDataFrame:
    ...


def returns(mu, sigma, size=None, method="normal"):
    """Generate simple returns from a given method:
        - 'normal': gaussian distribution
        - 'lognormal': gaussian distribution
        - 'gbr': geometric brownian motion

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
        The name of a method used for returns generation

    Returns
    -------
    out : ndarray or scalar
        Generated returns.

    See Also
    --------
    normal_returns, geometric_brownian_motion

    References
    ----------
    .. [1] "Normal distribution", *Wikipedia*,
                https://en.wikipedia.org/wiki/Normal_distribution.
    .. [2] "Geometric Brownian Motion", *Wikipedia*,
                https://en.wikipedia.org/wiki/Geometric_Brownian_motion.
    """
    mu = np.asarray(mu)
    sigma = np.asarray(sigma)

    if method == "normal":
        simulated_returns = normal_returns(mu, sigma, size)
    elif method == "lognormal":
        simulated_returns = log_normal_returns(mu, sigma, size)
    # elif method == "gbm":
    #     simulated_returns = geometric_brownian_motion(mu, sigma, size)
    else:
        raise ValueError(f"Invalid method {method}")

    if len(simulated_returns.shape) == 1:
        return ReturnSeries(simulated_returns)
    else:
        return ReturnDataFrame(simulated_returns)


@overload
def prices(
    initial_price: Union[int, float],
    mu: PythonScalar,
    sigma: PythonScalar,
    size: Optional[int] = None,
    method: str = ...,
) -> ReturnSeries:
    ...


@overload
def prices(
    initial_price: Union[List[int], List[float]],
    mu: Union[List[int], List[float]],
    sigma: Union[List[int], List[float]],
    size: Optional[int] = None,
    method: str = ...,
) -> ReturnDataFrame:
    ...


def prices(initial_price, mu, sigma, size=None, method="normal"):
    """Generate price evolution from a given method for returns distribution:
        - 'normal': gaussian distribution
        - 'gbr': geometric brownian motion

    Parameters
    ----------
    initial_price : float or array_like of floats

    mu : float or array_like of floats
        Mean (“centre”) of the distribution.

    sigma : float or array_like of floats
       Standard deviation (spread or “width”) of the distribution. Must be non-negative.

    size : int or tuple of ints, optional
        Output shape. If the given shape is, e.g., (m, n, k), then m * n * k samples
        are drawn. If size is None (default), a single value is returned if mu and sigma
        are both scalars. Otherwise, np.broadcast(mu, sigma).size samples are drawn.

    method: str
        The name of a method used for returns generation

    Returns
    -------
    out : ndarray or scalar
        Generated prices.

    See Also
    --------
    returns, normal_returns, geometric_brownian_motion

    References
    ----------
    .. [1] "Normal distribution", *Wikipedia*,
                https://en.wikipedia.org/wiki/Normal_distribution.
    .. [2] "Geometric Brownian Motion", *Wikipedia*,
                https://en.wikipedia.org/wiki/Geometric_Brownian_motion.
    """
    simulated_returns = returns(mu, sigma, size - 1, method)

    # if method == "gbm":
    #     simulated_returns = np.exp(simulated_returns)

    simulated_prices = initial_price * (simulated_returns + 1).cumprod()

    if len(simulated_returns.shape) == 1:
        simulated_prices = pd.concat([pd.Series([initial_price]), simulated_prices])
    else:
        simulated_prices = pd.concat([pd.DataFrame([initial_price]), simulated_prices])

    return simulated_prices
