from typing import TYPE_CHECKING

import numpy as np
import pandas as pd
import scipy.stats

from quantopy.stats import (
    financial,
    stats,
)

if TYPE_CHECKING:
    from quantopy.core.return_frame import ReturnDataFrame


class ReturnSeries(pd.Series):
    @property
    def _constructor(self):
        return ReturnSeries

    @property
    def _constructor_expanddim(self):
        """
        Used when a manipulation result has one higher dimension as the
        original, such as ReturnSeries.to_frame()
        """
        from quantopy.core.return_frame import ReturnDataFrame

        return ReturnDataFrame

    @classmethod
    def from_price(cls, price) -> "ReturnSeries":
        """
        Generate a new ReturnSeries with simple returns from given prices.

        Parameters
        ----------
        price : array-like or Iterable
            Contains price stored in Series.

        Returns
        -------
        ReturnSeries
            A new ReturnSeries object with simple returns for the given price series.

        See Also
        --------
        ReturnDataFrame.from_price: Analogous function for ReturnDataFrame.

        Examples
        --------
        >>> qp.ReturnSeries.from_price([10, 15, 20])
        1    0.500000
        2    0.333333
        dtype: float64

        >>> qp.ReturnSeries.from_price(np.array([10, 15, 20]))
        1    0.500000
        2    0.333333
        dtype: float64

        >>> qp.ReturnSeries.from_price(pd.Series([10, 15, 20]))
        1    0.500000
        2    0.333333
        dtype: float64
        """
        return financial.get_simple_returns_from_price(
            ReturnSeries(price, dtype="float64")
        )

    def cumulated(self) -> "ReturnSeries":
        """
        Compute the cumulated indexed values from simple returns.

        Returns
        -------
        ReturnSeries
            A ReturnSeries object with cumulated indexed values.

        Examples
        --------
        >>> rs = qp.ReturnSeries([0.5, 0.333333])
        >>> rs.cumulated()
        1    1.5
        2    2.0
        dtype: float64
        """
        return financial.cumulated(self)

    def mean(self) -> np.float64:
        """
        Compute the arithmetic mean of pasts returns.

        Returns
        -------
        np.float64
            The arithmetic mean of past returns.

        Examples
        --------
        >>> rs = qp.ReturnSeries([0.3, 0.1, -0.2, -0.1, 0.25])
        >>> rs.mean()
        0.06999
        """
        return super().mean()

    def gmean(self) -> np.float64:
        """
        Compute the geometric mean of series of returns. Commonly used to determine the
        performance results of an investment or portfolio.

        Return the geometric average of the simple returns.
        That is:  n-th root of (1+R1) * (1+R2) * ... * (1+Rn)

        Returns
        -------
        np.float64
            The geometric mean of past simple returns

        References
        ----------
        .. [1] "Weighted Geometric Mean", *Wikipedia*,
                    https://en.wikipedia.org/wiki/Weighted_geometric_mean.

        Examples
        --------
        >>> rs = qp.ReturnSeries([-0.1, 0.25, 0.05])
        >>> rs.gmean()
        0.057094
        """
        return stats.gmean(self)

    def annualized(
        self,
        period: stats.period = stats.period.MONTHLY,
    ) -> np.float64:
        """
        Determines the annualized rate of return. Commonly used for comparison
        of investment that have different time lenghts.

        Parameters
        ----------
        period : period, default period.MONTHLY
            Defines the periodicity of the 'returns' for purposes of
            annualizing.

        Returns
        -------
        np.float64
            The annualized rate of return

        Examples
        --------
        >>> rs = qp.ReturnSeries([0.01, 0.02])
        >>> rs.gmean()
        0.014987
        >>> rs.annualized(period=qp.stats.period.DAILY)
        41.47317
        >>> rs.annualized(period=qp.stats.period.WEEKLY)
        1.167505
        >>> rs.annualized(period=qp.stats.period.MONTHLY)
        0.195444
        >>> rs.annualized(period=qp.stats.period.YEARLY)
        0.195444
        """
        return stats.annualized(self, period)

    def sharpe_ratio(
        self, riskfree_rate: float, period: stats.period = stats.period.MONTHLY
    ) -> np.float64:
        """Compute the sharpe ratio. Commonly used to measure the performance of an investment compared
        to a risk-free asset, after adjusting for its risk.

        Return the difference between the returns of the investment and the risk-free return,
        divided by the standard deviation of the investment.

        Parameters
        ----------

        riskfree_rate: float
            Risk free rate, with the same periodicity as simple retuns (e.g. daily, monthly, ...).

        period : period, default period.MONTHLY
            Defines the periodicity of the 'returns' data for purposes of
            annualizing.

        Returns
        -------
        sharpe_ratio : np.float64

        References
        ----------
        .. [1] "Sharpe Ratio", *Wikipedia*, https://en.wikipedia.org/wiki/Sharpe_ratio.
        """
        return financial.sharpe(self, riskfree_rate, period)

    def drawdown(self) -> "ReturnDataFrame":
        """Compute the maximum drawdown in series of simple returns. Commonly used to measure the risk
        of a portfolio.

        Returns
        -------
        out : qp.ReturnDataFrame

        References
        ----------
        .. [1] "Drawdown", *Wikipedia*, https://en.wikipedia.org/wiki/Drawdown_(economics).
        """
        return financial.drawdown(self)

    def effect_vol(
        self,
        period: stats.period = stats.period.MONTHLY,
    ) -> np.float64:
        """
        Determines the annual effective annual volatility.

        Parameters
        ----------
        period : period, default period.MONTHLY
            Defines the periodicity of the 'returns' data for purposes of
            annualizing.

        Returns
        -------
        effective_annual_volatility : np.float64
        """
        return stats.effect_vol(self, period)

    def total_return(self) -> np.float64:
        """
        Compute total returns.

        Returns
        -------
        total_returns : np.float64
        """
        return stats.total_return(self)

    def log(self):
        return (self + 1).apply(np.log)  # type: ignore

    def skew(self):
        return scipy.stats.skew(self)

    def kurtosis(self):
        return scipy.stats.kurtosis(self) + 3

    def is_normal(self, pvalue=0.01):
        jb_value, p = scipy.stats.jarque_bera(self)
        return p > pvalue
